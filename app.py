import logging

from aiogram import executor
from tgbot.handlers import dp
from docs import config
from tgbot.utils.models import db


logger = logging.getLogger(__name__)

if config.DEBUG:
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] %(message)s\n', level=logging.DEBUG, handlers=[logging.StreamHandler()])
else:
    logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler(config.LOG_PATH)])


async def on_startup(dp):
    logger.info("Connected to the database")
    await db.set_bind(f"postgresql://{config.db_user}:{config.db_pass}@{config.db_host}/{config.db_name}")
    await db.gino.create_all()


async def on_shutdown(dp):
    await db.pop_bind().close()
    logger.info("Disconnected from the database")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)