from abc import ABC, ABCMeta


class CronFieldParsingError(Exception):
    code = "invalid_cron_field"


class CronFieldMetaClass(ABCMeta):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        attr_meta = attrs.pop("Meta", None)
        if attr_meta is not None:
            if not hasattr(attr_meta, "allowed_integer_values"):
                raise ValueError(f"`allowed_integer_values` attribute not defined in Meta for {cls.__name__}")

            new_class.allowed_integer_values = [str(value) for value in attr_meta.allowed_integer_values]
            new_class.slug = attr_meta.slug
            if hasattr(attr_meta, "allowed_text_values"):
                new_class.allowed_text_values = attr_meta.allowed_text_values
            else:
                new_class.allowed_text_values = []

        return new_class


class BaseCronField(ABC, metaclass=CronFieldMetaClass):

    def __init__(self, value):
        self.value = value

    def expand_range(self):
        try:
            start, end = self.value.split("-")
        except ValueError:
            raise CronFieldParsingError(f"Invalid format for {self.slug} range. Range expr should be of format `start-end`")

        if start.isnumeric() != end.isnumeric():
            raise CronFieldParsingError(f"Invalid format for {self.slug} range. Both start and end value of range should be of same type")

        if start.isnumeric():
            allowed_values = self.allowed_integer_values
        else:
            allowed_values = self.allowed_text_values

        try:
            start = allowed_values.index(start)
            end = allowed_values.index(end)
        except ValueError:
            raise CronFieldParsingError(f"Invalid format for {self.slug} range. Invalid start/end value for range expr")

        if start > end:
            raise CronFieldParsingError(f"Invalid format for {self.slug} range. {start} value should be <= {end}")

        return " ".join(self.allowed_integer_values[start:end+1])

    def expand_interval(self):
        first, second = self.value.split("/")

        if not second.isnumeric():
            raise CronFieldParsingError(f"Invalid format for {self.slug} interval. {second} should be an integer")

        if first == "*":
            return ' '.join(
               [i for i in self.allowed_integer_values if int(i) % int(second) == 0]
            )

        if not first.isnumeric():
            raise CronFieldParsingError(f"Invalid format for {self.slug} interval. {first} should be an integer or `*`")

        return " ".join([i for i in range(int(first), self.allowed_integer_values[:-1] + 1) if i % int(second) == 0])

    def expand_list(self):
        input_values = self.value.split(",")
        is_numeric_input = None
        expanded_values = []

        for input_value in input_values:
            if is_numeric_input is None:
                is_numeric_input = input_value.isnumeric()
            elif is_numeric_input != input_value.isnumeric():
                raise CronFieldParsingError(f"Invalid format for {self.slug} list. All values of list should have the same type.")

            if input_value.isnumeric() and input_value not in self.allowed_integer_values:
                raise CronFieldParsingError(f"Invalid format for {self.slug} list. {input_value} not in allowed integer values for {self.slug}")
            elif not input_value.isnumeric():
                if input_value not in self.allowed_text_values:
                    raise CronFieldParsingError(f"Invalid format for {self.slug} list. {input_value} not in allowed text values for {self.slug}")

                input_value = self.allowed_integer_values[self.allowed_text_values.index(input_value)]

            expanded_values.append(input_value)

        return " ".join(expanded_values)

    def expand(self):
        if self.value == "*":
            return " ".join(self.allowed_integer_values)

        if self.value == "?":
            return "Not Specified"

        if "-" in self.value:
            return self.expand_range()

        if "/" in self.value:
            return self.expand_interval()

        if "," in self.value:
            return self.expand_list()

        if (
            (self.value.isnumeric() and self.value in self.allowed_integer_values)
            or self.value in self.allowed_text_values
        ):
            return self.value

        raise CronFieldParsingError(f"Unable to parse {self.slug} field - {self.value}")


class MintuteCronField(BaseCronField):

    class Meta:
        slug = "minute"
        allowed_integer_values = [i for i in range(0, 60)]


class HourCronField(BaseCronField):

    class Meta:
        slug = "hour"
        allowed_integer_values = [i for i in range(0, 24)]


class DayCronField(BaseCronField):

    class Meta:
        slug = "day"
        allowed_integer_values = [i for i in range(0, 32)]


class WeekDayCronField(BaseCronField):

    class Meta:
        slug = "weekday"
        allowed_integer_values = [i for i in range(0, 7)]
        allowed_text_values = [
            "SUN",
            "MON",
            "TUE",
            "WED",
            "THU",
            "FRI",
            "SAT",
        ]


class MonthCronField(BaseCronField):

    class Meta:
        slug = "month"
        allowed_integer_values = [i for i in range(1, 13)]
        allowed_text_values = [
            "JAN",
            "FEB",
            "MAR",
            'APR',
            'MAY',
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
        ]
