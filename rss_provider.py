import setting
from feedparser import parse
from Logger import Logger
from datetime import datetime
from main import Static

def rss_fetch():
    logger = Logger()
    results = []
    excludes = ['jira']
    for provider, rss in setting.__providers_newsfeed__.items():
        news_feed = parse(rss)
        for entry in news_feed.entries:
            try:
                published = entry.get('published',
                                entry.get('updated_date', 
                                    entry.get('updated',
                                          entry.get('pubDate', datetime.now())
                                    )
                                )
                            )
                results.append({
                    'provider': provider,
                    'title': entry.title,
                    'summary': entry.summary if entry.summary.lower() not in excludes else 'SPAM',
                    'link': entry.link,
                    'published': published,
                })
            except Exception as e:
                logger.error.error(e)
                if Static.DEBUG: print(e)
                continue
    return results
