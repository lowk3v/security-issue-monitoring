import rss_provider
import telegram
from Logger import Logger

if __name__ == '__main__':
    news_feed = rss_provider.rss_fetch()
    for feed in news_feed:
        result = telegram.send_to_telegram(feed)
        # Logger.logger.info(result)
        print(result)
