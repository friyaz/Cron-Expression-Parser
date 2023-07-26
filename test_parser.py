from cron_field import HourCronField, MintuteCronField, DayCronField, WeekDayCronField, MonthCronField, CronFieldParsingError
from cron_parser import CronExprParsingError, CronExpressionParser
import pytest


class TestValidCronExpression:

    @pytest.mark.parametrize("input_value, expected_output", [
        ("*", "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59"),
        ("*/15", "0 15 30 45"),
        ("1-10", "1 2 3 4 5 6 7 8 9 10"),
    ])
    def test_valid_minute_field(self, input_value, expected_output):
        minute_field = MintuteCronField(input_value)
        assert minute_field.expand() == expected_output

    @pytest.mark.parametrize("input_value, expected_output", [
        ("*", "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23"),
        ("8-17", "8 9 10 11 12 13 14 15 16 17"),
        ("0-4", "0 1 2 3 4"),
    ])
    def test_valid_hour_field(self, input_value, expected_output):
        hour_field = HourCronField(input_value)
        assert hour_field.expand() == expected_output

    @pytest.mark.parametrize("input_value, expected_output", [
        ("*", "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31"),
        ("10-20", "10 11 12 13 14 15 16 17 18 19 20"),
        ("1,15,30", "1 15 30"),
    ])
    def test_valid_day_of_month_field(self, input_value, expected_output):
        month_field = DayCronField(input_value)
        assert month_field.expand() == expected_output

    @pytest.mark.parametrize("input_value, expected_output", [
        ("*", "1 2 3 4 5 6 7 8 9 10 11 12"),
        ("2-4", "2 3 4"),
        ("1,6,7", "1 6 7"),
        ("JAN-MAR", "1 2 3"),
        ("FEB,MAY", "2 5")
    ])
    def test_valid_month_field(self, input_value, expected_output):
        day_of_week_field = MonthCronField(input_value)
        assert day_of_week_field.expand() == expected_output

    @pytest.mark.parametrize("input_value, expected_output", [
        ("*", "0 1 2 3 4 5 6"),
        ("2-4", "2 3 4"),
        ("1,6", "1 6"),
        ("MON,WED", "1 3"),
        ("SUN-WED", "0 1 2 3"),
    ])
    def test_valid_day_of_week_field(self, input_value, expected_output):
        day_of_week_field = WeekDayCronField(input_value)
        assert day_of_week_field.expand() == expected_output

    @pytest.mark.parametrize("input_value, expected_output", [
        (
            "*/15 8-17 * * 1-5 /usr/bin/python script.py some args",
            [
                "minute        0 15 30 45",
                "hour          8 9 10 11 12 13 14 15 16 17",
                "day of month  0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31",
                "month         1 2 3 4 5 6 7 8 9 10 11 12",
                "day of week   1 2 3 4 5",
                "command       /usr/bin/python script.py some args",
            ]
        ),
    ])
    def test_cron_expression(self, input_value, expected_output):
        parser = CronExpressionParser(input_value)
        assert parser.describe_cron_expr().split('\n') == expected_output


class TestInValidCronExpression:

    @pytest.mark.parametrize("input_value", ["60-65", "12-3" "100", "ONE", "*/*", "12,89"])
    def test_invalid_minute_field(self, input_value):
        with pytest.raises(CronFieldParsingError):
            minute_field = MintuteCronField(input_value)
            minute_field.expand()

    @pytest.mark.parametrize("input_value", ["24-26", "100"])
    def test_invalid_hour_field(self, input_value):
        with pytest.raises(CronFieldParsingError):
            hour_field = HourCronField(input_value)
            hour_field.expand()

    @pytest.mark.parametrize("input_value", ["32", "100"])
    def test_invalid_day_of_month_field(self, input_value):
        with pytest.raises(CronFieldParsingError):
            day_of_month_field = DayCronField(input_value)
            day_of_month_field.expand()

    @pytest.mark.parametrize("input_value", ["0-8", "10-20", "100", "SUN-5"])
    def test_invalid_day_of_week_field(self, input_value):
        with pytest.raises(CronFieldParsingError):
            day_of_week_field = WeekDayCronField(input_value)
            day_of_week_field.expand()

    @pytest.mark.parametrize("input_value", ["13,15", "100", "JAN/3", "JAN-4", "1,FEB"])
    def test_invalid_month_field(self, input_value):
        with pytest.raises(CronFieldParsingError):
            month_field = MonthCronField(input_value)
            month_field.expand()

    @pytest.mark.parametrize("input_value", [
        "*/15 8-17 * * 1-5",
        "*/10 2-9 * *",
    ])
    def test_invalid_cron_expression(self, input_value):
        with pytest.raises(CronExprParsingError):
            CronExpressionParser(input_value).print_expanded_cron_expr()
