import setting
from feedparser import parse


def rss_fetch():
    results = []
    for provider, rss in setting.__providers__.items():
        news_feed = parse(rss)
        for entry in news_feed.entries:
            results.append({
                'provider': provider,
                'title': entry.title,
                'summary': entry.summary,
                'link': entry.link,
                'published': entry.get('published', entry.get('updated_date', '')),
            })
    return results
