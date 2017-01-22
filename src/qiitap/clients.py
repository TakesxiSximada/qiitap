import os
import json
import logging
import requests

from .environs import QiitapEnviron
from .exc import (
    NoTokenError,
    QiitaAPIError,
)

logger = logging.getLogger(__name__)


def get_client():
    environ = QiitapEnviron()
    return QiitaClient(environ.token, environ.host)


class QiitaClient(object):
    def __init__(self, token, host):
        self.token = token
        self.host = host

    @property
    def headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json',
        }

    def create(self, article):
        url = self.host + '/api/v2/items/'
        res = requests.post(url, data=article.payload_str, headers=self.headers)
        if res.status_code not in (200, 201):
            raise QiitaAPIError('Qiita Create API Failed: code={}, reason={}, body={}'.format(
                res.status_code, res.reason, res.content,
            ))

        data = json.loads(res.content)
        article.item_id = data['id']
        article.url = data['url']
        return article

    def update(self, article):
        url = self.host + '/api/v2/items/{}'.format(article.item_id)
        res = requests.patch(url, data=article.payload_str, headers=self.headers)

        if res.status_code != 200:
            raise QiitaAPIError('Qiita Update API Failed: code={}, reason={}, body={}'.format(
                res.status_code, res.reason, res.content,
            ))
        data = res.json()
        article.url = data['url']
        return article
