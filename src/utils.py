import json
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class PrintJson(object):
    def __init__(self, dict):
        print(json.dumps(dict, indent=2))


class Object(dict):
    def __init__(self, *args, **kwargs):
        super(Object, self).__init__(*args, **kwargs)
        self.__dict__ = self


def load_json(path):
    json_loaded = {}
    with open(path) as json_file:
        json_loaded = json.load(json_file)
    return json_loaded


def find_in_content(content_arr_dict, key, value, content_arr_key='content'):
    content_arr_dict = content_arr_dict or {}
    return next((c for c in content_arr_dict.get(content_arr_key, []) if c[key] == value), {})


def map_fields(o):

    STREET_ADDRESS = find_in_content(
        o.get("communications", {}),
        'type', 'STREET_ADDRESS', 'content')

    EMAIL = find_in_content(
        o.get("communications", {}),
        'type', 'EMAIL', 'content')

    PHONE = find_in_content(
        o.get("communications", {}),
        'type', 'PHONE', 'content')

    MOBILE_PHONE = find_in_content(
        o.get("communications", {}),
        'type', 'MOBILE_PHONE', 'content')

    FAX = find_in_content(
        o.get("communications", {}),
        'type', 'FAX', 'content')

    Far_Western = find_in_content(
        o.get("custom_fields", {}),
        'customFieldName', 'Far Western', 'content')
    Mid_Western = find_in_content(
        o.get("custom_fields", {}),
        'customFieldName', 'Mid Western', 'content')
    Capital_North = find_in_content(
        o.get("custom_fields", {}),
        'customFieldName', 'Capital north', 'content')
    Capital_South = find_in_content(
        o.get("custom_fields", {}),
        'customFieldName', 'Capital South', 'content')
    Central = find_in_content(
        o.get("custom_fields", {}),
        'customFieldName', 'Central', 'content')
    Southern = find_in_content(
        o.get("custom_fields", {}),
        'customFieldName', 'Southern', 'content')
    Upper_Eastern_Shore = find_in_content(
        o.get("custom_fields", {}),
        'customFieldName', 'Upper Eastern Shore', 'content')
    Lower_Eastern_Shore = find_in_content(
        o.get("custom_fields", {}),
        'customFieldName', 'Lower eastern shore', 'content')
    Continue_To_Contact = find_in_content(
        o.get("custom_fields", {}),
        'customFieldName', 'Continue to contact', 'content')

    # to do: handle other types
    continue_to_contact = "Yes" if Continue_To_Contact and Continue_To_Contact.get(
        'type') == 'BOOLEAN' and Continue_To_Contact.get('booleanValue') == True else "No"
    far_western = "Yes" if Far_Western and Far_Western.get(
        'type') == 'BOOLEAN' and Far_Western.get('booleanValue') == True else "No"
    mid_western = "Yes" if Mid_Western and Mid_Western.get(
        'type') == 'BOOLEAN' and Mid_Western.get('booleanValue') == True else "No"
    capital_north = "Yes" if Capital_North and Capital_North.get(
        'type') == 'BOOLEAN' and Capital_North.get('booleanValue') == True else "No"
    capital_south = "Yes" if Capital_South and Capital_South.get(
        'type') == 'BOOLEAN' and Capital_South.get('booleanValue') == True else "No"
    central = "Yes" if Central and Central.get(
        'type') == 'BOOLEAN' and Central.get('booleanValue') == True else "No"
    southern = "Yes" if Southern and Southern.get(
        'type') == 'BOOLEAN' and Southern.get('booleanValue') == True else "No"
    upper_eastern_shore = "Yes" if Upper_Eastern_Shore and Upper_Eastern_Shore.get(
        'type') == 'BOOLEAN' and Upper_Eastern_Shore.get('booleanValue') == True else "No"
    lower_eastern_shore = "Yes" if Lower_Eastern_Shore and Lower_Eastern_Shore.get(
        'type') == 'BOOLEAN' and Lower_Eastern_Shore.get('booleanValue') == True else "No"

    mobile_phone = "({})-{}".format(MOBILE_PHONE.get('dialArea', ''), MOBILE_PHONE.get('dialNumber', '')
                                    ) if MOBILE_PHONE and MOBILE_PHONE.get('dialArea') and MOBILE_PHONE.get('dialNumber') else None
    home_phone = "({})-{}".format(PHONE.get('dialArea', ''), PHONE.get('dialNumber',
                                                                       '')) if PHONE and PHONE.get('usageType') == "HOME" else None
    work_phone = "({})-{}".format(PHONE.get('dialArea', ''), PHONE.get('dialNumber',

                                                                       '')) if PHONE and PHONE.get('usageType') == "WORK" else None

    return {
        "firstname": o.get('name', {}).get('givenName') or o.get('name', {}).get('companyName'),
        "lastname": o.get('name', {}).get('familyName'),
        # "Middle Name": o.get('name', {}).get('middleName', ''),
        # # "Full Name": "{0} {1} {2}".format(
        #     o.get('name', {}).get('givenName', ''),
        #     o.get('name', {}).get('middleName', ''),
        #     o.get('name', {}).get('familyName', '')
        # ).strip().replace('  ', ' '),
        "gender": o.get('sex'),
        "id_number": o.get('employeeId'),
        "address": STREET_ADDRESS.get('streetLineOne'),
        "city": STREET_ADDRESS.get('city'),
        "state": STREET_ADDRESS.get('countrySubdivisionCode'),
        "zip": STREET_ADDRESS.get('postalCode'),
        "mobilephone": mobile_phone,
        "phone": home_phone,
        "work_phone": work_phone,
        "email": EMAIL.get('uri') if EMAIL.get('usageType') == 'PERSONAL' else None,
        "work_email": EMAIL.get('uri') if EMAIL.get('usageType') == 'BUSINESS' else None,
        "continue_to_contact": continue_to_contact,
        "far_western": far_western,
        "mid_western": mid_western,
        "capital_north": capital_north,
        "capital_south": capital_south,
        "central": central,
        "southern": southern,
        "upper_eastern_shore": upper_eastern_shore,
        "lower_eastern_shore": lower_eastern_shore,
        "paychex_status": o.get('currentStatus', {}).get('statusType'),
        "jobtitle": o.get('job', {}).get('title'),
        "paychex_org": o.get('organization', {}).get('name'),
        "employee_type": o.get('workerType')
    }


def to_hubspot_format(d):
    return {
        "properties": [{"property": field, "value": value} for field, value in d.items() if value]
    }


def company_custom_field_details(key='customFieldId', value=None):
    csf =  [{k: v for k, v in c.items() if k in ('customFieldId', 'customFieldName', 'categoryId', 'type')} 
            for c in load_json(os.path.join(dir_path, "company_custom_fields.json"))['content']
            ]
    if csf and key and value:
        return next((item for i, item in enumerate(csf) if item[key] == value), {})
    else:
        return csf
        