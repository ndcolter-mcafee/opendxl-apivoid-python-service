from __future__ import absolute_import
from __future__ import print_function
import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlclient.message import Message, Request
from dxlbootstrap.util import MessageUtils

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    logger.info("Connected to DXL fabric.")

    # Invoke 'stats remained' method
    request_topic = "/opendxl-apivoid/service/apivoid/iprep/stats"

    req = Request(request_topic)

    res = client.sync_request(req, timeout=60)
    if res.message_type != Message.MESSAGE_TYPE_ERROR:
        res_dict = MessageUtils.json_payload_to_dict(res)
        print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
    else:
        print("Error invoking service with topic '{0}': {1} ({2})".format(
            request_topic, res.error_message, res.error_code))
