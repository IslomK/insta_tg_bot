import logging

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.redis import RedisStorage
from docs.config import REDIS, BOT_TOKEN


logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage(db=REDIS.get('DB'), host=REDIS.get('HOST'), port=REDIS.get('PORT'))
dp = Dispatcher(bot, storage=storage)
