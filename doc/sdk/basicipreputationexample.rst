Basic IP Reputation Example
============================

This sample retrieves and displays the safety reputation of an IP address by invoking the APIVoid service via DXL.

For more information see the API Services documentation:
    https://app.apivoid.com/dashboard/api/ip-reputation/documentation/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The APIVoid DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_ip_reputation.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_ip_reputation.py

The output should appear similar to the following:

    .. code-block:: python

        {
            "credits_expiration": "Sat, 27 Apr 2019 20:51:14 GMT",
            "credits_remained": 24.92,
            "data": {
                "report": {
                    "anonymity": {
                        "is_hosting": false,
                        "is_proxy": false,
                        "is_tor": false,
                        "is_vpn": false,
                        "is_webproxy": false
                    },
                    "blacklists": {
                        "detection_rate": "0%",
                        "detections": 0,
                        "engines": {
                            "0": {
                                "detected": false,
                                "elapsed": "0.04",
                                "engine": "EFnet_RBL",
                                "reference": "http://rbl.efnetrbl.org/multicheck.php"
                            }
                            .
                            .
                            .
                            "99": {
                                "detected": false,
                                "elapsed": "0.24",
                                "engine": "MegaRBL",
                                "reference": "https://www.megarbl.net/check"
                            }
                        },
                        "engines_count": 100,
                        "scantime": "0.43"
                    },
                    "information": {
                        "city_name": "Moscow",
                        "continent_code": "EU",
                        "continent_name": "Europe",
                        "country_code": "RU",
                        "country_name": "Russian Federation",
                        "isp": "LLC Masterhost",
                        "latitude": 55.752220153808594,
                        "longitude": 37.61555862426758,
                        "region_name": "Moskva",
                        "reverse_dns": "fe.shared.masterhost.ru"
                    }
                }
            },
            "elapsed_time": "0.78",
            "estimated_queries": "311",
            "success": true
        }

The received results are displayed.

Details
*******

The majority of the sample code is shown below:

    .. code-block:: python

        # Create the client
        with DxlClient(config) as client:

            # Connect to the fabric
            client.connect()

            logger.info("Connected to DXL fabric.")

            # Invoke 'stats remained' method
            request_topic = "/opendxl-apivoid/service/apivoid/iprep"

            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"ip": "90.156.201.27"})

            res = client.sync_request(req, timeout=60)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{0}': {1} ({2})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "IP reputation" method
of the APIVoid DXL service.

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are displayed.
