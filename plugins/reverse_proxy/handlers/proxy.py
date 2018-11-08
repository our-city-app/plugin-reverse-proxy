# -*- coding: utf-8 -*-
# Copyright 2018 Mobicage NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @@license_version:1.5@@

import httplib
import logging
import urllib

import webapp2
from google.appengine.api import urlfetch
from plugins.reverse_proxy.models import ProxyPath


class ReverseProxyHandler(webapp2.RequestHandler):
    def _handle_request(self, kwargs):
        """
        Proxies a request to another server while first checking/refreshing authentication
        When issuing a request to another App Engine app, your App Engine app must assert its identity by adding the header
         X-Appengine-Inbound-Appid to the request. If you instruct the URL Fetch service to not follow redirects, App
         Engine will add this header to requests automatically.
        Args:
            url (unicode)
            request (webapp2.Request)
            response (webapp2.Response)
        """
        name = kwargs.get('name')
        proxy_path = ProxyPath.create_key(name).get()
        if not proxy_path:
            logging.info('Unknown proxy %s' % name)
            self.abort(404)
        url = proxy_path.url + kwargs.get('route')
        request = self.request
        headers = request.headers
        content = None
        if 'Cookie' in headers:
            del headers['Cookie']
        if 'Host' in headers:
            del headers['Host']
        if 'Content-Length' in headers:
            del headers['Content-Length']
        logging.info('Proxying request to %s\nHeaders:%s\nData:%s', url, headers, request.body)
        try:
            query_params = urllib.urlencode(request.GET)
            if query_params:
                url = '%s?%s' % (url, query_params)
            result = urlfetch.fetch(url, request.body, request.method, headers, deadline=30, follow_redirects=False)
            status_code, content, headers = result.status_code, result.content, result.headers
        except urlfetch.DeadlineExceededError:
            # Took more than 30 seconds
            status_code = httplib.GATEWAY_TIMEOUT
        except urlfetch.DownloadError as error:
            # server down/unreachable
            logging.error(error)
            status_code = httplib.BAD_GATEWAY
        except urlfetch.Error as error:
            logging.error(error)
            status_code = httplib.INTERNAL_SERVER_ERROR
        self.response.headers = headers
        self.response.set_status(status_code)
        if content:
            self.response.out.write(content)
        if headers.get('Content-Type', '').lower() == 'application/json':
            logged_content = content
        else:
            logged_content = '[%s content omitted]' % headers.get('Content-Type', '') if content else None
        logging.info('Response: %s\nHeaders: %s\nContent: %s', status_code, headers, logged_content)

    def get(self, *args, **kwargs):
        self._handle_request(kwargs)

    def post(self, *args, **kwargs):
        self._handle_request(kwargs)

    def put(self, *args, **kwargs):
        self._handle_request(kwargs)

    def delete(self, *args, **kwargs):
        self._handle_request(kwargs)

    def patch(self, *args, **kwargs):
        self._handle_request(kwargs)

    def head(self, *args, **kwargs):
        self._handle_request(kwargs)

