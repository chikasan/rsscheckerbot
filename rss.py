from datetime import datetime
from time import mktime
from logging import getLogger
import traceback

from discord.ext import commands, tasks
import feedparser
from ruamel import yaml


class RssChecker(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.logger = getLogger('rsschecklog')
        with open('config.yaml', 'r') as stream:
            self.yaml_data = yaml.safe_load(stream)
        self.channel_id = self.yaml_data['channel']
        self.checker.start()

    def cog_unload(self):
        self.checker.cancel()

    async def sendmessage(self, message):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send(message)
        else:
            self.logger.info('書き込みチャンネルが見つかりません')

    @tasks.loop(seconds=3600)
    async def checker(self):
        try:
            for url in self.yaml_data['account']:
                self.logger.info('url: ' + url['url'] + ' の確認')
                d = feedparser.parse(url['url'])

                if d.bozo == 1:
                    self.logger.info('Error: RSSの取得に失敗しました。')
                    self.logger.info(d.bozo_exception)
                    await self.sendmessage(url['url'] + ' の取得に失敗しました。'
                                           + d.bozo_exception)
                    continue

                last_call = datetime.fromisoformat(url['lastupdated'])
                last_updated = datetime.fromtimestamp(
                    mktime(d.updated_parsed) + 3600*9)

                if last_updated > last_call:
                    self.logger.info('最終更新:' + d['updated'] + ' 更新があります')
                    for entries in reversed(d['entries']):
                        update = datetime.fromtimestamp(
                            mktime(entries.updated_parsed) + 3600*9)
                        if update > last_call:
                            message = (entries['title'] + ' '
                                       + entries['updated'] + ' '
                                       + entries['link'])
                            await self.sendmessage(message)
                    url['lastupdated'] = last_updated.isoformat()
                    with open('config.yaml', 'w') as stream:
                        yaml.dump(self.yaml_data, stream=stream)
                else:
                    self.logger.info('最終更新:' + d['updated'] + ' 更新はありません')
        except AttributeError:
            message = '要素参照エラーが発生しました。エラーログを確認してください。'
            self.logger.info(message)
            print(traceback.format_exc())
            await self.sendmessage(message)
        except Exception:
            message = '処理中に問題が発生しました。エラーログを確認してください。'
            self.logger.info(message)
            print(traceback.format_exc())
            await self.sendmessage(message)

    @checker.before_loop
    async def before_checker(self):
        self.logger.info('waiting...')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(RssChecker(bot))
