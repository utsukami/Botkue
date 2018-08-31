import logging
from os.path import expanduser

home = expanduser("~")
log_file = "{}/logs/tracker.log".format(home)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def rank_logger(name, rank, action):
    logging.info(
        "STATUS: {} | RANK: {} | NAME: {}"
        .format(action, rank, name)
    )
