import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
import logging
logging.basicConfig(
    format="[%(asctime)s > %(module)s:%(lineno)d %(levelname)s] =>  %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
config_logger = logging.getLogger()


PayChexAPIPayload = dict(
    grant_type= os.getenv("PAYCHEX_GRANT_TYPE"),
    client_id= os.getenv("PAYCHEX_CLIENT_ID"),
    client_secret= os.getenv("PAYCHEX_CLIENT_SECRET")
)

# Automatic Nursing Care Services Inc
HubSpotAPIKEY = os.getenv("HubSpotAPIKEY")


proxy_host = "51.81.82.175:50"
proxy_host = "167.172.180.46:41039"  # Elite	United States
# proxy_host = "96.44.188.194:8020"	#Elite	United States

proxy_dict = {
    #   "http"  : f"https://{proxy_host}",
    "https": f"http://{proxy_host}",
}


def check_config_or_raise_error():
    valid = True
    if not os.getenv("PAYCHEX_GRANT_TYPE"):
        logging.error(f"[PAYCHEX_GRANT_TYPE] not provided!")
        valid = False
    if not os.getenv("PAYCHEX_CLIENT_ID"):
        logging.error(f"[PAYCHEX_CLIENT_ID] not provided!")
        valid = False
    if not os.getenv("PAYCHEX_CLIENT_SECRET"):
        logging.error(f"[PAYCHEX_CLIENT_SECRET] not provided!")
        valid = False
    if not os.getenv("HubSpotAPIKEY"):
        logging.error(f"[HubSpotAPIKEY] not provided!")
        valid = False
    if not valid:
        exit(1)
    
check_config_or_raise_error()