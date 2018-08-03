import logging
from os.path import expanduser

home = expanduser('~')
log_file = '{}/tmp/tracker.log'.format(home)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def rank_logger(name, rank, action):
    ranks = (
        "Smiley", "Recruit", "Corporal", "Sergeant",
        "Lieutenant", "Captain", "General"
    )

    logging.info(
        "ACTION: {} | NAME: {} | STATUS: {}"
        .format(action, name, ranks[rank])
    )
