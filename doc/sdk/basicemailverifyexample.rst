Basic Email Verify Example
============================

This sample retrieves and displays email verification information for a domain by invoking the APIVoid service via
DXL.

For more information see the API Services documentation:
    https://app.apivoid.com/dashboard/api/email-verify/documentation/

Prerequisites
*************
* The samples configuration step has been completed (see :doc:`sampleconfig`)
* The APIVoid DXL service is running (see :doc:`running`)

Running
*******

To run this sample execute the ``sample/basic/basic_email_verify.py`` script as follows:

    .. parsed-literal::

        python sample/basic/basic_email_verify.py

The output should appear similar to the following:

    .. code-block:: python

        {
            "credits_expiration": "Sat, 27 Apr 2019 20:51:14 GMT",
            "credits_remained": 24.49,
            "data": {
                "alexa_top_10k": false,
                "common_domain": false,
                "dirty_words": false,
                "disposable": false,
                "has_mx_records": true,
                "mistyped_domain": false,
                "risky_tld": false,
                "suggested_domain": ""
            },
            "elapsed_time": "0.67",
            "estimated_queries": "408",
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

            # Invoke 'email verify' method
            request_topic = "/opendxl-apivoid/service/apivoid/emailverify"

            req = Request(request_topic)
            MessageUtils.dict_to_json_payload(req, {"host": "027.ru"})

            res = client.sync_request(req, timeout=60)
            if res.message_type != Message.MESSAGE_TYPE_ERROR:
                res_dict = MessageUtils.json_payload_to_dict(res)
                print(MessageUtils.dict_to_json(res_dict, pretty_print=True))
            else:
                print("Error invoking service with topic '{0}': {1} ({2})".format(
                    request_topic, res.error_message, res.error_code))


After connecting to the DXL fabric, a `request message` is created with a topic that targets the "email verify" method
of the APIVoid DXL service.

The final step is to perform a `synchronous request` via the DXL fabric. If the `response message` is not an error
its contents are displayed.
