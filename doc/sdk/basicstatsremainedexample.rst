Basic Stats Remained Example
============================

This sample retrieves and displays the number of queries that remain for the account associated with the
APIVoid API key by invoking the APIVoid service via DXL. The estimated number of queries remaining is
determined based on the API call on which the 'stats remained' request is sent.

For example, the 'IP reputation' service topic:

    .. parsed-literal::

        /opendxl-apivoid/service/apivoid/iprep

To send a 'stats remained' request for 'IP reputation' would use the following topic:

  .. parsed-literal::

        /opendxl-apivoid/service/apivoid/iprep/stats

Similarly, to send a 'stats remained' request for 'dnslookup' would use the following topic:

  .. parsed-literal::

        /opendxl-apivoid/service/apivoid/dnslookup/stats


For more information see the API Services documentation:
    https://app.apivoid.com

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The APIVoid DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_stats_remained.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_stats_remained.py

The output should appear similar to the following:

    .. code-block:: python

        {
            "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
            "credits_remained": 24.92,
            "elapsed_time": "0.02",
            "estimated_queries": "311",
            "success": True
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
            request_topic = "/opendxl-apivoid/service/apivoid/iprep/stats"

            req = Request(request_topic)

            res = client.sync_request(req, timeout=60)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{0}': {1} ({2})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets a "stats remained" method
of the APIVoid DXL service.

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are displayed.
