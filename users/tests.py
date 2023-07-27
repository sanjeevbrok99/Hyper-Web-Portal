from django.test import Client
import urllib3

client = Client()
response = client.post(urllib3, content_type='application/json')