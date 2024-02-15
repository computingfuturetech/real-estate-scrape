from datetime import datetime
from django.conf import settings
from datetime import date,timedelta
import re
import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import os
import pandas as pd



def get_valid_value(value):
    if value is None or value.strip() == '':
        return ''
    else:
        # Replace consecutive commas with a single comma
        return ' '.join(value.split())


def update_source_file_data():
    url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
    page_numbers = [''] + [f'page-{i}/' for i in range(2, 25)]
    current_directory = os.path.dirname(os.path.abspath(__file__))
    bayutdata_directory = os.path.dirname(current_directory)
    media_directory = os.path.join(bayutdata_directory, 'media')
    directory_path = os.path.join(media_directory, 'csvfiles')
    os.makedirs(directory_path, exist_ok=True)
    csv_file_path = os.path.join(directory_path, 'source_file_data.csv')
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(['id', 'Price', 'Reference Number', 'Permit Number', 'Title', 'Rooms', 'Baths',
                             'Area', 'Mobile', 'Phone', 'Whatsapp', 'Proxy_mobile', 'Phone_number', 'Mobile_number',
                             'Contact Name', 'Latitude', 'Longitude', 'Furnishing Status'])

        for page_number in page_numbers:
            current_url = f'{url}{page_number}'

            response = requests.get(current_url)

            if response.status_code == 200:
                html_content = response.text

                soup = BeautifulSoup(html_content, 'html.parser')

                script_tags = soup.find_all('script')

                if len(script_tags) >= 4:
                    fourth_last_script = script_tags[-4]
                    fourth_last_script_content = fourth_last_script.get_text(strip=True)
                    first_script = script_tags[0]
                    first_script_content = first_script.get_text(strip=True)
                    json_match = re.search(r'({.*})', fourth_last_script_content)

                    if json_match:
                        json_content = json_match.group(1)

                        try:
                            data_dict = json.loads(json_content)
                            listing_ids = re.findall(r'"listing_id":\s*\[([^\]]+)]', first_script_content)
                            ids = [id for ids_string in listing_ids for id in re.findall(r'\d{7}', ids_string)]
                            prices = re.findall(r'"price":\s*(\d+)', fourth_last_script_content)
                            reference_numbers = re.findall(r'"referenceNumber":\s*"([^"]+)"', fourth_last_script_content)
                            permit_numbers = re.findall(r'"permitNumber":\s*"([^"]+)"', fourth_last_script_content)
                            titles = re.findall(r'"projectNumber":\s*[^,]+,\s*"title":\s*"([^"]+)"', fourth_last_script_content)
                            rooms = re.findall(r'"rooms":\s*(\d+)', fourth_last_script_content)
                            baths = re.findall(r'"baths":\s*(\d+)', fourth_last_script_content)
                            areas = re.findall(r'"area":\s*([\d.]+)', fourth_last_script_content)
                            mobiles = re.findall(r'"mobile":\s*"([^"]+)"', fourth_last_script_content)
                            phones = re.findall(r'"phone":\s*"([^"]+)"', fourth_last_script_content)
                            whatsapps = re.findall(r'"whatsapp":\s*"([^"]+)"', fourth_last_script_content)
                            proxyMobiles = re.findall(r'"proxyMobile":\s*"([^"]+)"', fourth_last_script_content)
                            phone_numbers = re.findall(r'"phoneNumbers":\s*\["(\+\d+)"\]', fourth_last_script_content)
                            mobile_numbers = re.findall(r'"mobileNumbers":\s*\["(\+\d+)"\]', fourth_last_script_content)
                            contactNames = re.findall(r'"contactName":\s*"([^"]+)"', fourth_last_script_content)
                            latitudes = re.findall(r'"state":\s*[^,]+,\s*"geography":\s*{\s*"lat":\s*([\d.]+)', fourth_last_script_content)
                            longitudes = re.findall(r'"state":\s*[^,]+,\s*"geography":\s*{\s*"lat":\s*[^,]+,\s*"lng":\s*([\d.]+)', fourth_last_script_content)
                            furnishingStatus = re.findall(r'"furnishingStatus":\s*"([^"]+)"', fourth_last_script_content)
                            for i in range(max(len(ids), len(prices), len(reference_numbers), len(permit_numbers), len(titles), len(rooms),
                                                len(baths), len(areas), len(mobiles), len(phones), len(whatsapps), len(proxyMobiles),
                                                len(phone_numbers), len(mobile_numbers), len(contactNames), len(latitudes), len(longitudes),
                                                len(furnishingStatus))):
                                if i < len(ids):
                                    csv_writer.writerow([
                                        get_valid_value(ids[i]),
                                        get_valid_value(prices[i]) if i < len(prices) else '',
                                        get_valid_value(reference_numbers[i]) if i < len(reference_numbers) else '',
                                        get_valid_value(permit_numbers[i]) if i < len(permit_numbers) else '',
                                        get_valid_value(titles[i]) if i < len(titles) else '',
                                        get_valid_value(rooms[i]) if i < len(rooms) else '',
                                        get_valid_value(baths[i]) if i < len(baths) else '',
                                        get_valid_value(areas[i]) if i < len(areas) else '',
                                        get_valid_value(mobiles[i]) if i < len(mobiles) else '',
                                        get_valid_value(phones[i]) if i < len(phones) else '',
                                        get_valid_value(whatsapps[i]) if i < len(whatsapps) else '',
                                        get_valid_value(proxyMobiles[i]) if i < len(proxyMobiles) else '',
                                        get_valid_value(phone_numbers[i]) if i < len(phone_numbers) else '',
                                        get_valid_value(mobile_numbers[i]) if i < len(mobile_numbers) else '',
                                        get_valid_value(contactNames[i]) if i < len(contactNames) else '',
                                        get_valid_value(latitudes[i]) if i < len(latitudes) else '',
                                        get_valid_value(longitudes[i]) if i < len(longitudes) else '',
                                        get_valid_value(furnishingStatus[i]) if i < len(furnishingStatus) else ''
                                    ])

                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                    else:
                        print("No valid JSON content found in the script.")

                else:
                    print("There are not enough script tags on the page.")

            else:
                print(f"Failed to fetch the page. Status code: {response.status_code}")

    print(f"Data saved to {csv_file_path}")



# update_source_file_data()

# def preprocess_data(dataframe):
#     for col in dataframe.columns:
#         if dataframe[col].dtype == 'float64':
#             dataframe[col] = dataframe[col].fillna(0).astype(int)
#             dataframe[col] = dataframe[col].astype(str).apply(lambda x: x.rstrip('.0'))
#         if col.endswith(''):
#             dataframe.rename(columns={col: col[:-2]}, inplace=True)
#     return dataframe


# def merge_source_file_data():
#     update_source_file_data()
#     print("Waiting for 10 seconds before merging and deleting the new source file data...")
#     time.sleep(10)

    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # bayutdata_directory = os.path.dirname(current_directory)
    # media_directory = os.path.join(bayutdata_directory, 'media')
    # directory_path = os.path.join(media_directory, 'csvfiles')
    # new_source_file_path = os.path.join(directory_path, 'new_source_file_data.csv')
    # source_file_path = os.path.join(directory_path, 'source_file_data.csv')

#     try:
#         csv_files = [source_file_path, new_source_file_path]
#         dataframes = [pd.read_csv(file) for file in csv_files]
#         for i in range(len(dataframes)):
#             dataframes[i] = preprocess_data(dataframes[i])

#         for df_index, df in enumerate(dataframes):
#             df.columns = df.columns.str.lower().str.strip()

#         # Check if both DataFrames have the 'id' column
#         if 'id' not in dataframes[0] or 'id' not in dataframes[1]:
#             print("One or both DataFrames do not have the 'id' column.")
#             return

#         # Perform merge
#         merged_df = pd.merge(dataframes[0], dataframes[1], on='id', how='inner')
#         merged_df.to_csv(source_file_path, index=False)
#         if os.path.exists(new_source_file_path):
#             os.remove(new_source_file_path)
#             print("New source file data deleted.")
#         print("Merge operation completed successfully.")
#     except Exception as e:
#         print("Error occurred during merge operation:")
#         print(e)

# def merge_source_file_data():
#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     bayutdata_directory = os.path.dirname(current_directory)
#     media_directory = os.path.join(bayutdata_directory, 'media')
#     directory_path = os.path.join(media_directory, 'csvfiles')
#     new_source_file_path = os.path.join(directory_path, 'new_source_file_data.csv')
#     source_file_path = os.path.join(directory_path, 'source_file_data.csv')
#     csv_files = [new_source_file_path, source_file_path]

#     if csv_files:
#         print("Found")

#     dataframes = [pd.read_csv(file) for file in csv_files]
#     for df_index, df in enumerate(dataframes):
#         df.columns = df.columns.str.lower().str.strip()
#         print(f"DataFrame {df_index+1} columns:")
#         print(df.columns)
#         print()

#     # Rename columns of the second DataFrame to match the columns of the first DataFrame
#     dataframes[1].rename(columns=dict(zip(dataframes[1].columns, dataframes[0].columns)), inplace=True)

#     # Merge DataFrames with suffixes and without changing column names
#     merged_df = pd.merge(dataframes[0], dataframes[1], on='id', how='inner')
#     merged_df.to_csv(source_file_path, index=False)





# merge_source_file_data()