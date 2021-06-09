import logging
import os
import argparse
import http
import sys
from config import PayChexAPIPayload, HubSpotAPIKEY, proxy_dict
from utils import find_in_content, map_fields, to_hubspot_format, company_custom_field_details
from paychex_api import PayChexAPI
from hubspot_api import HubspotWrapper
from datetime import datetime
dir_path = os.path.dirname(os.path.realpath(__file__))


logging.basicConfig(
    format="[%(asctime)s > %(module)s:%(lineno)d %(levelname)s] =>  %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
logger = logging.getLogger()

# logging.basicConfig(filename=os.path.join(dir_path, datetime.now().strftime(
#     "%d_%m_%Y.log")), filemode='w', format='%(name)s - %(levelname)s - %(message)s')

companyId = '00Z1IQF9IB6EJRFDEGED'
paychex_api_instance = PayChexAPI(
    payload=PayChexAPIPayload, json_response=True, retries=3, timeout=60)
hubsport_api_instance = HubspotWrapper(api_key=HubSpotAPIKEY)
retries = 3

def get_company_worker_details(company_workers, filter_active_workers=True, hubspot_format=True):

    # adding workers fields details
    for cw in company_workers['content']:

        # get communication details
        cw['communications'] = paychex_api_instance.worker_communications(
            cw['workerId'])

        worker_custom_fields = paychex_api_instance.worker_custom_fields(
            cw["workerId"])
        for wcf in worker_custom_fields['content']:
            wcf.update(company_custom_field_details(
                key='customFieldId', value=wcf['customFieldId']
            ))
        cw['custom_fields'] = worker_custom_fields

        cw_mapped = map_fields(o=cw)
        if hubspot_format:
            if filter_active_workers and cw_mapped.get('continue_to_contact') == 'Yes':
                logger.info(
                    f"[Worker: {cw_mapped.get('id_number')}] continue_to_contact is Yes [action:create]")
                yield {'worker': to_hubspot_format(cw_mapped), 'action': 'create'}
            else:
                logger.info(
                    f"[Worker: {cw_mapped.get('id_number')}] continue_to_contact is No, [action:delete]")
                yield {'worker': to_hubspot_format(cw_mapped), 'action': 'delete'}
        else:
            yield {'worker': cw}


def _run(limit, offset, import_to_hubspot=True, filter_active_workers=True):
    workers = []
    hubspot_contacts = []
    total = limit

    # fetch/refresh token
    paychex_api_instance.fetch_oauth_token(refresh=True)

    # get all workers in a given company
    if int(limit) == 0:
        logger.info(f"No Limit provided, fetching all workers ...")
        company_workers = paychex_api_instance.company_workers(
            companyId)
        total = company_workers['metadata']['contentItemCount']
    else:
        company_workers = paychex_api_instance.company_workers(
            companyId, limit=str(limit), offset=str(offset))
    company_worker_details = get_company_worker_details(
        company_workers=company_workers, filter_active_workers=filter_active_workers, hubspot_format=True
    )

    if import_to_hubspot:
        i = 1
        for worker_detail in company_worker_details:
            worker = worker_detail['worker']
            action = worker_detail['action']
            logger.info(f"Uploading [Company-Worker] of {i}/{total} ...\n")
            workers.append(worker)
            
            tries = 1
            err = {'response': 'ok'}
            hubspot_contact = {}
            
            while(tries <= retries):          
                try:
                    hubspot_contact = hubsport_api_instance.contact_upload(
                    worker, action)
                    break
                except  http.client.HTTPException as e:
                    tries+=1
                    logger.error(f"HubSpot HTTPException :: {e}, retrying [{tries}/{retries}]...")
                    # hubsport_api_instance = HubspotWrapper(api_key=HubSpotAPIKEY)
                    err['response'] = 'error'
                    
            success = hubspot_contact.get('vid')
            response = hubspot_contact.get(
                'response') if action == 'delete' else err.get('response', 'ok')
            logger.info(f"Success: {success} Response: {response}\n")
            hubspot_contacts.append(hubspot_contact)
            i += 1
    else:
        workers = list(company_worker_details)

    return dict(workers=workers, hubspot_contacts=hubspot_contacts)


# ================================================================
# _cli_opts
# ================================================================
def _cli_opts():
    '''
    Parse command line options.
    @returns the arguments
    '''
    mepath = os.path.abspath(sys.argv[0]).encode('utf-8')
    mebase = os.path.basename(mepath)

    description = '''
    Main Program to Fetch Workers From PayChex API
    '''

    parser = argparse.ArgumentParser(prog=mebase,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=description,
                                     )

    parser.add_argument('-i', '--import_to_hubspot',
                        default=True,
                        type=lambda x: (str(x).lower() == 'true'),
                        help='Import To Hubspot Flag')
    parser.add_argument('-l', '--limit',
                        default=0,
                        type=int,
                        help='Limit')
    parser.add_argument('-offset', '--offset',
                        default=0,
                        type=int,
                        help='Offset')
    parser.add_argument('-f', '--filter_active_workers',
                        default=True,
                        type=lambda x: (str(x).lower() == 'true'),
                        help='Filter out in active workers')

    args = parser.parse_args()
    return args


# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    args = _cli_opts()
    logger.info(
        "Started Run at: {}\n[limit -> '{}' | offset -> '{}' | import_to_hubspot -> {} | filter_active_workers -> {} ]".format(
            datetime.now().strftime("%c"), args.limit, args.offset, args.import_to_hubspot, args.filter_active_workers))
    print(
        _run(args.limit, args.offset, args.import_to_hubspot,
             args.filter_active_workers)
    )
