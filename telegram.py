from abc import ABC

import setting
from requests import post
from pytz import timezone
from datetime import datetime
import hashlib
from os import path
from pandas import to_datetime
from html.parser import HTMLParser
from re import sub
from os import environ

HOME = environ.get('NEWSFEED_HOME', '.') + '/'
posted_log = HOME+'logs/posted.log'


def send_to_telegram(text_json):
    is_post, md5 = _is_posted(text_json.get('title', ''))
    if is_post:
        return {'posted': True}
    text_json = pre_handle_message(text_json)
    text = _format_message(text_json)
    send_api = f'https://api.telegram.org/bot{setting.SecBlogBot}/sendMessage'
    post_data = {
        'chat_id': setting.bot_chat_id,
        'text': text,
        'parse_mode': 'html'
    }
    response = post(send_api, data=post_data)
    if response.json().get('ok', False):
        _update_log(md5)
        return response.json()
    err = response.json()
    err['content'] = text
    return err 


def _format_message(text_json):
    published = to_datetime(text_json.get('published', datetime.now()))
    published = published.replace(tzinfo=timezone('Asia/Ho_Chi_Minh'))
    published = published.strftime('%a, %d %b %Y')
    return f'''
[{published}] <b>{text_json.get('provider', '')} - {text_json.get('title', {})}</b>  <a href="{text_json.get('link', {})}">see more ...</a>
'''


def _is_posted(title):
    if not path.exists(posted_log):
        open(posted_log, 'w+').close()
    md5 = hashlib.md5(title.encode("utf-8")).hexdigest()
    if md5 in open(posted_log, 'r+').read():
        return True, None
    return False, md5


def _update_log(md5):
    open(posted_log, 'a+').write(md5 + '\n')


class MLStripper(HTMLParser, ABC):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def _strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def _strip_special_char(before):
    temp = sub('^[^\w]+', '', before)
    after = sub('[=<>/]+', '', temp)
    return after

def pre_handle_message(text_json):
    title = text_json.get('title', '')
    summary = text_json.get('summary', '')
    # Escape HTML tags
    summary = _strip_tags(summary)
    summary = _strip_special_char(title)

    title = _strip_tags(title)
    title = _strip_special_char(title)

    # Beauty
    text_json['summary'] = summary[:270]
    text_json['title'] = title
    return text_json
