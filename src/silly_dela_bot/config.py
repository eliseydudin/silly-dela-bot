import toml


class Config:
    def __init__(self):
        contents = toml.load("config.toml")
        self.MASTODON_ACCESS_TOKEN = str(contents["mastodon_access_token"])
        self.MASTODON_INSTANCE = str(contents["mastodon_instance"])
        self.TELEGRAM_BOT_TOKEN = str(contents["telegram_bot_token"])
        self.GEMINI_TOKEN = str(contents["gemini_api_token"])
