# Cron Expression Parser

This project implements a CLI using python to parse cron expressions. 

Supported features:
- asterisk (`*`)
- comma separated lists (ex: `1,2,3`)
- time intervals using slashes (ex: `*/10`)
- ranges using hythens (ex: `3-5`)
- capital abbrevations for months (ex: `JAN-MAR`)
- capital abbrevations for weekdays (ex: `MON-WED`)

Unsupported features or features for future development:
- [Non standard characters](https://en.wikipedia.org/wiki/Cron#Non-standard_characters)
- Non capital abbrevations for months and weekdays
- All months are assumed to have 31 days. Different number of days for different months is taken into consideration.

Note that the weekdays numbering starts from 0 and the first weekday is Sunday.

## Installation
Your system should have python with version >= 3.70. 

## Running the parser

Run the following command to parse cron expresion:

```
python cron_parser.py "CRON_EXPRESSION"
```


For example:

```
python cron_parser.py "*/10 0 1,7 * 2-6 /usr/local/server.sh"
```

Running the above command produces the following output:

```
minute        0 10 20 30 40 50
hour          0
day of month  1 7
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   2 3 4 5 6
command       /usr/local/server.sh
```

## Running tests
To run tests, you need to have pytest installed. 

Recommended way to install pytest is using poetry to avoid making changes to global python environment.
If you don't have poetry installed, follow instructions from [here](https://python-poetry.org/docs/) to install poetry.

```
poetry shell
poetry install
```

Once you activate virtual environment, you can run unit tests by running

```
pytest test_parser.py
```
