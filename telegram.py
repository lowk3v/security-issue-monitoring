import setting
from requests import post
import pytz
from datetime import datetime
import hashlib
from os import path
from pandas import to_datetime
from re import findall, sub


def format_message(text_json):
    published = to_datetime(text_json.get('published', datetime.now()))
    published = published.replace(tzinfo=pytz.timezone('Asia/Ho_Chi_Minh'))
    published = published.strftime('%a, %d %b %Y')
    return f'''
---
\[{published}] ___{text_json.get('provider', '')}___: `{text_json.get('title', {})}`
{text_json.get('summary', '')}
[see more ...]({text_json.get('link', {})})
'''


def send_to_telegram(text_json):
    is_post, md5 = is_posted(text_json.get('title', ''))
    if is_post:
        return {}
    text_json = pre_handle_message(text_json)
    text = format_message(text_json)
    send_api = f'https://api.telegram.org/bot{setting.SecBlogBot}/sendMessage'
    post_data = {
        'chat_id': setting.bot_chat_id,
        'text': text,
        'parse_mode': 'markdown'
    }
    response = post(send_api, data=post_data)
    if response.json().get('ok', False):
        update_log(md5)
    else:
        print(text)
    return response.json()


def is_posted(title):
    if not path.exists('posted.log'):
        open('posted.log', 'w+').close()
    md5 = hashlib.md5(title.encode("utf-8")).hexdigest()
    if md5 in open('posted.log', 'r+').read():
        return True, None
    return False, md5


def update_log(md5):
    open('posted.log', 'a+').write(md5 + '\n')


def pre_handle_message(text_json):
    summary = text_json.get('summary', '')
    if text_json.get('provider', '') == 'Code White Sec':
        try:
            summary = findall('<p>([^<]+)', summary)[0]
        except: pass
    summary = sub(r'(<[\w]+[^//]+/>|<a[^>]+>[^<]*</a>)', '', summary)
    text_json['summary'] = summary[:270] + ' ...'
    return text_json
