Basic DNS Lookup Example
============================

This sample retrieves and displays the DNS records of a given type (CNAME, SOA, etc.) for a host by invoking the
APIVoid service via DXL.

For more information, including a list of supported DNS record types, see the API Services documentation:
    https://app.apivoid.com/dashboard/api/dns-lookup/documentation/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The APIVoid DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_dns_lookup.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_dns_lookup.py

The output should appear similar to the following:

    .. code-block:: python

        {
            "credits_expiration": "Sat, 27 Apr 2019 20:51:14 GMT",
            "credits_remained": 24.72,
            "data": {
                "records": {
                    "count": 1,
                    "found": true,
                    "items": [
                        {
                            "class": "IN",
                            "host": "027.ru",
                            "ip": "46.38.62.7",
                            "ttl": 3599,
                            "type": "A"
                        }
                    ]
                }
            },
            "elapsed_time": "0.33",
            "estimated_queries": "412",
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

            # Invoke 'DNS lookup' method for DNS AAAA records
            request_topic = "/opendxl-apivoid/service/apivoid/dnslookup"

            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(
                req,
                {
                    "action": "dns-a",
                    "host": "027.ru"
                }
            )

            res = client.sync_request(req, timeout=60)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{0}': {1} ({2})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "DNS lookup" method
of the APIVoid DXL service.

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are displayed.
