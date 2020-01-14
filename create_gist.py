# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

# https://developer.github.com/v3/gists/#create-a-gist

import os
import sys
import requests
import json

GITHUB_TOKEN = os.environ.get('JEKYLL_GITHUB_TOKEN', None)
if not GITHUB_TOKEN:
    sys.exit('Missing Github token')

API_URL = 'https://api.github.com/gists'
ARTICLE_URL = 'https://apiraino.github.io/posts'
ARTICLE_LINK = sys.argv[1]

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'Bearer {}'.format(GITHUB_TOKEN)
}

payload = {
    'description': 'Comments for {}/{}'.format(ARTICLE_URL,ARTICLE_LINK),
    'public': False,
    'files': {
        ARTICLE_LINK: {
            'content': 'Comments for {}/{}'.format(
                ARTICLE_URL,ARTICLE_LINK
            )
        }
    }
}

resp = requests.post(API_URL, headers=headers, data=json.dumps(payload))
if resp.status_code // 100 != 2:
    print(payload)
    sys.exit('Gist creation failed: {}'.format(resp.content))

gist_id = resp.json()['id']
print(gist_id)
