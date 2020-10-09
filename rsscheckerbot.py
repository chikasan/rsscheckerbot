import os
from logging import getLogger, StreamHandler, DEBUG, Formatter

import discord
from discord.ext import commands


class RssCheckerBot(commands.Bot):
    """RSS更新通知Bot

    Args:
        commands (commands.Bot): Botの親クラス
    """

    def __init__(self, logger, intents):
        super().__init__(command_prefix='%',
                         intents=intents)
        self.load_extension('rss')
        self.logger = logger

    def run(self, token):
        super().run(token)

    async def on_ready(self):
        self.logger.info('Bot起動しました')


if __name__ == '__main__':
    logger = getLogger('rsschecklog')
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    formatter = Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    intents = discord.Intents.all()
    client = RssCheckerBot(logger, intents)

    TOKEN = os.environ['TOKEN']

    try:
        client.loop.run_until_complete(client.start(TOKEN))
    except KeyboardInterrupt:
        client.loop.run_until_complete(client.close())
