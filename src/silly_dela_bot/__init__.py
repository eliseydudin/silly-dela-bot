import mastodon
import telebot
import telebot.types as tp
from .config import Config
import time
import datetime


def get_hashtags():
    HASHTAGS = "#cat #cats #mastocats"
    if datetime.datetime.today().weekday() == 5:
        return HASHTAGS + " #caturday"
    else:
        return HASHTAGS


class Client:
    def __init__(self, config: Config):
        self.mastodon_instance = mastodon.Mastodon(
            access_token=config.MASTODON_ACCESS_TOKEN,
            api_base_url=config.MASTODON_INSTANCE,
        )

        self.bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
        self.on_photo = self.bot.channel_post_handler(content_types=["photo"])(
            self.on_photo
        )
        self.on_video = self.bot.channel_post_handler(content_types=["video"])(
            self.on_video
        )

    def on_photo(self, message: tp.Message):
        photo = message.photo[-1]
        file_id = photo.file_id
        file = self.bot.get_file(file_id)
        photo_bytes = self.bot.download_file(file.file_path)

        photo_id = self.mastodon_instance.media_post(
            media_file=photo_bytes, mime_type="image/jpeg"
        )

        if message.caption is None:
            caption = get_hashtags()
        else:
            caption = f"{message.caption} {get_hashtags()}"
        status = self.mastodon_instance.status_post(
            status=caption, media_ids=photo_id["id"]
        )

        self.mastodon_instance.status_favourite(status)
        self.mastodon_instance.status_reblog(status)

    def on_video(self, message: tp.Message):
        file = self.bot.get_file(message.video.file_id)
        video_bytes = self.bot.download_file(file.file_path)
        video_id = self.mastodon_instance.media_post(
            media_file=video_bytes, mime_type=message.video.mime_type or "video/mp4"
        )

        time.sleep(60.0)  # for some reason mastodon takes some time to upload stuff :/

        if message.caption is None:
            caption = get_hashtags()
        else:
            caption = f"{message.caption} {get_hashtags()}"
        status = self.mastodon_instance.status_post(
            status=caption, media_ids=video_id["id"]
        )

        self.mastodon_instance.status_favourite(status)
        self.mastodon_instance.status_reblog(status)

    def run(self):
        self.bot.infinity_polling()


def main() -> None:
    config = Config()
    client = Client(config)
    client.run()
