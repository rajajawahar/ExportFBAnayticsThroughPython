import datetime
import json
import os

import send_mail as sendMail
import xlsxwriter

HEADERS_MAP = {"user_property_user_id": "User ID",
               "app_info_version": "App Version",
               "event_name": "Event",
               "item_name": "Action",
               "content_type":"Type",
               "firebase_screen_id":"FireBase ScreenID",
               "user_property_first_open_time":"Open Time",
               "device_info_mobile_model_name":"Mobile Model Name",
               "category":"Category",
               "city":"City",
               "country" : "Country",
               "region" : "Region",
               "firebase_screen_class":"Screen Name",
               "operating_system":"OS",
               "operating_system_version" : "OS Version",
               "item_id":"Item ID",
               "version" :"Version",
               "geo_info_region": "Region",
               "geo_info_country": "Country"}


def flatten_user_json(user_json, user_id):
    flat_json = {}
    prefix = "user_property_"

    print(user_json)

    for individual_json in user_json:
        key = prefix + individual_json['key']
        property_json = (individual_json['value'])

        if 'string_value' in property_json:
            flat_json[key] = property_json['string_value']
        if 'int_value' in property_json:
            flat_json[key] = property_json['int_value']
        if str(individual_json['key']) == 'user_id':
            flat_json[key] = user_id

    return json.dumps(flat_json)

def flatten_event_json(event_params):
    flat_json = {}
    print(event_params)

    for individual_json in event_params:
        key = individual_json['key']
        property_json = (individual_json['value'])

        if 'string_value' in property_json is not None :
            flat_json[key] = property_json['string_value']
            
        elif 'int_value' in property_json is not None :
            flat_json[key] = property_json['int_value']
        
    return json.dumps(flat_json)    


def flatten_input_info(input_json,required_key_set, message):
    flat_json = {}

    print("\n%s\n" % (message))
    print(input_json)

    for key in required_key_set:
        if key in input_json:
            flat_json[key] = input_json[key]

    return json.dumps(flat_json)


def convert_from_json(rows, file_path):
    field_names = [field.name for field in rows.schema]   
    events_dict_array = []
    for row in rows:
        # print(format_string.format(*row))
        user_properties, user_id, device_info, geo_info, app_info,event_name,event_params = extract_values(row,
                                                                                   field_names)
        #  Separting UserJSON from the list
        user_json = flatten_user_json(user_properties, user_id)

        #  Separting DeviceType from the list
        device_info_key_set = ["category", "operating_system", 
                               "operating_system_version"]

        device_json = flatten_input_info(device_info,
                                         device_info_key_set, "Device JSON")
        #  Separting GeoType from the list
        geo_json = flatten_input_info(geo_info, ["country", "region",
                                                              "city"], "GEO JSON")                                                          
        #  Separating Events From the list
        events_json = flatten_event_json(event_params)

        # Separting AppInfo from the list
        app_info_json = flatten_input_info(app_info,
                                           ["version"], "App JSON")

        single_entry = json.loads(user_json)
        single_entry.update(json.loads(device_json))
        single_entry.update(json.loads(geo_json))
        single_entry.update(json.loads(app_info_json))
        single_entry.update(json.loads(events_json))
        events_dict_array.append(single_entry)
    
    write_dict_array_to_excel_send_mail(events_dict_array, file_path + '.xls')


def print_values(newline, *args):
    if newline:
        for value in args:
            print(value)
            print('\n')
    else:
        for value in args:
            print(value)

def extract_values(row, field_names):
    event_name = row[field_names.index("event_name")]
    print(event_name)
    event_params = row[field_names.index("event_params")]
    user_id_index = field_names.index("user_id")
    user_id = row[user_id_index]
    user_properties = row[field_names.index("user_properties")]
    device_info = row[field_names.index("device")]
    geo_info = row[field_names.index("geo")]
    app_info = row[field_names.index("app_info")]
    
    print_values(False, [row, event_name, user_id_index, user_id,
                         user_properties, device_info, geo_info, app_info])

    return user_properties, user_id, device_info, geo_info, app_info,event_name,event_params


def write_dict_array_to_excel_send_mail(array_of_dict, output_path):
     # //Creating a WorkBook
    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet()

    dict_to_write = fetch_dict_to_write(array_of_dict)
    dict_key_list = list(set(dict_to_write))

    worksheet = write_to_worksheet(worksheet, dict_key_list, array_of_dict)

    workbook.close()
    workbook_size = os.stat(output_path).st_size
    # process_mail(workbook_size, output_path)


def process_mail(workbook_size, attachment_path):
    if workbook_size > 0:
        from_addr = "rajajawahar77@gmail.com"
        to_addr = "raja@tarkalabs.com"
        subject = "Mobile User Activity - " + \
            datetime.datetime.strftime(
                datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')
        body_message = "Hi, \n Greetings of the day!!. \n Attached sheet contains \
                        the details of the mobile user activity"

        print(body_message)

        sendMail.send_mail(from_addr, to_addr, subject,
                           body_message, attachment_path)
        return
    print("Unable to send email")


def write_to_worksheet(worksheet, dict_key_list, array_of_dict):
    row = 0
    col = 0
    for key in dict_key_list:
        if HEADERS_MAP.get(key):
            key = HEADERS_MAP[key]
        worksheet.write(0, col, key)
        col += 1

    for single_dict in array_of_dict:
        col = 0
        for key in dict_key_list:
            if key in single_dict:
                worksheet.write(row + 1, col, single_dict[key])
            col += 1
        row += 1

    return worksheet


def fetch_dict_to_write(array_of_dict):
    dict_to_write = {}

    for each_dict in array_of_dict:
        for key in each_dict.keys():
            if key not in dict_to_write:
                dict_to_write[key] = []
            dict_to_write[key].append(each_dict[key])
            print(dict_to_write)
    return dict_to_write
