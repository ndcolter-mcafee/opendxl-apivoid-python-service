from __future__ import absolute_import
import logging

from dxlbootstrap.app import Application
from dxlclient.service import ServiceRegistrationInfo
from .requesthandlers import *

# Configure local logger
logger = logging.getLogger(__name__)


class ApiVoidService(Application):
    """
    The "APIVoid DXL Service" application class.
    """

    #: The name of the "General" section within the application configuration file
    GENERAL_CONFIG_SECTION = "General"

    #: The property used to specify the APIVoid API Key in the application
    #: configuration file
    GENERAL_API_KEY_CONFIG_PROP = "apiKey"

    #: The DXL service type for APIVoid Services
    SERVICE_TYPE = "/opendxl-apivoid/service/apivoid"

    #: The length of the DXL service type string
    SERVICE_TYPE_LENGTH = len(SERVICE_TYPE)

    #: The URL format for APIVoid Services invocations
    API_VOID_URL_FORMAT = "https://endpoint.apivoid.com/{0}/v1/pay-as-you-go/{1}"
    KEY_PARAM_FORMAT = "?key={0}"

    #: The "IP Reputation" command & DXL request topic
    CMD_IP_REPUTATION = "iprep"
    REQ_TOPIC_IP_REP = "{0}/{1}".format(SERVICE_TYPE, CMD_IP_REPUTATION)

    #: The "Domain Reputation" command & DXL request topic
    CMD_DOMAIN_REPUTATION = "domainbl"
    REQ_TOPIC_DOMAIN_REP = "{0}/{1}".format(SERVICE_TYPE, CMD_DOMAIN_REPUTATION)

    #: The "DNS Lookup" command & DXL request topic
    CMD_DNS_LOOKUP = "dnslookup"
    REQ_TOPIC_DNS_LOOKUP = "{0}/{1}".format(SERVICE_TYPE, CMD_DNS_LOOKUP)

    #: The "SSL Info" command & DXL request topic
    CMD_SSL_INFO = "sslinfo"
    REQ_TOPIC_SSL_INFO = "{0}/{1}".format(SERVICE_TYPE, CMD_SSL_INFO)

    #: The "ThreatLog" command & DXL request topic
    CMD_THREATLOG = "threatlog"
    REQ_TOPIC_THREATLOG = "{0}/{1}".format(SERVICE_TYPE, CMD_THREATLOG)

    #: The "Email Verify" command & DXL request topic
    CMD_EMAIL_VERIFY = "emailverify"
    REQ_TOPIC_EMAIL_VERIFY = "{0}/{1}".format(SERVICE_TYPE, CMD_EMAIL_VERIFY)

    #: The "Domain Age" command & DXL request topic
    CMD_DOMAIN_AGE = "domainage"
    REQ_TOPIC_DOMAIN_AGE = "{0}/{1}".format(SERVICE_TYPE, CMD_DOMAIN_AGE)

    #: The "Parked Domain" command & DXL request topic
    CMD_PARKED_DOMAIN = "parkeddomain"
    REQ_TOPIC_PARKED_DOMAIN = "{0}/{1}".format(SERVICE_TYPE, CMD_PARKED_DOMAIN)

    #: The "Stats Remained" suffix
    REQ_TOPIC_SUFFIX_STATS = "stats"

    #: Full request topic list:
    REQ_TOPICS_DICT = {
        REQ_TOPIC_IP_REP: [ApiVoidCallback.PARAM_IP],
        REQ_TOPIC_DOMAIN_REP: [ApiVoidCallback.PARAM_HOST],
        REQ_TOPIC_DNS_LOOKUP: [ApiVoidCallback.PARAM_HOST, ApiVoidCallback.PARAM_ACTION],
        REQ_TOPIC_SSL_INFO: [ApiVoidCallback.PARAM_HOST],
        REQ_TOPIC_THREATLOG: [ApiVoidCallback.PARAM_HOST],
        REQ_TOPIC_EMAIL_VERIFY: [ApiVoidCallback.PARAM_HOST],
        REQ_TOPIC_DOMAIN_AGE: [ApiVoidCallback.PARAM_HOST],
        REQ_TOPIC_PARKED_DOMAIN: [ApiVoidCallback.PARAM_HOST]
    }

    def __init__(self, config_dir):
        """
        Constructor parameters:

        :param config_dir: The location of the configuration files for the
            application
        """
        super(ApiVoidService, self).__init__(config_dir, "dxlapivoidservice.config")
        self._api_key = None

    @property
    def api_key(self):
        """
        The APIVoid API key
        """
        return self._api_key

    @property
    def client(self):
        """
        The DXL client used by the application to communicate with the DXL
        fabric
        """
        return self._dxl_client

    @property
    def config(self):
        """
        The application configuration (as read from the "dxlapivoidservice.config" file)
        """
        return self._config

    def on_run(self):
        """
        Invoked when the application has started running.
        """
        logger.info("On 'run' callback.")

    def on_load_configuration(self, config):
        """
        Invoked after the application-specific configuration has been loaded

        This callback provides the opportunity for the application to parse
        additional configuration properties.

        :param config: The application configuration
        """
        logger.info("On 'load configuration' callback.")

        # API Key
        try:
            self._api_key = config.get(self.GENERAL_CONFIG_SECTION,
                                       self.GENERAL_API_KEY_CONFIG_PROP)
        except Exception:
            pass
        if not self._api_key:
            raise Exception(
                "APIVoid API Key not found in configuration file: {0}"
                .format(self._app_config_path))

    def on_dxl_connect(self):
        """
        Invoked after the client associated with the application has connected
        to the DXL fabric.
        """
        logger.info("On 'DXL connect' callback.")

    def on_register_services(self):
        """
        Invoked when services should be registered with the application
        """
        # Register service
        logger.info("Registering service: %s", "apivoidservice")
        service = ServiceRegistrationInfo(self._dxl_client, self.SERVICE_TYPE)

        print(str(self.REQ_TOPICS_DICT.keys()))

        for topic_key in self.REQ_TOPICS_DICT.keys():
            topic = topic_key
            # Register request callback for this API call
            logger.info("Registering request callbacks: %s", topic)
            self.add_request_callback(
                service,
                topic,
                ApiVoidCallback(self, self.REQ_TOPICS_DICT[topic_key]),
                False
            )

            topic += "/" + self.REQ_TOPIC_SUFFIX_STATS

            # Register "Stats Remained" for this API call
            logger.info("Registering request callback: %s", topic)
            self.add_request_callback(
                service,
                topic,
                ApiVoidCallback(self),
                False
            )

        self.register_service(service)
