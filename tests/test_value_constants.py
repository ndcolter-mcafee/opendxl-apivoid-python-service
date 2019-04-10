import os

TEST_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))
APIVOID_CONFIG_FILENAME = TEST_FOLDER + "/dxlapivoidservice.config"

SAMPLE_API_KEY = '0123456789abcdef'
HTTP_ERROR_SERVER_PATH = "/test/http/error"

SAMPLE_HOST = '027.ru'
SAMPLE_IP = '1.2.3.4'
SAMPLE_ACTION = 'dns-a'

SAMPLE_STATS_REMAINED = {
    "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
    "credits_remained": 24.92,
    "elapsed_time": "0.02",
    "estimated_queries": "311",
    "success": True
}

SAMPLE_IP_REP = {
    "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
    "credits_remained": 24.92,
    "data": {
        "report": {
            "anonymity": {
                "is_hosting": False,
                "is_proxy": False,
                "is_tor": False,
                "is_vpn": False,
                "is_webproxy": False
            },
            "blacklists": {
                "detection_rate": "0%",
                "detections": 0,
                "engines": {
                    "0": {
                        "detected": False,
                        "elapsed": "0.04",
                        "engine": "EFnet_RBL",
                        "reference": "http://rbl.efnetrbl.org/multicheck.php"
                    },
                    "1": {
                        "detected": False,
                        "elapsed": "0.24",
                        "engine": "MegaRBL",
                        "reference": "https://www.megarbl.net/check"
                    }
                },
                "engines_count": 2,
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
    "success": True
}

SAMPLE_DOMAIN_REP = {
    "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
    "credits_remained": 24.84,
    "data": {
        "report": {
            "alexa_top_100k": False,
            "alexa_top_10k": False,
            "alexa_top_250k": False,
            "blacklists": {
                "detection_rate": "0%",
                "detections": 0,
                "engines": {
                    "0": {
                        "confidence": "low",
                        "detected": False,
                        "elapsed": "0.00",
                        "engine": "Phishing Test",
                        "reference": "https://www.novirusthanks.org/"
                    },
                    "1": {
                        "confidence": "low",
                        "detected": False,
                        "elapsed": "0.00",
                        "engine": "Scam Test",
                        "reference": "https://www.novirusthanks.org/"
                    }
                },
                "engines_count": 2,
                "scantime": "0.74"
            },
            "domain_length": 6,
            "most_abused_tld": False
        }
    },
    "elapsed_time": "0.85",
    "estimated_queries": "310",
    "success": True
}

SAMPLE_DNS_LOOKUP = {
    "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
    "credits_remained": 24.72,
    "data": {
        "records": {
            "count": 1,
            "found": True,
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
    "success": True
}

SAMPLE_SSL_INFO = {
    "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
    "credits_remained": 24.65,
    "data": {
        "certificate": {
            "debug_message": "Failed to connect to host on port 443",
            "found": False
        }
    },
    "elapsed_time": "0.23",
    "estimated_queries": "352",
    "success": True
}

SAMPLE_THREATLOG = {
    "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
    "credits_remained": 24.6,
    "data": {
        "threatlog": {
            "detected": False,
            "scantime": "0.00"
        }
    },
    "elapsed_time": "0.13",
    "estimated_queries": "492",
    "success": True
}

SAMPLE_EMAIL_VERIFY = {
    "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
    "credits_remained": 24.49,
    "data": {
        "alexa_top_10k": False,
        "common_domain": False,
        "dirty_words": False,
        "disposable": False,
        "has_mx_records": True,
        "mistyped_domain": False,
        "risky_tld": False,
        "suggested_domain": ""
    },
    "elapsed_time": "0.67",
    "estimated_queries": "408",
    "success": True
}

SAMPLE_DOMAIN_AGE = {
    "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
    "credits_remained": 23.99,
    "data": {
        "domain_age_in_days": 4865,
        "domain_creation_date": "2005-12-08"
    },
    "elapsed_time": "0.51",
    "estimated_queries": "47",
    "success": True
}

SAMPLE_PARKED_DOMAIN = {
    "credits_expiration": "Sat, 8 Apr 2019 20:51:14 GMT",
    "credits_remained": 23.49,
    "data": {
        "parked_domain": False
    },
    "elapsed_time": "1.51",
    "estimated_queries": "46",
    "success": True
}
