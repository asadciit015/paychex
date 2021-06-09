from utils import PrintJson, find_in_content, map_fields


workers_api_response = {'metadata': {'contentItemCount': 1},
    'content': [{'workerId': '004UWBZQKOLSVMXZ68PJ',
                    'employeeId': '1278',
                    'workerType': 'INDEPENDENT_CONTRACTOR',
                    'employmentType': 'PART_TIME',
                    'exemptionType': 'NON_EXEMPT',
                    'workState': 'MD',
                    'birthDate': '1959-09-26T00:00:00Z',
                    'sex': 'FEMALE',
                    'hireDate': '2021-05-12T00:00:00Z',
                    'name': {'familyName': 'Appiah', 'givenName': 'Kate'},
                    'legalId': {'legalIdType': 'SSN', 'legalIdValue': '219739357'},
                    'locationId': '1090029319563308',
                    'job': {'jobTitleId': '1090031588820248', 'title': 'LPN'},
                    'organization': {'organizationId': '1090029319562963',
                                    'name': '700 Clinical Field',
                                    'number': '700',
                                    'links': []},
                    'currentStatus': {'workerStatusId': '00DWS906IMW2JSH8AQJD',
                                    'statusType': 'ACTIVE',
                                    'statusReason': 'BEGIN_CONTRACT',
                                    'effectiveDate': '2021-05-12T00:00:00Z'},
                    'links': [{'rel': 'self',
                            'href': 'https://api.paychex.com/workers/004UWBZQKOLSVMXZ68PJ'},
                            {'rel': 'communications',
                            'href': 'https://api.paychex.com/workers/004UWBZQKOLSVMXZ68PJ/communications'}],
                    'custom_fields': {'metadata': {'contentItemCount': 9},
                                    'content': [{'workerCustomFieldId': '1090041381333439',
                                                'customFieldId': '1090041381172077',
                                                'booleanValue': True,
                                                'customFieldName': 'Continue to contact',
                                                'categoryId': '1090040641759757',
                                                'required': True,
                                                'checkStub': False,
                                                'employeeEditable': False,
                                                'type': 'BOOLEAN',
                                                'categoryName': 'Scheduling'},
                                                {'workerCustomFieldId': '1090041341573389',
                                                'customFieldId': '1090041270075152',
                                                'booleanValue': False,
                                                'customFieldName': 'Far Western',
                                                'categoryId': '1090040641759757',
                                                'required': True,
                                                'checkStub': False,
                                                'employeeEditable': True,
                                                'type': 'BOOLEAN',
                                                'categoryName': 'Scheduling'},
                                                {'workerCustomFieldId': '1090041341573390',
                                                'customFieldId': '1090041270075195',
                                                'booleanValue': False,
                                                'customFieldName': 'Mid Western',
                                                'categoryId': '1090040641759757',
                                                'required': True,
                                                'checkStub': False,
                                                'employeeEditable': True,
                                                'type': 'BOOLEAN',
                                                'categoryName': 'Scheduling'},
                                                {'workerCustomFieldId': '1090041341573391',
                                                'customFieldId': '1090041270413968',
                                                'booleanValue': True,
                                                'customFieldName': 'Capital north',
                                                'categoryId': '1090040641759757',
                                                'required': True,
                                                'checkStub': False,
                                                'employeeEditable': True,
                                                'type': 'BOOLEAN',
                                                'categoryName': 'Scheduling'},
                                                {'workerCustomFieldId': '1090041341573392',
                                                'customFieldId': '1090041270413977',
                                                'booleanValue': False,
                                                'customFieldName': 'Capital South',
                                                'categoryId': '1090040641759757',
                                                'required': True,
                                                'checkStub': False,
                                                'employeeEditable': True,
                                                'type': 'BOOLEAN',
                                                'categoryName': 'Scheduling'},
                                                {'workerCustomFieldId': '1090041341573393',
                                                'customFieldId': '1090041270523205',
                                                'booleanValue': False,
                                                'customFieldName': 'Central',
                                                'categoryId': '1090040641759757',
                                                'required': True,
                                                'checkStub': False,
                                                'employeeEditable': True,
                                                'type': 'BOOLEAN',
                                                'categoryName': 'Scheduling'},
                                                {'workerCustomFieldId': '1090041341573394',
                                                'customFieldId': '1090041270523211',
                                                'booleanValue': False,
                                                'customFieldName': 'Southern',
                                                'categoryId': '1090040641759757',
                                                'required': True,
                                                'checkStub': False,
                                                'employeeEditable': True,
                                                'type': 'BOOLEAN',
                                                'categoryName': 'Scheduling'},
                                                {'workerCustomFieldId': '1090041341573395',
                                                'customFieldId': '1090041270519102',
                                                'booleanValue': False,
                                                'customFieldName': 'Upper Eastern Shore',
                                                'categoryId': '1090040641759757',
                                                'required': True,
                                                'checkStub': False,
                                                'employeeEditable': True,
                                                'type': 'BOOLEAN',
                                                'categoryName': 'Scheduling'},
                                                {'workerCustomFieldId': '1090041341573396',
                                                'customFieldId': '1090041270413989',
                                                'booleanValue': False,
                                                'customFieldName': 'Lower eastern shore',
                                                'categoryId': '1090040641759757',
                                                'required': True,
                                                'checkStub': False,
                                                'employeeEditable': True,
                                                'type': 'BOOLEAN',
                                                'categoryName': 'Scheduling'}],
                                    'links': []}}],
    'links': [{'rel': 'self',
                'href': 'https://api.paychex.com/workers/?companyid=00Z1IQF9IB6EJRFDEGED&employeeId=1278'}]}


if __name__ == '__main__':

    workers = list(map(map_fields, workers_api_response['content']))
    # workers = list(map(lambda workers_api_response: map_fields, ))

    PrintJson(workers)
