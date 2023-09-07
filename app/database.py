import logging
from sqlite3 import Error
import sys

import aiosqlite
from aiosqlite import Connection

from settings import DB_PATH

logger = logging.getLogger(__name__)


class Database:

    @property
    async def connection(self) -> Connection:
        try:
            return await aiosqlite.connect(database=DB_PATH)
        except Error as e:
            logger.error(e)
            sys.exit(e)
