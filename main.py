import rss_provider
import telegram

if __name__ == '__main__':
    news_feed = rss_provider.rss_fetch()
    for feed in news_feed:
        print(telegram.send_to_telegram(feed))