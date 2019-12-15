# -*- coding: utf-8 -*-

import json
import time
import base64
import logging

import urllib
from .handler import Handler
from ..conf import setting
from ..util import util
from ..util.request import RemoteRequest


class SearchArticleHandler(Handler):
    def __init__(self):
        super(SearchArticleHandler, self).__init__()
        self.request = RemoteRequest()
        self.url = setting.search_url

    def process(self, message):
        if not message.is_at:
            return message

        answer = self.replyMsg(message)

        time.sleep(1)
        message.reply_msg(answer)

        return message

    def replyMsg(self, message):
        url = self.url.format(urllib.parse.quote(message.text))
        logging.info(url)
        response = self.request.get(url)
        idx = 0
        articles = []
        try:
            response = json.loads(response)
            for article in response['data']['search']:
                articles.append({
                    'title': util.nohighlight(article['title']),
                    'url': self.short(
                        setting.article_url.
                        format(article['article_id']))
                })
                idx += 1
                if idx >= 3:
                    break
        except Exception:
            logging.error(
                    'search article for question [{}] fail'.
                    format(message.text))
            logging.error(response)
            return setting.no_answer

        if not idx:
            return setting.no_answer

        answer = setting.answer_template.format(
                len(articles), self.answerTemplate(articles))
        return answer

    def answerTemplate(self, articles):
        phrases = []
        for idx, article in enumerate(articles):
            phrases.append(
                    '{}、 {} {}'.
                    format(idx+1, article['title'], article['url']))
        return '\n\n'.join(phrases)

    def short(self, uri):
        return uri

        data = {
            'url': base64.b64encode(uri.encode('utf-8')),
            'from': 'w',
            'site': '1t.click'
        }
        # self.request.update_header(setting.dwz_header)
        url = (setting.short_service +
               '?url={}&from={}&site={}'.format(
                   data['url'].decode('utf-8'), data['from'], data['site']))
        response = self.request.get(url)
        try:
            response = json.load(response)
            return response['data']['short_url']
        except Exception:
            logging.error(url)
            logging.error(response)
            return uri
