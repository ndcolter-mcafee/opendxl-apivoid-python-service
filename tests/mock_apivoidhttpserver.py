import socket

try: #Python 3
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import urllib.parse as urlparse
except ImportError: #Python 2.7
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    import urlparse

from threading import Thread

import requests

from dxlbootstrap.util import MessageUtils
from dxlapivoidservice import ApiVoidService
from dxlapivoidservice.requesthandlers import ApiVoidCallback
from tests.test_value_constants import *

TEST_FOLDER = str(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"))
MOCK_EPOHTTPSERVER_CERTNAME = TEST_FOLDER + "/client.crt"
MOCK_EPOHTTPSERVER_KEYNAME = TEST_FOLDER + "/client.key"


def get_free_port():
    stream_socket = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    stream_socket.bind(('localhost', 0))
    address, port = stream_socket.getsockname()
    stream_socket.close()

    return address, port


class MockApiVoidServerRequestHandler(SimpleHTTPRequestHandler):

    KEY_PATTERN = "key={0}"
    BASE_PATTERN = "{0}/v1/pay-as-you-go/?" + \
                   KEY_PATTERN.format(SAMPLE_API_KEY) + \
                   "{1}"

    IP_REP_PATTERN = BASE_PATTERN.format(
        ApiVoidService.CMD_IP_REPUTATION,
        "&" + ApiVoidCallback.PARAM_IP + "=" + SAMPLE_IP
    )

    DOMAIN_REP_PATTERN = BASE_PATTERN.format(
        ApiVoidService.CMD_DOMAIN_REPUTATION,
        "&" + ApiVoidCallback.PARAM_HOST + "=" + SAMPLE_HOST
    )

    DNS_LOOKUP_PATTERN = BASE_PATTERN.format(
        ApiVoidService.CMD_DNS_LOOKUP,
        "&" + ApiVoidCallback.PARAM_ACTION + "=" + SAMPLE_ACTION + \
        "&" + ApiVoidCallback.PARAM_HOST + "=" + SAMPLE_HOST
    )

    SSL_INFO_PATTERN = BASE_PATTERN.format(
        ApiVoidService.CMD_SSL_INFO,
        "&" + ApiVoidCallback.PARAM_HOST + "=" + SAMPLE_HOST
    )

    THREATLOG_PATTERN = BASE_PATTERN.format(
        ApiVoidService.CMD_THREATLOG,
        "&" + ApiVoidCallback.PARAM_HOST + "=" + SAMPLE_HOST
    )

    EMAIL_VERIFY_PATTERN = BASE_PATTERN.format(
        ApiVoidService.CMD_EMAIL_VERIFY,
        "&" + ApiVoidCallback.PARAM_HOST + "=" + SAMPLE_HOST
    )

    DOMAIN_AGE_PATTERN = BASE_PATTERN.format(
        ApiVoidService.CMD_DOMAIN_AGE,
        "&" + ApiVoidCallback.PARAM_HOST + "=" + SAMPLE_HOST
    )

    PARKED_DOMAIN_PATTERN = BASE_PATTERN.format(
        ApiVoidService.CMD_PARKED_DOMAIN,
        "&" + ApiVoidCallback.PARAM_HOST + "=" + SAMPLE_HOST
    )

    STATS_PATTERN = "stats"

    def do_GET(self):

        response_code = requests.codes.ok #pylint: disable=no-member

        parsed_url = urlparse.urlparse(self.path)
        parsed_query = urlparse.parse_qs(parsed_url.query, keep_blank_values=True)
        parsed_api_key = parsed_query["key"][0]

        if parsed_api_key == SAMPLE_API_KEY:
            if self.STATS_PATTERN in parsed_query:
                response_content = self.stats_remained_cmd()
            elif self.IP_REP_PATTERN in self.path:
                response_content = self.ip_rep_cmd(self, parsed_url)
            elif self.DOMAIN_REP_PATTERN in self.path:
                response_content = self.domain_rep_cmd(self, parsed_url)
            elif self.DNS_LOOKUP_PATTERN in self.path:
                response_content = self.dns_lookup_cmd(self, parsed_url)
            elif self.SSL_INFO_PATTERN in self.path:
                response_content = self.ssl_info_cmd(self, parsed_url)
            elif self.THREATLOG_PATTERN in self.path:
                response_content = self.threatlog_cmd(self, parsed_url)
            elif self.EMAIL_VERIFY_PATTERN in self.path:
                response_content = self.email_verify_cmd(self, parsed_url)
            elif self.DOMAIN_AGE_PATTERN in self.path:
                response_content = self.domain_age_cmd(self, parsed_url)
            elif self.PARKED_DOMAIN_PATTERN in self.path:
                response_content = self.parked_domain_cmd(self, parsed_url)

            elif HTTP_ERROR_SERVER_PATH in self.path:
                response_code = requests.codes.internal_server_error #pylint: disable=no-member
                response_content = "500 - Internal Server Error"

            else:
                response_content = self.unknown_call(self.path)
        else:
            response_content = self.bad_param(
                "key",
                parsed_api_key,
                SAMPLE_API_KEY
            )

        self.send_response(response_code, response_content)

        self.send_header('Content-Type', 'text/plain; charset=utf-8', )
        self.end_headers()

        self.wfile.write(response_content.encode())

    @staticmethod
    def stats_remained_cmd():
        return MessageUtils.dict_to_json(SAMPLE_STATS_REMAINED, pretty_print=False)

    @staticmethod
    def ip_rep_cmd(self, parsed_url):
        ip = \
            urlparse.parse_qs(parsed_url.query)[ApiVoidCallback.PARAM_IP][0]
        if ip == SAMPLE_IP:
            return MessageUtils.dict_to_json(SAMPLE_IP_REP, pretty_print=False)
        return self.bad_param(ApiVoidCallback.PARAM_IP, ip)

    @staticmethod
    def domain_rep_cmd(self, parsed_url):
        host = \
            urlparse.parse_qs(parsed_url.query)[ApiVoidCallback.PARAM_HOST][0]
        if host == SAMPLE_HOST:
            return MessageUtils.dict_to_json(SAMPLE_DOMAIN_REP, pretty_print=False)
        return self.bad_param(ApiVoidCallback.PARAM_HOST, host)

    @staticmethod
    def dns_lookup_cmd(self, parsed_url):
        action = \
            urlparse.parse_qs(parsed_url.query)[ApiVoidCallback.PARAM_ACTION][0]
        host = \
            urlparse.parse_qs(parsed_url.query)[ApiVoidCallback.PARAM_HOST][0]
        if action == SAMPLE_ACTION:
            if host == SAMPLE_HOST:
                return MessageUtils.dict_to_json(SAMPLE_DNS_LOOKUP, pretty_print=False)
            return self.bad_param(ApiVoidCallback.PARAM_HOST, host)
        return self.bad_param(ApiVoidCallback.PARAM_ACTION, action)

    @staticmethod
    def ssl_info_cmd(self, parsed_url):
        host = \
            urlparse.parse_qs(parsed_url.query)[ApiVoidCallback.PARAM_HOST][0]
        if host == SAMPLE_HOST:
            return MessageUtils.dict_to_json(SAMPLE_SSL_INFO, pretty_print=False)
        return self.bad_param(ApiVoidCallback.PARAM_HOST, host)

    @staticmethod
    def threatlog_cmd(self, parsed_url):
        host = \
            urlparse.parse_qs(parsed_url.query)[ApiVoidCallback.PARAM_HOST][0]
        if host == SAMPLE_HOST:
            return MessageUtils.dict_to_json(SAMPLE_THREATLOG, pretty_print=False)
        return self.bad_param(ApiVoidCallback.PARAM_HOST, host)

    @staticmethod
    def email_verify_cmd(self, parsed_url):
        host = \
            urlparse.parse_qs(parsed_url.query)[ApiVoidCallback.PARAM_HOST][0]
        if host == SAMPLE_HOST:
            return MessageUtils.dict_to_json(SAMPLE_EMAIL_VERIFY, pretty_print=False)
        return self.bad_param(ApiVoidCallback.PARAM_HOST, host)

    @staticmethod
    def domain_age_cmd(self, parsed_url):
        host = \
            urlparse.parse_qs(parsed_url.query)[ApiVoidCallback.PARAM_HOST][0]
        if host == SAMPLE_HOST:
            return MessageUtils.dict_to_json(SAMPLE_DOMAIN_AGE, pretty_print=False)
        return self.bad_param(ApiVoidCallback.PARAM_HOST, host)

    @staticmethod
    def parked_domain_cmd(self, parsed_url):
        host = \
            urlparse.parse_qs(parsed_url.query)[ApiVoidCallback.PARAM_HOST][0]
        if host == SAMPLE_HOST:
            return MessageUtils.dict_to_json(SAMPLE_PARKED_DOMAIN, pretty_print=False)
        return self.bad_param(ApiVoidCallback.PARAM_HOST, host)


    @staticmethod
    def unknown_call(path):
        return MessageUtils.dict_to_json(
            {
                "unit_test_error_unknown_host": path
            },
            pretty_print=False
        )

    @staticmethod
    def bad_param(param_name, param_val, expected_val='unknown'):
        return MessageUtils.dict_to_json(
            {
                "bad_param_name": param_name,
                "bad_param_val": param_val,
                "exp_param_val": expected_val
            },
            pretty_print=False
        )


class MockServerRunner(object):

    SERVER_HOST = "localhost"
    SERVING_TIMEOUT = 60

    def __init__(self):
        self.mock_server_port = 0
        self.mock_server = None
        self.mock_server_address = ""
        self.mock_server_thread = None

    def __enter__(self):
        self.mock_server_address, self.mock_server_port = get_free_port()
        self.mock_server = HTTPServer(
            (self.SERVER_HOST, self.mock_server_port),
            MockApiVoidServerRequestHandler
        )

        self.mock_server_thread = Thread(target=self.mock_server.serve_forever)
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mock_server.shutdown()
        self.mock_server_thread.join()
        self.mock_server.server_close()
