import rss_provider
import telegram
from Logger import Logger

logger = Logger()

if __name__ == '__main__':
    news_feed = rss_provider.rss_fetch()
    for feed in news_feed:
        result = telegram.send_to_telegram(feed)
        logger.access.info(result)
        print(result)

