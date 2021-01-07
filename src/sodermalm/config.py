import os
import logging
from typing import List

from starlette.config import Config

logger = logging.getLogger(__name__)


def get_env_tags(tag_list: List[str]) -> dict:
    """Create dictionary of available env tags."""
    tags = {}
    for t in tag_list:
        tag_key, env_key = t.split(":")

        env_value = os.environ.get(env_key)

        if env_value:
            tags.update({tag_key: env_value})

    return tags


# Get env path
package_dir = os.path.dirname(__file__)
root = os.path.normpath(os.path.join(package_dir, os.pardir, os.pardir))

# Build config from env variables
config = Config(os.path.join(root, '.env'))

LOG_LEVEL = config('LOG_LEVEL', default=logging.WARNING)
ENV = config('ENV', default='development')

# database
DATABASE_HOSTNAME = config('DATABASE_HOSTNAME')
DATABASE_CREDENTIALS = config('DATABASE_CREDENTIALS')
DATABASE_NAME = config('DATABASE_NAME', default='sodermalm')
DATABASE_PORT = config('DATABASE_PORT', default='5432')
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DATABASE_CREDENTIALS}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}'