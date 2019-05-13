"""
    Analytics from GC
"""

import datetime
from google.cloud import bigquery


print(datetime.datetime.now())
CLIENT = bigquery.Client.from_service_account_json(
    "credentials/fir-analyticssample-59ed7-bb6f13508dae.json")


DATA_SETS = list(CLIENT.list_datasets())
print(DATA_SETS)


development_data_set = None
for data_set in DATA_SETS:
    if data_set.dataset_id == "analytics_188981975":
        print(data_set)
        development_data_set = data_set
        break


def initiate_analytics():
    """
        Initiate analytics
    """
    input_date = str(datetime.datetime.strftime(
        datetime.datetime.now() - datetime.timedelta(1), '%Y%m%d'))

    print("Getting data for date: " + input_date)

    table_name = 'events_' + input_date
    # table_name = 'events_20190501'

    print(table_name)

    query = """
        SELECT * FROM `%s.%s.%s` WHERE platform = 'ANDROID' and 
        event_name = 'select_content'""" % (development_data_set.project,
                                                              development_data_set.dataset_id,
                                                              table_name)
    print(query)
    return CLIENT.query(query).result()
