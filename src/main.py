# coding: utf-8

# Generic librairies.
import argparse
import importlib
import logging
import time
import sys

# Third party libs
import schedule

# Project modules.
from conf import config
from utils.fs import list_files, mv_file


def cron(job_module, job_conf):
    """Runs 'check_files' for 'job_module' every x minutes."""
    freq = job_conf.get('freq', 1)

    logger.info(f"Run job {job_module.__name__.split('.')[-1]} every {freq} minute(s).")
    schedule.every(freq).minutes.do(check_files, job_module, job_conf)

    while 1:
        schedule.run_pending()
        time.sleep(1)


def check_files(job_module, job_conf):
    """List files in specific source and run job if files are found."""
    # Parse configuration.
    data_in = job_conf.get('data_in')
    filename_in = job_conf.get('filename_in')

    # List files.
    new_files = list_files(data_in, pattern=filename_in)
    if new_files:
        logger.info("{} new file(s) to process : {}".format(len(new_files), ", ".join(new_files)))
    
    # Run job for each file.
    for f in new_files:
        job_module.run(f, job_conf)


if __name__ == "__main__":

    # Parse command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=str, help="job name")
    parser.add_argument("-cron", action='store_true', help="activate cron mode")
    args = parser.parse_args()

    # Create logger.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s :: %(levelname)s :: %(funcName)15s > %(message)s")
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(fmt)
    logger.addHandler(stdout)

    # Import job.
    try:
        job = importlib.import_module(f"jobs.{args.job}")
    except ModuleNotFoundError as e:
        parser.error(f"{args.job} is not an available job.")

    # Run job.
    if args.cron:
        cron(job, config.jobs[args.job])  # scheduled run
    else:
        check_files(job, config.jobs[args.job])  # one time run
