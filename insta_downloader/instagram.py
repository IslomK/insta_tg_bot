import os

import instaloader
from insta_downloader.core.exceptions import PrivateAccountException
from docs import config


class InstagramDownloader:
    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd
        self.L = instaloader.Instaloader()
        self.L.download_video_thumbnails = False
        self.L.download_comments = False
        self.L.download_geotags = False
        self.L.request_timeout = 5
        self.L.save_metadata = False
        self.L.filename_pattern = '{shortcode}_ig'

        try:
            self.L.load_session_from_file(username, os.path.join(config.BASE_DIR, username))
        except Exception as ex:
            self.L.login(username, pwd)
            self.L.save_session_to_file(os.path.join(config.BASE_DIR, username))

    async def download_post(self, post_id):
        post = instaloader.Post.from_shortcode(self.L.context, post_id)
        downloaded = self.L.download_post(post, 'media')
        return downloaded

    async def get_user(self, username):
        user = instaloader.Profile.from_username(self.L.context, username=username)
        if user.is_private:
            raise PrivateAccountException()
        return user

    async def get_post(self, post_id):
        post = instaloader.Post.from_shortcode(self.L.context, post_id)
        return post

    async def get_user_story(self, story_id, username):
        user = await self.get_user(username)
        for story in self.L.get_stories([user.userid]):
            for item in story.get_items():
                if item.mediaid == int(story_id):
                    self.L.download_storyitem(item, 'media')
                    return {
                        "is_video": item.is_video,
                        "author": username,
                        "thumbnail": item.video_url,
                        "image_url": item.url,
                        "shortcode": item.shortcode
                    }


downloader = InstagramDownloader(
    config.IG_USERNAME,
    config.IG_PASSWORD
)