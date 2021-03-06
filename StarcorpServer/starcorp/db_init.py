from models import Base
from database.static import push_config
from database.session import ENGINE

from utils import get_logger

LOGGER = get_logger(__name__)


def main():
    """ Initialize database data. """
    LOGGER.info("Creating/validating models")
    Base.metadata.create_all(ENGINE)

    push_config()


if __name__ == "__main__":
    main()