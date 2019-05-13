import time
import analytics_from_gc
import json_parser

ANALYTICS_JSON = analytics_from_gc.initiate_analytics()
FILE_NAME = 'analyticsfiles/' + ('ANALYTICS_' + str(int(time.time()))).strip()

print("Current File Path:" + FILE_NAME)
json_parser.convert_from_json(ANALYTICS_JSON, FILE_NAME)
