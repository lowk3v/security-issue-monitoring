#!/root/kev/security-issue-monitoring/venv/bin/python3.7

import rss_provider
import telegram
from Logger import Logger
import sys

logger = Logger()

class Static:
    DEBUG = False

if 'debug' in sys.argv:
    Static.DEBUG = True

if __name__ == '__main__':
    news_feed = rss_provider.rss_fetch()
    for feed in news_feed:
        result = telegram.send_to_telegram(feed)
        if result.get('posted', False):
            pass
        if not result.get('ok', False):
            logger.access.info(result.get('content',''))
        if Static.DEBUG: print(result)
    if Static.DEBUG: print(f'Count news feed: {len(news_feed)}')
