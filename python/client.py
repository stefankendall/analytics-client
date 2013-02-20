import json
import requests
import grequests


class Client(object):
    api_url = 'URL_HERE'

    def __init__(self, api_key, website_id, async=False):
        self.api_key = api_key
        self.website_id = website_id
        self.async = async

    def add_event(self, collection_name, data):
        url = '{0}/collection/'.format(self.api_url)
        request_data = {
            'api_key': self.api_key,
            'website': self.website_id,
            'event': json.dumps(data),
            'collection': collection_name
        }
        headers = {
            'content-type': 'application/json'
        }

        # If do not specify that we want async calls, use requests
        # Otherwise, fancy gevent + requests lib
        if not self.async:
            r = requests.put(url, data=request_data, headers=headers)

            if r.status_code != requests.codes.ok:
                r.raise_for_status()
        else:
            urls = [url]
            request_set = (grequests.put(url, data=request_data, headers=headers) for url in urls)
            grequests.map(request_set)
