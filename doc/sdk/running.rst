Running Service
===============

Once the APIVoid DXL Service has been installed and the configuration files are populated it can be started by
executing the following command line:

    .. parsed-literal::

        python -m dxlapivoidservice <configuration-directory>

    The ``<configuration-directory>`` argument must point to a directory containing the configuration files
    required for the APIVoid DXL Service (see :doc:`configuration`).

For example:

    .. parsed-literal::

        python -m dxlurlvoidservice config

Output
------

The output from starting the service should appear similar to the following:

    .. parsed-literal::

        Running application ...
        On 'run' callback.
        On 'load configuration' callback.
        Incoming message configuration: queueSize=1000, threadCount=10
        Message callback configuration: queueSize=1000, threadCount=10
        Attempting to connect to DXL fabric ...
        Connected to DXL fabric.
        Registering service: apivoidservice
        Registering request callbacks: /opendxl-apivoid/service/apivoid/iprep
        Registering request callback: /opendxl-apivoid/service/apivoid/iprep/stats
        Registering request callbacks: /opendxl-apivoid/service/apivoid/parkeddomain
        Registering request callback: /opendxl-apivoid/service/apivoid/parkeddomain/stats
        Registering request callbacks: /opendxl-apivoid/service/apivoid/domainbl
        Registering request callback: /opendxl-apivoid/service/apivoid/domainbl/stats
        Registering request callbacks: /opendxl-apivoid/service/apivoid/domainage
        Registering request callback: /opendxl-apivoid/service/apivoid/domainage/stats
        Registering request callbacks: /opendxl-apivoid/service/apivoid/threatlog
        Registering request callback: /opendxl-apivoid/service/apivoid/threatlog/stats
        Registering request callbacks: /opendxl-apivoid/service/apivoid/sslinfo
        Registering request callback: /opendxl-apivoid/service/apivoid/sslinfo/stats
        Registering request callbacks: /opendxl-apivoid/service/apivoid/emailverify
        Registering request callback: /opendxl-apivoid/service/apivoid/emailverify/stats
        Registering request callbacks: /opendxl-apivoid/service/apivoid/dnslookup
        Registering request callback: /opendxl-apivoid/service/apivoid/dnslookup/stats
        On 'DXL connect' callback.