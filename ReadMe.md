



Usage: python main.py' [-h] [-i IMPORT_TO_HUBSPOT] [-l LIMIT] [-offset OFFSET]

    Main Program to Fetch Workers From PayChex API

    optional arguments:
    -h, --help            show this help message and exit
    -i IMPORT_TO_HUBSPOT, --import_to_hubspot IMPORT_TO_HUBSPOT
                            Import To Hubspot Flag
    -l LIMIT, --limit LIMIT
                            Limit
    -offset OFFSET, --offset OFFSET
                        Offset

# Upload first five records
    Example : python main.py --l 5 --o 0 --i 'true'

# Upload all records (it will create/update workers whose <continue to work> field is <Yes> and deletes workers whose <continue to work> field is <No> from HubSpot )
    Example : python main.py --l 5 --o 0 --i 'true'
