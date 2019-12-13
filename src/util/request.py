# coding: utf-8

import time
import requests
from .util import logit


class RemoteRequest():
    def __init__(
            self, method='GET', headers={},
            timeout=10, retry=2, proxys=None, cookie_url=None):
        self.retry = retry
        self.method = method
        self.headers = headers
        self.timeout = timeout
        self.proxys = proxys
        self.cookie_url = cookie_url

    def update_header(self, header):
        self.headers.update(header)

    def get(self, url, data={}):
        return self.request(url, fn=requests.get, data=data)

    def post(self, url, data={}):
        return self.request(url, fn=requests.post, data=data)

    @logit
    def request(self, url, fn, data):
        retry = self.retry
        while retry:
            try:
                retry -= 1
                response = fn(
                    url,
                    data=data,
                    timeout=self.timeout,
                    allow_redirects=False,
                    headers=self.headers)
                response.raise_for_status()

                return response.text
            except Exception:
                time.sleep(2)
                if not retry:
                    raise
