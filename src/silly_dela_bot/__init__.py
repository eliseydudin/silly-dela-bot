import mastodon
import telebot
import telebot.types as tp
from .config import Config


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

    def on_photo(self, message: tp.Message):
        photo = message.photo[-1]
        file_id = photo.file_id
        file = self.bot.get_file(file_id)
        photo_bytes = self.bot.download_file(file.file_path)

        photo_id = self.mastodon_instance.media_post(
            media_file=photo_bytes, mime_type="image/jpeg"
        )

        self.mastodon_instance.status_post(
            status=message.caption or "", media_ids=photo_id["id"]
        )

    def run(self):
        self.bot.infinity_polling()


def main() -> None:
    config = Config()
    client = Client(config)
    client.run()
