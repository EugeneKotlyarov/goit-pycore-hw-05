import argparse
import collections
import re
from datetime import datetime as dt
from pathlib import Path
from typing import Callable


# Welcome to logfiles parser (damn, i like how i did it :)
#
# Here is top down a description for constants and methods
# ATTANTION: this realisation covers any kind of levels, not just INFO, DEBUG, ERROR and WARNING
# it can be any other like CRITICAL, VERBOSE, etc
#
# Please use const COUNTS_TABLE_COLUMN_WIDTH >= 16 for better formatting, less is not forbidden
# but gives you a broken output table
#
# we use ARGPARSE for for command-line options
#
# PARSE_LOG_LINE function accepts one log line at a time. First - check line consistency by regex and return error if any.
# Next is to creating list of values by dividing line by split():
# 0 - date, 1 - time, 2 - level, 3 - rest of line to log message
# finally zip keys and values to dict and return it
#
# LOAD_LOGS function reads input file, check if its exists, permissions or any other error (can come from PARSE_LOG_LINE).
# Parse line by line using PARSE_LOG_LINE function and returns list of dicts
# Covers errors (if any) making list from it to return, because function must return list
#
# FILTER_LOGS_BY_LEVEL function accepts full list of dicts table with logs and specified level.
# Prints title, filtered list by filter() and lambda and prints the result list
# also returns result list
#
# COUNT_LOGS_BY_LEVEL function accepts full list of dicts table with logs
# and counts messages per level using Counter. Returns result as dict
#
# DISPLAY_LOG_COUNTS function simply output counted levels as a table
#
# MAIN do the rest. It gets arguments, call the functions and process the errors if any returns

COUNTS_TABLE_COLUMN_WIDTH = 16


parser = argparse.ArgumentParser(description="Logs parser")
parser.add_argument(
    "--logfile",
    help="Typical log file with date level and text [required]",
    required=True,
)
parser.add_argument(
    "--level",
    help="Enter to show only specific level's records [optional]",
    required=False,
)

arguments = vars(parser.parse_args())


def parse_log_line(line: str) -> dict:
    # verification for line format beginnig: "YYYY-MM-DD HH:MM:SS LEVEL message"
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]+ .+")
    if not re.search(pattern, line):
        return {
            "error": f'\nLog line pattern "YYYY-MM-DD HH:MM:SS LEVEL message" was not recognized in line:\n{line}'
        }

    keys = ["date", "time", "level", "message"]
    values = line.split()[0:3]
    values.append(" ".join(line.split()[3:]))
    log_line_as_dict = dict(zip(keys, values))
    return log_line_as_dict


def load_logs(file_path: str) -> list:
    logs_file_path = Path(file_path)
    logs_list = []
    try:
        with open(logs_file_path, "r") as file:
            for line in file:
                parsed_line = parse_log_line(line.strip())
                if not parsed_line.get("error"):
                    logs_list.append(parsed_line)
                else:
                    return ["error", parsed_line["error"]]
        return logs_list
    except FileNotFoundError:
        return ["error", "File Not Found"]
    except PermissionError:
        return ["error", "Permission Denied"]
    except Exception as excpt:
        return ["error", str(excpt)]


def filter_logs_by_level(logs: list, level: str) -> list:
    print(f"\nДеталі логів для рівня {level}:")
    logs_by_level = filter(lambda a: a["level"] == level, logs)
    for l in logs_by_level:
        print(f"{l["date"]} {l["time"]} - {l["message"]}")
    return logs_by_level


def count_logs_by_level(logs: list) -> dict:
    keys = [line.get("level") for line in logs]
    return dict(collections.Counter(keys))


def display_log_counts(counts: dict):
    print(f'\nРівень логування{" " * (COUNTS_TABLE_COLUMN_WIDTH - 16)}| Кількість')
    print(f'{"-" * COUNTS_TABLE_COLUMN_WIDTH}+{"-" * COUNTS_TABLE_COLUMN_WIDTH}')
    for k, v in counts.items():
        print(f'{k}{" " * (COUNTS_TABLE_COLUMN_WIDTH - len(k))}| {v}')


def main():

    logs = load_logs(arguments["logfile"])
    if logs[0] != "error":
        display_log_counts(count_logs_by_level(logs))
        if arguments["level"]:
            filter_logs_by_level(logs, str(arguments["level"]).upper())
    else:
        print(f"Error while reading file:\n{arguments["logfile"]}: {logs[1]}")


if __name__ == "__main__":
    main()
