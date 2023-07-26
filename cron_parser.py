from sys import argv

from cron_field import (
    DayCronField,
    HourCronField,
    MintuteCronField,
    MonthCronField,
    WeekDayCronField,
)


class CronExprParsingError(Exception):
    code = "invalid_cron_expr"


class CronExpressionParser:

    def __init__(self, cron_expr):
        self.cron_expr = cron_expr

    def split_cron_expr(self):
        try:
            minute, hour, day, month, week_day, command = self.cron_expr.split(' ', 5)
        except ValueError:
            raise CronExprParsingError("Insufficient numbers of parameters passed.")

        minute = MintuteCronField(minute)
        hour = HourCronField(hour)
        day = DayCronField(day)
        month = MonthCronField(month)
        week_day = WeekDayCronField(week_day)

        return minute, hour, day, month, week_day, command

    def describe_cron_expr(self):
        minute, hour, day, month, week_day, command = self.split_cron_expr()
        return '\n'.join([
            f"minute        {minute.expand()}",
            f"hour          {hour.expand()}",
            f"day of month  {day.expand()}",
            f"month         {month.expand()}",
            f"day of week   {week_day.expand()}",
            f"command       {command}",
        ])

    def print_expanded_cron_expr(self):
        print(self.describe_cron_expr())


if __name__ == "__main__":
    if len(argv) < 2:
        raise CronExprParsingError("No cron expression provided to parse")

    cron_expr_parser = CronExpressionParser(argv[1])
    cron_expr_parser.print_expanded_cron_expr()
