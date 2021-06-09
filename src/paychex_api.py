import requests, json, os
from pathlib import Path
from api_wrapper import APIWrapper, logging as logger
dir_path = os.path.dirname(os.path.realpath(__file__))

class PayChexAPI(APIWrapper):
    
    base_url = "https://api.paychex.com/"
    oauth_token_suffix = "auth/oauth/v2/token"
    company_workers_suffix = "companies/{}/workers"
    worker_suffix = "workers/{workerId}"
    worker_communications_suffix = "workers/{workerId}/communications"
    worker_custom_fields_suffix = "workers/{workerId}/customfields"
    company_custom_fields_suffix= "companies/{companyId}/customfields"
    company_custom_field_suffix = "companies/{companyId}/customfields/{customFieldId}"
    custom_field_worker_suffix = "workers/{workerId}/customfields/{workerCustomFieldId}"
    company_custom_fields_category_suffix = "companies/{companyId}/customfieldscategories/{categoryId}"
    company_custom_fields_categories_suffix = "companies/{companyId}/customfieldscategories"
    company_locations_suffix = "companies/{companyId}/locations"
    
    _out_dir = dir_path
    __oauth_token = None
    __retries = 3
    
    def __init__(self, *args, **kwargs):
        kwargs['retries'] = kwargs.get('retries', 5)
        self.payload = kwargs.get("payload", {})
        if not self.payload:
            raise Exception("payload is required!")
        super().__init__(*args, **kwargs)
        

    @property
    def oauth_token(self):
        return self.__oauth_token or self.load_json("token")
    

    @property
    def api_headers(self):
        return {
                'Content-type':'application/json',
                'Accept':'application/json',
                'Authorization': f'{self.oauth_token["token_type"]} {self.oauth_token["access_token"]}'
            }


    @property
    def out_dir(self):
        """
        Default output directory
        """
        outdir = self._out_dir if self._out_dir.endswith("/") else f"{self._out_dir}/"
        Path(outdir).mkdir(parents=True, exist_ok=True)
        return outdir

    def export_json(self, obj, filename):
        fpath = self.out_dir + filename + '.json'
        with open(fpath, 'w', encoding='utf-8') as outfile:
            json.dump(obj, outfile, ensure_ascii=False, indent=4)
        logger.info("Exported Token to ({fpath})".format(fpath=fpath))
    

    def load_json(self, filename):
        json_loaded = {}
        fpath = self.out_dir + filename + '.json'
        with open(fpath) as json_file:
            json_loaded = json.load(json_file)
        return json_loaded


    def api_call(self, url, action, data=None, **params):
        error_response = None
        status_code = None
        try:
            return self.perform_request(
                end_point=url, action=action,
                headers=self.api_headers, data=data, **params
            )
        except requests.exceptions.HTTPError as err:
            error_response = err
            status_code = err.response.status_code
            logger.error(f"Http Error: {err}")
        except requests.exceptions.ConnectionError as err:
            error_response = err
            logger.error(f"Error Connecting: {err}")
        except requests.exceptions.Timeout as err:
            error_response = err
            logger.error(f"Timeout Error: {err}")
        except requests.exceptions.RequestException as err:
            error_response = err
            logger.error(f"OOps: Something Else: {err}")
        
        
        if status_code == 401:
            logger.info("Resetting Session ...")
            self.reset_session()
            self.fetch_oauth_token(True)
            return self.perform_request(
                end_point=url, action=action,
                headers=self.api_headers, data=data, **params
            )
                

    def fetch_oauth_token(self, refresh=True):
        if refresh:
            logger.info(f"Fetching oauth token via API")
            end_point = f"{self.base_url}{self.oauth_token_suffix}"
            resp = self.perform_request(
                end_point=end_point, action="post",
                **self.payload
            )
            self.export_json(resp, "token")
        else:
            logger.info("Fetching oauth token from Local Storage")
        self.__oauth_token =  self.load_json("token")


    


    def worker(self, workerId):
        """
        Information about a unique worker (employee and contractor) that your application has been granted access to.
        Currently workers that exist within Paychex Flex payroll will be available,
        future enhancements will make workers from other Paychex systems available.
        
        PATH PARAMETERS:
            workerId (required) type => string
            ID associated with desired worker.
        """
        return self.api_call(f"{self.base_url}{companyId}/customfieldscategories/{categoryId}", 'get')

    
    def company_locations(self, companyId):
        """
        Array of locations set at the company level.
        PATH PARAMETERS
            companyId
                required
                string
                The ID of the company.
        """
        return  self.api_call(
            url = f"{self.base_url}{self.company_locations_suffix.format(companyId=companyId)}",
            action = 'get')
        

    def company_workers(self, companyId, **params):
        """
        Array of workers (employee and contractor) for all of the companies 
        who are associated with a specific company that your application has been granted access to.
        The combination of query parameters to be used with this endpoint are as follows:
         1. givenname, familyname, legallastfour
         2. from, to (start date, end date) 
         3. employeeid 
         4. locationid 
         5. offset, limit (paging)
        """
        logger.info(f"Fetching company_workers: [companyId:{companyId}, params:{params}]")
        return self.api_call(
            url = f"{self.base_url}{self.company_workers_suffix.format(companyId)}",
            action = 'get', **params)
    
    
    def company_custom_fields(self, companyId):
        """
        Array of customFields Configured at the company level
        PATH PARAMETERS
            companyId
                required
                string
                ID associated with desired company.
        """
        return self.api_call(
            f"{self.base_url}{self.company_custom_fields_suffix.format(companyId=companyId)}", 'get'
        )

    def company_custom_field(self, companyId, customFieldId):
        """
        Information about a single CustomField.
        PATH PARAMETERS
            companyId
                required
                string
                ID associated with desired company.
            customFieldId
                required
                string
                ID associated with desired custom field.
        """
        return self.api_call(
            f"{self.base_url}{self.company_custom_field_suffix.format(companyId=companyId, customFieldId=customFieldId)}",
            'get'
        )

    
    def worker_custom_fields(self, workerId, action="get"):
        return self.api_call(f"{self.base_url}{self.worker_custom_fields_suffix.format(workerId=workerId)}", 'get')
    

    def custom_field_worker(self, workerId, workerCustomFieldId, action="get"):
        return self.api_call(
            f"{self.base_url}{self.custom_field_worker_suffix.format(workerId=workerId, workerCustomFieldId=workerCustomFieldId)}",
            'get'
        )

    
    def company_custom_fields_category(self, companyId, categoryId):
        """
        Information about a single CustomFieldsCategory.
        PATH PARAMETERS
            companyId
                required
                string
                ID associated with desired company.
            categoryId
                required
                string
                ID associated with desired category.
        """
        return self.api_call(
            f"{self.base_url}{self.company_custom_fields_category_suffix.format(companyId=companyId, categoryId=categoryId)}",
            'get'
        )
    
    
    def company_custom_fields_categories(self, companyId):
        """
        Array of CustomFieldsCategories Configured at the company level
        PATH PARAMETERS
            companyId
                required
                string
                ID associated with desired company.
        """
        return self.api_call(
            f"{self.base_url}{self.company_custom_fields_categories_suffix.format(companyId=companyId)}",
            'get'
        )
        
    
    def worker_communications(self, workerId):
        """
        Information about "Active" or "In-progress" workers communications.
        PATH PARAMETERS
            workerId
                required
                string
                The id assigned to the worker that workers are being requested for.
        """
        return self.api_call(
            f"{self.base_url}{self.worker_communications_suffix.format(workerId=workerId)}",
            'get'
        )
        