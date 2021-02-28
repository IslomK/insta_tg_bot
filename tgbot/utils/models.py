import logging
from datetime import datetime

from gino import Gino
from sqlalchemy import (Column, Integer, BigInteger, Sequence, String, ForeignKey, Boolean, DateTime)
from sqlalchemy import sql
from sqlalchemy.orm import relationship

db = Gino()

logger = logging.getLogger(__name__)


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String(255))
    full_name = Column(String(100))
    username = Column(String(50))
    is_subscribed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    downloads = relationship("Downloads", back_populates='video')

    query: sql.Select

    def __str__(self):
        return self.full_name

    @staticmethod
    async def get_user(user_id):
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        return user

    async def set_lang(self, lang):
        await self.update(language=lang).apply()


class Video(db.Model):
    __tablename__ = 'videos'
    TIK_TOK = 1
    INSTAGRAM = 2
    YOUTUBE = 3

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    file_id = Column(String(255), unique=True)
    file_id_in_tg = Column(String(255), unique=True)
    file_type = Column(Integer, default=INSTAGRAM)
    url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(), nullable=True)
    download_count = Column(Integer, nullable=True, default=0)

    query: sql.Select

    async def increment_download_count(self):
        self.download_count +=1

    def __str__(self):
        return self.url

    @staticmethod
    async def get_video_by_url(url):
        video = await Video.query.where(Video.url == url).gino.first()
        return video

    @staticmethod
    async def add_video(file_id, file_id_in_tg, url, file_type=None):
        try:
            video = await Video(
                file_id=file_id,
                file_id_in_tg=file_id_in_tg,
                file_type=file_type,
                url=url
            ).create()
        except Exception as ex:
            logger.error("Error while adding new video. Details".format(ex))
            video = None

        return video


class Channel(db.Model):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    chat_id = Column(BigInteger, default=None)
    url = Column(String(255))

    query: sql.Select

    def __str__(self):
        return self.usernamer


class Downloads(db.Model):
    __tablename__ = 'downloads'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    video_id = Column(ForeignKey('videos.id'))
    user_id = Column(ForeignKey('users.id'))
    download_time = Column(DateTime, default=datetime.now())

    video = relationship("Video", foreign_keys=[video_id])
    user = relationship("Users", foreign_keys=[user_id])

    @staticmethod
    async def add_download(video_id, user_id):
        try:
            download = await Downloads(
                video_id=video_id,
                user_id=user_id,
            ).create()

            await download.video.increment_download_count()
        except Exception as ex:
            logger.error("Error while adding download. Details - {}".format(ex))