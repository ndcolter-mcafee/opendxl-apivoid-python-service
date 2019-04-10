from dxlapivoidservice import ApiVoidService
from tests.mock_apivoidhttpserver import MockServerRunner
from tests.test_base import *
from tests.test_service import create_service_configfile
from tests.test_value_constants import *


def configure_service(port):

    create_service_configfile(
        config_file_name=APIVOID_CONFIG_FILENAME
    )

    apivoid_service = ApiVoidService(TEST_FOLDER)

    apivoid_service.API_VOID_URL_FORMAT = "http://127.0.0.1:" \
        + str(port) \
        + "/{0}/v1/pay-as-you-go/{1}"

    apivoid_service.run()

    return apivoid_service


class TestSamples(BaseClientTest):

    def test_statsremained_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_stats_remained.py"

        with MockServerRunner() as mock_server, \
            configure_service(mock_server.mock_server_port):

            mock_print = self.run_sample(sample_filename)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_STATS_REMAINED["credits_remained"]))
            )

    def test_iprep_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_ip_reputation.py"
        temp_sample_file = TempSampleFile(sample_filename)

        with MockServerRunner() as mock_server, \
            configure_service(mock_server.mock_server_port):

            target_line = "    MessageUtils.dict_to_json_payload(req, {\"ip\": "
            replacement_line = target_line + "\"" + SAMPLE_IP + "\"})\n"
            temp_sample_file.write_file_line(target_line, replacement_line)

            mock_print = self.run_sample(temp_sample_file.temp_file.name)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_IP_REP["credits_remained"]))
            )

    def test_domainrep_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_domain_reputation.py"
        temp_sample_file = TempSampleFile(sample_filename)

        with MockServerRunner() as mock_server, \
            configure_service(mock_server.mock_server_port):

            target_line = "    MessageUtils.dict_to_json_payload(req, {\"host\": "
            replacement_line = target_line + "\"" + SAMPLE_HOST + "\"})\n"
            temp_sample_file.write_file_line(target_line, replacement_line)

            mock_print = self.run_sample(temp_sample_file.temp_file.name)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_DOMAIN_REP["credits_remained"]))
            )

    def test_dnslookup_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_dns_lookup.py"
        temp_sample_file = TempSampleFile(sample_filename)

        with MockServerRunner() as mock_server, \
            configure_service(mock_server.mock_server_port):

            target_line = "            \"action\": "
            replacement_line = target_line + "\"" + SAMPLE_ACTION + "\",\n"
            temp_sample_file.write_file_line(target_line, replacement_line)

            target_line = "            \"host\": "
            replacement_line = target_line + "\"" + SAMPLE_HOST + "\"\n"
            temp_sample_file.write_file_line(target_line, replacement_line)

            mock_print = self.run_sample(temp_sample_file.temp_file.name)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_DNS_LOOKUP["credits_remained"]))
            )

    def test_sslinfo_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_ssl_info.py"
        temp_sample_file = TempSampleFile(sample_filename)

        with MockServerRunner() as mock_server, \
            configure_service(mock_server.mock_server_port):

            target_line = "    MessageUtils.dict_to_json_payload(req, {\"host\": "
            replacement_line = target_line + "\"" + SAMPLE_HOST + "\"})\n"
            temp_sample_file.write_file_line(target_line, replacement_line)

            mock_print = self.run_sample(temp_sample_file.temp_file.name)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_SSL_INFO["credits_remained"]))
            )

    def test_threatlog_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_threatlog.py"
        temp_sample_file = TempSampleFile(sample_filename)

        with MockServerRunner() as mock_server, \
            configure_service(mock_server.mock_server_port):

            target_line = "    MessageUtils.dict_to_json_payload(req, {\"host\": "
            replacement_line = target_line + "\"" + SAMPLE_HOST + "\"})\n"
            temp_sample_file.write_file_line(target_line, replacement_line)

            mock_print = self.run_sample(temp_sample_file.temp_file.name)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_THREATLOG["credits_remained"]))
            )

    def test_emailverify_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_email_verify.py"
        temp_sample_file = TempSampleFile(sample_filename)

        with MockServerRunner() as mock_server, \
            configure_service(mock_server.mock_server_port):

            target_line = "    MessageUtils.dict_to_json_payload(req, {\"host\": "
            replacement_line = target_line + "\"" + SAMPLE_HOST + "\"})\n"
            temp_sample_file.write_file_line(target_line, replacement_line)

            mock_print = self.run_sample(temp_sample_file.temp_file.name)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_EMAIL_VERIFY["credits_remained"]))
            )

    def test_domainage_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_domain_age.py"
        temp_sample_file = TempSampleFile(sample_filename)

        with MockServerRunner() as mock_server, \
            configure_service(mock_server.mock_server_port):

            target_line = "    MessageUtils.dict_to_json_payload(req, {\"host\": "
            replacement_line = target_line + "\"" + SAMPLE_HOST + "\"})\n"
            temp_sample_file.write_file_line(target_line, replacement_line)

            mock_print = self.run_sample(temp_sample_file.temp_file.name)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_DOMAIN_AGE["credits_remained"]))
            )

    def test_parkeddomain_example(self):
        # Modify sample file to include necessary sample data
        sample_filename = self.BASIC_FOLDER + "/basic_parked_domain.py"
        temp_sample_file = TempSampleFile(sample_filename)

        with MockServerRunner() as mock_server, \
            configure_service(mock_server.mock_server_port):

            target_line = "    MessageUtils.dict_to_json_payload(req, {\"host\": "
            replacement_line = target_line + "\"" + SAMPLE_HOST + "\"})\n"
            temp_sample_file.write_file_line(target_line, replacement_line)

            mock_print = self.run_sample(temp_sample_file.temp_file.name)

            mock_print.assert_any_call(
                StringDoesNotContain("Error")
            )

            # Validate page_load from expected result
            mock_print.assert_any_call(
                StringContains(str(SAMPLE_PARKED_DOMAIN["credits_remained"]))
            )