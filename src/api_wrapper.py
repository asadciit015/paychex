from urllib.parse import parse_qsl, urlsplit, urlencode
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from requests.api import head
from requests.auth import HTTPBasicAuth
import logging, json

DEFAULT_TIMEOUT = 60 # seconds


logging.basicConfig(
    format="[%(asctime)s > %(module)s:%(lineno)d %(levelname)s] =>  %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
api_logger = logging.getLogger()





class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
    

class APIWrapper(object):
    
    def __init__(self, *args, **kwargs):
        self.json_response = bool(kwargs.get("json_response", True)) 
        self.timeout = int(kwargs.get("timeout", DEFAULT_TIMEOUT))
        self.headers = kwargs.get("headers", {} )
        self.proxy = kwargs.get("proxy", {})
        
        # Supported HTTP Headers & Supported HTTP MIME Types
        self.headers = kwargs.get("headers", {})
        
        # Setup retry strategry
        self._retries = Retry(
            total= int(kwargs.get("retries", 3)),
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "POST", "OPTIONS", "TRACE"]
        )
        
        self._session = requests.Session()
        api_logger.info(
            "APIWrapper ARGS ::\n"
            f"\tjson_response => {self.json_response}\n"
            f"\ttimeout => {self.timeout}\n"
            f"\theaders => {self.headers}\n"
            f"\tproxy => {self.proxy}\n"
            f"\tretries => {self._retries}\n"
        )
    
    
    def reset_session(self):
        self._session = requests.Session()
    
    @staticmethod
    def get_url_query_dict(url):
        return (
            dict(parse_qsl(urlsplit(url).query))
            if url
            not in (
                "",
                None,
            )
            else {}
        )

    @staticmethod
    def gen_url_with_query_dict(url, **qs):
        uri = urlsplit(url)
        parsed_url = "{uri.scheme}://{uri.netloc}{uri.path}".format(uri=uri)
        parsed_url_qs = APIWrapper.get_url_query_dict(url)
        parsed_url_qs.update(**{k: v for k, v in qs.items() if v})
        parsed_url_qstr = urlencode(parsed_url_qs)
        return f"{parsed_url}?{parsed_url_qstr}"
    
    
    def get_request_method(self, action):
        if action.upper().strip()=="GET":
            return self._session.get
        elif action.upper().strip()=="POST":
            return self._session.post
        elif action.upper().strip()=="PUTS":
            return self._session.put
        elif action.upper().strip()=="DELETE":
            return self._session.delete
        else:
            raise ValueError(f"invalid action:{action} provided !")


    def make_request(
        self, url, action, headers={}, data=None, verify=True, **params
    ):
        request_method = self.get_request_method(action)
        # update class headers with provided headers
        headers.update(self.headers) 
        self._session.headers.update(headers)
        # Build HTTPadapter and mount for both http and https usage
        adapter = TimeoutHTTPAdapter(timeout=self.timeout, max_retries=self._retries)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)
        self._session.headers.update(self.headers)
        
        # api_logger.info(f"[Request Type:{request_method.__name__.upper()}] url => {url}\n")
        # api_logger.info(f"headers => {headers}\n")
        # api_logger.info(f"data => {data}\n")
        
        if request_method.__name__ == "get":
            return request_method(
                url=url,
                verify=verify,
                headers = headers,
                proxies=self.proxy,
                **params,
            )
        elif request_method.__name__ in ( "post", "put", "delete",):
            return request_method(
                url=url,
                verify=verify,
                headers = headers,
                data=data or {},
                proxies=self.proxy
            )
        else:
            raise ValueError("Invlaid/Empty options supplied to make_request !")
            
    
    def perform_request(self, end_point, action, headers={}, **kwargs):
        if action.upper().strip()=="GET":
            url = self.gen_url_with_query_dict(end_point, **kwargs) if kwargs else end_point
            r = self.make_request(url, action=action, headers=headers)
            r.raise_for_status()
            return r.json() if self.json_response else r.text
            return AttrDict(r.json()) if self.json_response else r.text

            
        else:
            if action.upper().strip()=="POST":
                r = self.make_request(end_point, action=action, headers=headers, data=kwargs)
                r.raise_for_status()
                return r.json() if self.json_response else r.text