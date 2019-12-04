import setting
from feedparser import parse
from Logger import Logger


def rss_fetch():
    logger = Logger()
    results = []
    excludes = ['jira']
    for provider, rss in setting.__providers_newsfeed__.items():
        news_feed = parse(rss)
        for entry in news_feed.entries:
            try:
                results.append({
                    'provider': provider,
                    'title': entry.title,
                    'summary': entry.summary if entry.summary.lower() not in excludes else 'SPAM',
                    'link': entry.link,
                    'published': entry.get('published', entry.get('updated_date', '')),
                })
            except Exception as e:
                logger.error.error(e)
                continue
    return results
