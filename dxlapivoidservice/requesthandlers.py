from __future__ import absolute_import
import logging
import requests

from dxlclient.callbacks import RequestCallback
from dxlclient.message import Response, ErrorResponse
from dxlbootstrap.util import MessageUtils


# Configure local logger
logger = logging.getLogger(__name__)


class ApiVoidCallback(RequestCallback):
    """
    Request callback used to convert DXL requests to APIVoid Services invocations
    and send back corresponding DXL response
    """

    #: The host request parameter
    PARAM_HOST = "host"
    PARAM_IP = "ip"
    PARAM_ACTION = "action"
    PARAM_STATS = "stats"


    def __init__(self, app, required_params=None):
        """
        Constructor parameters:

        :param app: The application this handler is associated with
        """
        super(ApiVoidCallback, self).__init__()
        self._app = app
        self._required_params = required_params

    def _validate(self, req_dict):
        """
        Validates that required parameters are present in the specified
        dictionary

        :param req_dict: The request dictionary
        """
        if self._required_params:
            for param in self._required_params:
                if param not in req_dict:
                    raise Exception("Required parameter not specified: '{0}'".format(param))

    def on_request(self, request): #pylint
        """
        Invoked when a request message is received.

        :param request: The request message
        """
        # Handle request
        logger.info("Request received on topic: '%s' with payload: '%s'",
                    request.destination_topic,
                    MessageUtils.decode_payload(request))

        try:
            command = request.destination_topic[self._app.SERVICE_TYPE_LENGTH + 1:]

            stats_remained = False
            if self._app.REQ_TOPIC_SUFFIX_STATS in command:
                stats_remained = True
                command = command[:len(command) - len(self._app.REQ_TOPIC_SUFFIX_STATS) - 1]

            # API URL
            api_url = self._app.API_VOID_URL_FORMAT.format(
                command,
                self._app.KEY_PARAM_FORMAT.format(self._app.api_key)
            )

            if stats_remained:
                api_url = "{0}&{1}".format(api_url, self.PARAM_STATS)
            else:
                params = {}
                if request.payload:
                    params = MessageUtils.json_payload_to_dict(request)

                if self._required_params:
                    self._validate(params)

                if command == self._app.CMD_IP_REPUTATION:
                    ip_param = params[self.PARAM_IP]
                    api_url = "{0}&{1}={2}".format(api_url, self.PARAM_IP, ip_param)
                elif command == self._app.CMD_DOMAIN_REPUTATION:
                    host = params[self.PARAM_HOST]
                    api_url = "{0}&{1}={2}".format(api_url, self.PARAM_HOST, host)
                elif command == self._app.CMD_DNS_LOOKUP:
                    action = params[self.PARAM_ACTION]
                    host = params[self.PARAM_HOST]
                    api_url = "{0}&{1}={2}&{3}={4}".format(
                        api_url,
                        self.PARAM_ACTION,
                        action,
                        self.PARAM_HOST,
                        host
                    )
                elif command in self._app.CMD_LIST:
                    host = params[self.PARAM_HOST]
                    api_url = "{0}&{1}={2}".format(api_url, self.PARAM_HOST, host)

            # Invoke URLVoid API
            api_void_response = requests.get(api_url)

            # Check HTTP response code
            api_void_response.raise_for_status()

            # Create response
            res = Response(request)

            # Set payload
            MessageUtils.encode_payload(res, api_void_response.text)

            # Send response
            self._app.client.send_response(res)

        except Exception as ex:
            logger.exception("Error handling request")
            err_res = ErrorResponse(request, error_message=MessageUtils.encode(str(ex)))
            self._app.client.send_response(err_res)
