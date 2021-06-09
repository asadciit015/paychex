from api import API, logging as logger


class ProxyFinder(API):

	gimmeproxy_suffix 	= "https://gimmeproxy.com/api/getProxy"

	def __init__(self, *args, **kwargs):
		logger.info(f"INSTANCE INITIALIZED HERE FOR: {self.__class__.__name__}")

 
	def gimme_proxies(self, **kwargs):
		return self.perform_request(end_point=self.gimmeproxy_suffix, action="get", **kwargs)
        


proxy = ProxyFinder().gimme_proxies(get='true',supportsHttps='true',maxCheckPeriod='3600',country='US,GB')