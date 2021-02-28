import os

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
botname = str(os.getenv("BOT_USERNAME"))


admins = os.getenv("ADMIN_ID").split(',')

ip = os.getenv("ip")

I18N_DOMAIN = 'downloader'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALES_DIR = os.path.join(BASE_DIR, 'locales')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

db_user = str(os.getenv("DBUSER"))
db_pass = str(os.getenv('DBPASS'))
db_host = str(os.getenv('HOST'))
db_name = str(os.getenv('DBNAME'))
db_port = os.getenv('DBPORT')
db_admin = os.getenv('SANIC_DB_USER')

ig_regexp = str(os.getenv('INSTAGRAM_REGEXP'))
ig_video_stories = str(os.getenv('INSTAGRAM_STORIES_REGEXP'))

REDIS = {
    'HOST': os.getenv('REDIS_HOST', '127.0.0.1'),
    'PORT': os.getenv('REDIS_PORT', 6379),
    'DB': os.getenv('REDIS_DB', 0),
    'PASSWORD': os.getenv('REDIS_PASSWORD', '')
}

STATIC_DIR = str(BASE_DIR) + '/static/'
DEFAULT_THUMBNAIL = STATIC_DIR + 'default_thumbnail.jpeg'
LOG_PATH = os.getenv('LOG_DIR', '/var/log/downloader/logs.log')

IG_USERNAME = str(os.getenv('IG_USERNAME'))
IG_PASSWORD = str(os.getenv('IG_PASSWORD'))
DEBUG=int(os.getenv('DEBUG', True))
