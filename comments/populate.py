import sys, os
sys.path.append('/Users/kamal/code/django/nis_comments')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nis_comments.settings'
from django.conf import settings

from comments.models import News
import json

FILENAME = "/Users/kamal/code/nis_json_data.txt"
nis_json_data = open(FILENAME).read().replace('while(1);','')
parsed_data = json.loads(nis_json_data)

news = parsed_data['pages']

for n in news:
    News(news_id = n['bottomNewsId'], author = n['author']['name'], text = n['content']).save()
