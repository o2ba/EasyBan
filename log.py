from datetime import datetime


# DEFAULT LOG FILE
log_file = 'logs/log'


def error(error_str: str, logfile=log_file):
    with open(logfile, 'a') as file:
        writer = file.write(f"[ERROR] {error_str} @ {datetime.now()}\n")


def warning(warning_str: str, logfile=log_file):
    with open(logfile, 'a') as file:
        writer = file.write(f"[WARNING] {warning_str} @ {datetime.now()}\n")


def log(log_str: str, logfile=log_file):
    with open(logfile, 'a') as file:
        writer = file.write(f"[LOG] {log_str} @ {datetime.now()}\n")
