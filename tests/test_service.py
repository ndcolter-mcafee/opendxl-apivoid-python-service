import sys
import time
from configparser import ConfigParser
from dxlbootstrap.util import MessageUtils
from dxlclient import Request
from dxlapivoidservice import ApiVoidService
from dxlapivoidservice.requesthandlers import ApiVoidCallback

from tests.test_base import BaseClientTest
from tests.test_value_constants import *
from tests.mock_apivoidhttpserver import MockServerRunner

sys.path.append(
    os.path.dirname(os.path.abspath(__file__)) + "/../.."
)

def create_service_configfile(config_file_name):
    config = ConfigParser()

    config['General'] = {'apiKey': SAMPLE_API_KEY}

    with open(config_file_name, 'w') as config_file:
        config.write(config_file)


class TestConfiguration(BaseClientTest):

    def test_loadconfig(self):

        create_service_configfile(
            config_file_name=APIVOID_CONFIG_FILENAME,
        )

        apivoid_service = ApiVoidService(TEST_FOLDER)
        apivoid_service._load_configuration()

        self.assertEqual(apivoid_service.api_key, SAMPLE_API_KEY)

        os.remove(APIVOID_CONFIG_FILENAME)


    def test_registerservices(self):
        with MockServerRunner():
            with self.create_client(max_retries=0) as dxl_client:
                dxl_client.connect()

                apivoid_service = ApiVoidService(TEST_FOLDER)
                apivoid_service._dxl_client = dxl_client

                create_service_configfile(
                    config_file_name=APIVOID_CONFIG_FILENAME
                )

                apivoid_service._load_configuration()
                apivoid_service.on_register_services()

                self.assertTrue(len(apivoid_service._services) == 1)

                expected_topics = []

                for key in ApiVoidService.REQ_TOPICS_DICT.keys():
                    expected_topics.append(key)
                    expected_topics.append(key + "/" + ApiVoidService.REQ_TOPIC_SUFFIX_STATS)

                self.assertEqual(
                    sorted(expected_topics),
                    sorted(apivoid_service._services[0].topics)
                )


class TestApiVoidRequestCallback(BaseClientTest):

    def test_validate_params(self):
        test_params = ["test", "required", "parameters"]
        apivoid_callback = ApiVoidCallback(None, required_params=test_params)

        test_req_dict = {
            "test": True,
            "required": True,
            "parameters": True
        }

        # Expected to raise an exception if there is a mismatch, so no need to assert
        apivoid_callback._validate(test_req_dict)

        test_req_dict = {
            "test": True,
            "parameters": True
        }

        self.assertRaisesRegex(
            Exception,
            r"Required parameter not specified: ",
            apivoid_callback._validate,
            test_req_dict,
        )

        test_req_dict = {
            "test": True,
            "required": True,
            "parameters": True,
            "false": True
        }

        # Expected to raise an exception if there is a mismatch, so no need to assert
        apivoid_callback._validate(test_req_dict)

        test_req_dict = {
            "test": True,
            "required": True,
            "false": True
        }

        self.assertRaisesRegex(
            Exception,
            r"Required parameter not specified: ",
            apivoid_callback._validate,
            test_req_dict,
        )


    def test_callback_statsremained(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockServerRunner() as server_runner:
                with ApiVoidService(TEST_FOLDER) as apivoid_service:
                    apivoid_service._dxl_client = dxl_client

                    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
                                                  + str(server_runner.mock_server_port) \
                                                  + "/{0}/v1/pay-as-you-go/{1}"

                    apivoid_service.run()

                    request_topic = ApiVoidService.REQ_TOPIC_IP_REP + "/" + \
                        ApiVoidService.REQ_TOPIC_SUFFIX_STATS
                    req = Request(request_topic)

                    res = apivoid_service._dxl_client.sync_request(req, timeout=30)

                    res_dict = MessageUtils.json_payload_to_dict(res)

                    self.assertDictEqual(
                        SAMPLE_STATS_REMAINED,
                        res_dict
                    )


    def test_callback_iprep(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockServerRunner() as server_runner:
                with ApiVoidService(TEST_FOLDER) as apivoid_service:
                    apivoid_service._dxl_client = dxl_client

                    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
                                                  + str(server_runner.mock_server_port) \
                                                  + "/{0}/v1/pay-as-you-go/{1}"

                    apivoid_service.run()

                    request_topic = ApiVoidService.REQ_TOPIC_IP_REP
                    req = Request(request_topic)
                    MessageUtils.dict_to_json_payload(req, {ApiVoidCallback.PARAM_IP: SAMPLE_IP})

                    res = apivoid_service._dxl_client.sync_request(req, timeout=30)

                    res_dict = MessageUtils.json_payload_to_dict(res)

                    self.assertDictEqual(
                        SAMPLE_IP_REP,
                        res_dict
                    )

    def test_callback_domainrep(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockServerRunner() as server_runner:
                with ApiVoidService(TEST_FOLDER) as apivoid_service:
                    apivoid_service._dxl_client = dxl_client

                    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
                                                  + str(server_runner.mock_server_port) \
                                                  + "/{0}/v1/pay-as-you-go/{1}"

                    apivoid_service.run()

                    request_topic = ApiVoidService.REQ_TOPIC_DOMAIN_REP
                    req = Request(request_topic)
                    MessageUtils.dict_to_json_payload(req, {ApiVoidCallback.PARAM_HOST: SAMPLE_HOST})

                    res = apivoid_service._dxl_client.sync_request(req, timeout=30)

                    res_dict = MessageUtils.json_payload_to_dict(res)

                    self.assertDictEqual(
                        SAMPLE_DOMAIN_REP,
                        res_dict
                    )

    def test_callback_dnslookup(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockServerRunner() as server_runner:
                with ApiVoidService(TEST_FOLDER) as apivoid_service:
                    apivoid_service._dxl_client = dxl_client

                    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
                                                  + str(server_runner.mock_server_port) \
                                                  + "/{0}/v1/pay-as-you-go/{1}"

                    apivoid_service.run()

                    request_topic = ApiVoidService.REQ_TOPIC_DNS_LOOKUP
                    req = Request(request_topic)
                    MessageUtils.dict_to_json_payload(
                        req,
                        {
                            ApiVoidCallback.PARAM_HOST: SAMPLE_HOST,
                            ApiVoidCallback.PARAM_ACTION: SAMPLE_ACTION
                        }
                    )

                    res = apivoid_service._dxl_client.sync_request(req, timeout=30)

                    res_dict = MessageUtils.json_payload_to_dict(res)

                    self.assertDictEqual(
                        SAMPLE_DNS_LOOKUP,
                        res_dict
                    )

    def test_callback_sslinfo(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockServerRunner() as server_runner:
                with ApiVoidService(TEST_FOLDER) as apivoid_service:
                    apivoid_service._dxl_client = dxl_client

                    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
                                                  + str(server_runner.mock_server_port) \
                                                  + "/{0}/v1/pay-as-you-go/{1}"

                    apivoid_service.run()

                    request_topic = ApiVoidService.REQ_TOPIC_SSL_INFO
                    req = Request(request_topic)
                    MessageUtils.dict_to_json_payload(req, {ApiVoidCallback.PARAM_HOST: SAMPLE_HOST})

                    res = apivoid_service._dxl_client.sync_request(req, timeout=30)

                    res_dict = MessageUtils.json_payload_to_dict(res)

                    self.assertDictEqual(
                        SAMPLE_SSL_INFO,
                        res_dict
                    )

    def test_callback_threatlog(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockServerRunner() as server_runner:
                with ApiVoidService(TEST_FOLDER) as apivoid_service:
                    apivoid_service._dxl_client = dxl_client

                    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
                                                  + str(server_runner.mock_server_port) \
                                                  + "/{0}/v1/pay-as-you-go/{1}"

                    apivoid_service.run()

                    request_topic = ApiVoidService.REQ_TOPIC_THREATLOG
                    req = Request(request_topic)
                    MessageUtils.dict_to_json_payload(req, {ApiVoidCallback.PARAM_HOST: SAMPLE_HOST})

                    res = apivoid_service._dxl_client.sync_request(req, timeout=30)

                    res_dict = MessageUtils.json_payload_to_dict(res)

                    self.assertDictEqual(
                        SAMPLE_THREATLOG,
                        res_dict
                    )

    def test_callback_emailverify(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockServerRunner() as server_runner:
                with ApiVoidService(TEST_FOLDER) as apivoid_service:
                    apivoid_service._dxl_client = dxl_client

                    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
                                                  + str(server_runner.mock_server_port) \
                                                  + "/{0}/v1/pay-as-you-go/{1}"

                    apivoid_service.run()

                    request_topic = ApiVoidService.REQ_TOPIC_EMAIL_VERIFY
                    req = Request(request_topic)
                    MessageUtils.dict_to_json_payload(req, {ApiVoidCallback.PARAM_HOST: SAMPLE_HOST})

                    res = apivoid_service._dxl_client.sync_request(req, timeout=30)

                    res_dict = MessageUtils.json_payload_to_dict(res)

                    self.assertDictEqual(
                        SAMPLE_EMAIL_VERIFY,
                        res_dict
                    )

    def test_callback_domainage(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockServerRunner() as server_runner:
                with ApiVoidService(TEST_FOLDER) as apivoid_service:
                    apivoid_service._dxl_client = dxl_client

                    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
                                                  + str(server_runner.mock_server_port) \
                                                  + "/{0}/v1/pay-as-you-go/{1}"

                    apivoid_service.run()

                    request_topic = ApiVoidService.REQ_TOPIC_DOMAIN_AGE
                    req = Request(request_topic)
                    MessageUtils.dict_to_json_payload(req, {ApiVoidCallback.PARAM_HOST: SAMPLE_HOST})

                    res = apivoid_service._dxl_client.sync_request(req, timeout=30)

                    res_dict = MessageUtils.json_payload_to_dict(res)

                    self.assertDictEqual(
                        SAMPLE_DOMAIN_AGE,
                        res_dict
                    )

    def test_callback_parkeddomain(self):
        with BaseClientTest.create_client(max_retries=0) as dxl_client:
            dxl_client.connect()

            with MockServerRunner() as server_runner:
                with ApiVoidService(TEST_FOLDER) as apivoid_service:
                    apivoid_service._dxl_client = dxl_client

                    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
                                                  + str(server_runner.mock_server_port) \
                                                  + "/{0}/v1/pay-as-you-go/{1}"

                    apivoid_service.run()

                    request_topic = ApiVoidService.REQ_TOPIC_PARKED_DOMAIN
                    req = Request(request_topic)
                    MessageUtils.dict_to_json_payload(req, {ApiVoidCallback.PARAM_HOST: SAMPLE_HOST})

                    res = apivoid_service._dxl_client.sync_request(req, timeout=30)

                    res_dict = MessageUtils.json_payload_to_dict(res)

                    self.assertDictEqual(
                        SAMPLE_PARKED_DOMAIN,
                        res_dict
                    )
