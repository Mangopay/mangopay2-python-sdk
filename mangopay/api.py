# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import requests
import time
import logging
import six
import copy
import mangopay
from mangopay.ratelimit import RateLimit


from mangopay.auth import AuthorizationTokenManager
from .exceptions import APIError, DecodeError
from .signals import request_finished, request_started, request_error
from .utils import reraise_as, truncatechars

from requests.exceptions import ConnectionError, ConnectTimeout, Timeout

try:
    import urllib.parse as urlrequest
except ImportError:
    import urllib as urlrequest

try:
    import simplejson as json
except ImportError:
    import json


logger = logging.getLogger('mangopay')

requests_session = requests.Session()
rate_limits = None

class APIRequest(object):


    def __init__(self, client_id=None, apikey=None, api_url=None, api_sandbox_url=None, sandbox=None,
                 timeout=30.0, storage_strategy=None, proxies=None):
        global rate_limits
        rate_limits = None
        if (sandbox is None and mangopay.sandbox) or sandbox:
            self.api_url = api_sandbox_url or mangopay.api_sandbox_url
        else:
            self.api_url = api_url or mangopay.api_url

        self.client_id = client_id or mangopay.client_id
        self.apikey = apikey or mangopay.apikey
        self.auth_manager = AuthorizationTokenManager(self, storage_strategy)
        self.timeout = timeout
        self.proxies = proxies

    def set_rate_limit(self, rate_limit):
        global rate_limits
        rate_limits = rate_limit


    def get_rate_limits(self):
        return rate_limits

    def request(self, method, url, data=None, idempotency_key=None, oauth_request=False, without_client_id=False, **params):
        return self.custom_request(method, url, data, idempotency_key, oauth_request, True, without_client_id, **params)

    def custom_request(self, method, url, data=None, idempotency_key=None, oauth_request=False,
                       is_mangopay_request=False, without_client_id=False, **params):
        params = params or {}

        headers = {}

        if is_mangopay_request:
            headers['User-Agent'] = 'MangoPay V2 Python/' + str(mangopay.package_version)
            if oauth_request:
                headers['Authorization'] = self.auth_manager.basic_token()
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
            else:
                headers['Authorization'] = self.auth_manager.get_token()
                headers['Content-Type'] = 'application/json'

            if idempotency_key:
                headers['Idempotency-Key'] = idempotency_key
        else:
            if "data_XXX" in params:
                params[str("data")] = params[str("data_XXX")]
                params.__delitem__(str("data_XXX"))
                headers['Content-Type'] = 'application/x-www-form-urlencoded'

        truncated_data = None

        encoded_params = urlrequest.urlencode(params)

        if is_mangopay_request:
            if oauth_request or without_client_id:
                url = self.api_url + url
            else:
                url = self._absolute_url(url, encoded_params)
        else:
            url = '%s?%s' % (url, encoded_params)

        if data or data == {}:
            truncated_data = truncatechars(copy.copy(data))

            data = json.dumps(data, default=lambda x: x.to_api_json())

        logger.debug('DATA[IN -> %s]\n\t- headers: %s\n\t- content: %s', url, headers, truncated_data)

        ts = time.time()

        # signal:
        request_started.send(url=url, data=truncated_data, headers=headers, method=method)

        try:
            result = requests_session.request(method, url,
                                              data=data,
                                              headers=headers,
                                              timeout=self.timeout,
                                              proxies=self.proxies)
        except ConnectionError as e:
            msg = '{}'.format(e)

            if msg:
                msg = '%s: %s' % (type(e).__name__, msg)
            else:
                msg = type(e).__name__

            reraise_as(APIError(msg))

        except Timeout as e:
            msg = '{}'.format(e)

            if msg:
                msg = '%s: %s' % (type(e).__name__, msg)
            else:
                msg = type(e).__name__

            reraise_as(APIError(msg))
        laps = time.time() - ts

        # signal:
        request_finished.send(url=url,
                              data=truncated_data,
                              headers=headers,
                              method=method,
                              result=result,
                              laps=laps)

        logger.debug('DATA[OUT -> %s][%2.3f seconds]\n\t- status_code: %s\n\t- headers: %s\n\t- content: %s',
            url,
            laps,
            result.status_code,
            result.headers,
            result.text if hasattr(result, 'text') else result.content
        )

        self.read_response_headers(result.headers)

        if result.status_code not in (requests.codes.ok, requests.codes.not_found,
                                      requests.codes.created, requests.codes.accepted,
                                      requests.codes.no_content):
            self._create_apierror(result, url=url, data=truncated_data, method=method)
        elif result.status_code == requests.codes.no_content:
            return result, None
        else:
            if result.content:
                try:
                    content = result.content

                    if six.PY3:
                        content = content.decode('utf-8')

                    return result, json.loads(content)
                except ValueError:
                    if result.content.startswith(b'data='):
                        return result.content
                    self._create_decodeerror(result, url=url)
            else:
                self._create_decodeerror(result, url=url)

    def init_rate_limits(self):
        rate_limits = [RateLimit(15), RateLimit(30), RateLimit(60), RateLimit(24 * 60)]
        return rate_limits

    def read_response_headers(self, headers):
        update_rate_limits = None

        for k, v in headers.items():
            lower_case_header = k.lower()
            if lower_case_header == "x-ratelimit-remaining":
                if update_rate_limits is None:
                    update_rate_limits = self.init_rate_limits()
                calls_remaining = list(eval(v))
                update_rate_limits[0].calls_remaining = int(calls_remaining[3])
                update_rate_limits[1].calls_remaining = int(calls_remaining[2])
                update_rate_limits[2].calls_remaining = int(calls_remaining[1])
                update_rate_limits[3].calls_remaining = int(calls_remaining[0])

            if lower_case_header == "x-ratelimit":
                if update_rate_limits is None:
                    update_rate_limits = self.init_rate_limits()
                calls_made = list(eval(v))
                update_rate_limits[0].calls_made = int(calls_made[3])
                update_rate_limits[1].calls_made = int(calls_made[2])
                update_rate_limits[2].calls_made = int(calls_made[1])
                update_rate_limits[3].calls_made = int(calls_made[0])

            if lower_case_header == "x-ratelimit-reset":
                if update_rate_limits is None:
                    update_rate_limits = self.init_rate_limits()
                reset_times = list(eval(v))
                update_rate_limits[0].reset_time_millis = int(reset_times[3])
                update_rate_limits[1].reset_time_millis = int(reset_times[2])
                update_rate_limits[2].reset_time_millis = int(reset_times[1])
                update_rate_limits[3].reset_time_millis = int(reset_times[0])

        if update_rate_limits is not None:
            self.set_rate_limit(update_rate_limits)

    def _absolute_url(self, url, encoded_params):
        pattern = '%s%s%s'

        if encoded_params:
            pattern = '%s%s?%s'

        return pattern % (self.api_url, self._construct_api_url(url), encoded_params)

    def _construct_api_url(self, relative_url):
        return '%s%s' % (self.client_id, relative_url)

    def _create_apierror(self, result, url=None, data=None, method=None):
        text = result.text if hasattr(result, 'text') else result.content

        status_code = result.status_code

        headers = result.headers

        logger.error('API ERROR: status_code: %s | url: %s | method: %s | data: %r | headers: %s | content: %s',
            status_code,
            url,
            method,
            data,
            headers,
            text,
        )

        request_error.send(url=url, status_code=status_code, headers=headers)

        try:
            content = result.json()
        except ValueError:
            content = None

        raise APIError(text, code=status_code, content=content, headers=headers)

    def _create_decodeerror(self, result, url=None):

        text = result.text if hasattr(result, 'text') else result.content

        status_code = result.status_code

        headers = result.headers

        logger.error('DECODE ERROR: status_code: %s | headers: %s | content: %s',
            status_code,
            headers,
            text,
        )

        request_error.send(url=url, status_code=status_code, headers=headers)

        try:
            content = result.json()
        except ValueError:
            content = None

        raise DecodeError(text,
                          code=status_code,
                          headers=headers,
                          content=content)
