import asyncio
import re

from aiogram.types import Message, InputFile, InputMedia, MediaGroup
from aiogram.utils.exceptions import BadRequest

from docs import config
from tgbot.setup import dp, bot
from instaloader import BadResponseException
from insta_downloader.core.exceptions import PrivateAccountException
from insta_downloader.instagram import downloader
from tgbot.utils.models import Video


@dp.message_handler(regexp=config.ig_regexp)
async def instagram_handler(message: Message):
    msg_to_delete = await message.reply("downloading")

    mobj = re.match(config.ig_regexp, message.text)
    post_id = mobj.group('id')

    try:
        post = await downloader.get_post(post_id)
    except (PrivateAccountException, BadResponseException) as ex:
        await message.reply(PrivateAccountException().message)
        await msg_to_delete.delete()
        raise ex
    except Exception as ex:
        await message.reply("exception")
        await msg_to_delete.delete()
        raise ex

    sidecar_items = []
    if post.typename == 'GraphSidecar':
        for item in post.get_sidecar_nodes():
            sidecar_items.append(item)

    video_name = f"{config.MEDIA_DIR}/{post.shortcode}_ig.mp4"
    caption = post.caption
    owner_username = post.owner_username
    typename = post.typename
    image_url = post.url

    text = f"<b>{owner_username}</b>: {caption}\n\n"

    if typename == 'GraphSidecar':
        await downloader.download_post(post_id)

        media_group = [
            InputMedia(media=InputFile(
                path_or_bytesio=f'{config.MEDIA_DIR}/{post.shortcode}_ig_{i+1}.{"mp4" if v.is_video else "jpg"}'),
                type='video' if v.is_video else 'photo',
                caption=text if i == 0 else None) for i,v in enumerate(sidecar_items)
        ]
        await message.reply_media_group(media_group)

    else:
        try:
            video = await Video.get_video_by_url(message.text)
            file = video.file_id_in_tg
        except Exception as ex:
            await downloader.download_post(post_id)

            file = InputFile(path_or_bytesio=video_name)

        if post.is_video:
            try:
                send_video = await message.reply_video(
                    file,
                    caption=text
                )
                # записываем в базу этот видос
                asyncio.create_task(Video.add_video(
                    file_id=video_name,
                    file_id_in_tg=send_video.video.file_id,
                    url=message.text
                ))
            except BadRequest:
                # если у него bad request - значит не смог скачать картинку видео, отправляем все что есть
                await message.reply(text=text)
        else:
            await message.reply_photo(image_url, caption)

    await msg_to_delete.delete()


@dp.message_handler(regexp=config.ig_video_stories)
async def instagram_stories(message: Message):
    msg_to_delete = await message.reply("downloading")

    stories = re.match(config.ig_video_stories, message.text)

    username = stories.group('username')
    story_id = stories.group('id')

    try:
        meta_info = await downloader.get_user_story(story_id=story_id, username=username)
    except (PrivateAccountException, BadResponseException) as ex:
        await message.reply(PrivateAccountException().message)
        await msg_to_delete.delete()
        raise ex

    short_code = meta_info.get('shortcode')
    author = meta_info.get('author')

    name = f'media/{short_code}_ig.jpg'

    if meta_info.get('is_video'):
        # отправляем юзеру данные о фото
        name = f'media/{short_code}_ig.mp4'
        await message.reply_video(InputFile(path_or_bytesio=name), caption=f'{author} \n\n' + "downloadedwith")
    else:
        await message.reply_photo(InputFile(path_or_bytesio=name), caption=f'{author} \n\n' + "downloadedwith")

    await msg_to_delete.delete()
