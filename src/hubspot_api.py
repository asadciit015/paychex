from hubspot3 import Hubspot3
from api_wrapper import logging as logger
from config import HubSpotAPIKEY


class HubspotWrapper(Hubspot3):

    def __init__(self, *args, **kwargs):
        logger.info(
            "HubspotWrapper Initiated !!!\n"
        )
        super().__init__(*args, **kwargs)

    def contact_upload(self, data=None, action='create', **options):
        """create,update,delete a contact"""
        options['timeout'] = 60
        data = data or {}

        contact_id_number = " ".join(
            [p['value'] for p in data['properties'] if p['property'] in ('id_number',)]) or None
        contact_name = " ".join([p['value'] for p in data['properties'] if p['property'] in (
            'firstname', 'lastname',)]) or None
        contact_email = " ".join(
            [p['value'] for p in data['properties'] if p['property'] in ('email',)]) or None

        if contact_email:
            sr = self.contacts.search(contact_email, **options)
        elif contact_name:
            sr = self.contacts.search(contact_name, **options)
        else:
            sr = []

        if len(sr) > 0:
            contact_id = sr[0]['vid']
            action = 'update' if action.lower().strip() == 'create' else action.lower().strip()
        else:
            contact_id = None
        

        if contact_id:
            logger.info(
                f"[Action:{action}] for Existing Contact => 'contact_id:{contact_id}' [id_number:{contact_id_number} name:{contact_name} email:{contact_email}] ..."
            )
            if action.lower().strip() == 'update':
                # r = b''
                r = str(self.contacts.update_by_id(
                    contact_id, data, **options))
            elif action.lower().strip() == 'delete':
                r = str(self.contacts.delete_a_contact(
                    contact_id, **options))
            return {'vid': contact_id, 'response': r}
        else:
            if action.lower().strip() == 'delete':
                logger.info(
                    f"[Action:{action}] for No Contact Found =>  [id_number:{contact_id_number} name:{contact_name} email:{contact_email}] ..."
                )
                return {'vid': None, 'response': 'Not Found'}
            else:
                logger.info(
                    f"[Action:{action}] for New Contact =>  [id_number:{contact_id_number} name:{contact_name} email:{contact_email}] ..."
                )
                return self.contacts.create(data, **options)


# if __name__ == '__main__':
#     client = HubspotWrapper(api_key=HubSpotAPIKEY)
#     from mapping_test import map_fields, workers
#     workers = list(map(map_fields, workers_api_response['content']))
