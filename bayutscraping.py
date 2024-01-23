# import re
# import requests
# from bs4 import BeautifulSoup
# import json
# import csv

# url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
# page_numbers = [
#     '',
#     'page-2/'
# ]

# all_prices = []  # List to store all prices

# for page_number in page_numbers:
#     current_url = f'{url}{page_number}'  # Use a new variable to store the current URL

#     response = requests.get(current_url)

#     if response.status_code == 200:
#         html_content = response.text

#         soup = BeautifulSoup(html_content, 'html.parser')

#         script_tags = soup.find_all('script')

#         if len(script_tags) >= 4:
#             fourth_last_script = script_tags[-4]
#             fourth_last_script_content = fourth_last_script.get_text(strip=True)

#             json_match = re.search(r'({.*})', fourth_last_script_content)

#             if json_match:
#                 json_content = json_match.group(1)

#                 try:
#                     data_dict = json.loads(json_content)

#                     prices = re.findall(r'"price":\s*(\d+)', fourth_last_script_content)
#                     reference_numbers = re.findall(r'"referenceNumber":\s*"([^"]+)"', fourth_last_script_content)
#                     permit_numbers = re.findall(r'"permitNumber":\s*"([^"]+)"', fourth_last_script_content)
#                     titles = re.findall(r'"title":\s*"([^"]+)"', fourth_last_script_content)
#                     rooms = re.findall(r'"rooms":\s*(\d+)', fourth_last_script_content)
#                     baths = re.findall(r'"baths":\s*(\d+)', fourth_last_script_content)
#                     areas = re.findall(r'"area":\s*([\d.]+)', fourth_last_script_content)
#                     mobiles=re.findall(r'"mobile":\s*"([^"]+)"', fourth_last_script_content)
#                     phones=re.findall(r'"phone":\s*"([^"]+)"', fourth_last_script_content)
#                     whatsapps=re.findall(r'"whatsapp":\s*"([^"]+)"', fourth_last_script_content)
#                     proxyMobiles=re.findall(r'"proxyMobile":\s*"([^"]+)"', fourth_last_script_content)
#                     phone_numbers = re.findall(r'"phoneNumbers":\s*\["(\+\d+)"\]', fourth_last_script_content)
#                     mobile_numbers = re.findall(r'"mobileNumbers":\s*\["(\+\d+)"\]', fourth_last_script_content)
#                     contactNames = re.findall(r'"contactName":\s*"([^"]+)"', fourth_last_script_content)
#                     latitudes = re.findall(r'"lat":\s*([\d.]+)', fourth_last_script_content)
#                     longitudes = re.findall(r'"lng":\s*([\d.]+)', fourth_last_script_content)
#                     furnishingStatus = re.findall(r'"furnishingStatus":\s*"([^"]+)"', fourth_last_script_content)
#                     csv_file_path = 'apartment_data.csv'
#                     with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
#                         csv_writer = csv.writer(csv_file)

#                         # Writing headers
#                         csv_writer.writerow(['Price', 'Reference Number', 'Permit Number', 'titles', 'rooms', 'baths','areas','contactName','mobiles','phones','whatsapps'
#                                              ,'proxyMobiles','phone_numbers','mobile_numbers','latitudes','longitudes','furnishingStatus'])

#                         # Writing data for one apartment
#                         csv_writer.writerow([prices, reference_numbers, permit_numbers, titles, rooms, baths,areas,contactNames,mobiles,phones,whatsapps,
#                                              proxyMobiles,phone_numbers,mobile_numbers,latitudes,longitudes,furnishingStatus])

#                     print(f"Data saved to {csv_file_path}")

#                 except json.JSONDecodeError as e:
#                     print(f"Error decoding JSON: {e}")
#             else:
#                 print("No valid JSON content found in the script.")

#         else:
#             print("There are not enough script tags on the page.")

#     else:
#         print(f"Failed to fetch the page. Status code: {response.status_code}")











# print(reference_number)
# print(permit_number)
# print(title)

# Extracting location data
# location_matches = re.findall(r'"location":\s*\[\s*{[^}]*"name":\s*"([^"]+)"', fourth_last_script_content)
# location_names = location_matches if location_matches else []
# print(location_names)

# locations = data_dict.get("algolia", {}).get("hits", [])[0].get("location", [])
# location_names = [location["name"] for location in locations]
# location_str = ", ".join(location_names)
# print(location_str)


# Extracting category data
# category_names = [category["name"] for category in data_dict.get("category", [])]
# category_str = ",".join(category_names)

# Writing data to CSV
# csv_file_path = 'apartment_data.csv'
# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
#     csv_writer = csv.writer(csv_file)

#     # Writing headers
#     csv_writer.writerow(['Price', 'Reference Number', 'Permit Number', 'Title', 'Location', 'Category'])

#     # Writing data for one apartment
#     csv_writer.writerow([price, reference_number, permit_number, title, location_str, category_str])

# print(f"Data saved to {csv_file_path}")



# import re
# import requests
# from bs4 import BeautifulSoup
# import json
# import csv
# import time

# url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
# page_numbers = [
#     '',
#     'page-2/'
# ]

# all_apartment_data = []  

# for page_number in page_numbers:
#     current_url = f'{url}{page_number}' 
    
#     response = requests.get(current_url)

#     if response.status_code == 200:
#         html_content = response.text

#         soup = BeautifulSoup(html_content, 'html.parser')

#         script_tags = soup.find_all('script')

#         if len(script_tags) >= 4:
#             fourth_last_script = script_tags[-4]
#             fourth_last_script_content = fourth_last_script.get_text(strip=True)

#             json_match = re.search(r'({.*})', fourth_last_script_content)

#             if json_match:
#                 json_content = json_match.group(1)

#                 try:
#                     data_dict = json.loads(json_content)

#                     prices = re.findall(r'"price":\s*(\d+)', fourth_last_script_content)
#                     reference_numbers = re.findall(r'"referenceNumber":\s*"([^"]+)"', fourth_last_script_content)
#                     permit_numbers = re.findall(r'"permitNumber":\s*"([^"]+)"', fourth_last_script_content)
#                     titles = re.findall(r'"title":\s*"([^"]+)"', fourth_last_script_content)
#                     rooms = re.findall(r'"rooms":\s*(\d+)', fourth_last_script_content)
#                     baths = re.findall(r'"baths":\s*(\d+)', fourth_last_script_content)
#                     areas = re.findall(r'"area":\s*([\d.]+)', fourth_last_script_content)
#                     mobiles = re.findall(r'"mobile":\s*"([^"]+)"', fourth_last_script_content)
#                     phones = re.findall(r'"phone":\s*"([^"]+)"', fourth_last_script_content)
#                     whatsapps = re.findall(r'"whatsapp":\s*"([^"]+)"', fourth_last_script_content)
#                     proxyMobiles = re.findall(r'"proxyMobile":\s*"([^"]+)"', fourth_last_script_content)
#                     phone_numbers = re.findall(r'"phoneNumbers":\s*\["(\+\d+)"\]', fourth_last_script_content)
#                     mobile_numbers = re.findall(r'"mobileNumbers":\s*\["(\+\d+)"\]', fourth_last_script_content)
#                     contactNames = re.findall(r'"contactName":\s*"([^"]+)"', fourth_last_script_content)
#                     latitudes = re.findall(r'"lat":\s*([\d.]+)', fourth_last_script_content)
#                     longitudes = re.findall(r'"lng":\s*([\d.]+)', fourth_last_script_content)
#                     furnishingStatus = re.findall(r'"furnishingStatus":\s*"([^"]+)"', fourth_last_script_content)

#                     all_apartment_data.append({
#                         'Price': prices[0] if prices else '',
#                         'Reference Number': reference_numbers[0] if reference_numbers else '',
#                         'Permit Number': permit_numbers[0] if permit_numbers else '',
#                         'Title': titles[0] if titles else '',
#                         'Rooms': rooms[0] if rooms else '',
#                         'Baths': baths[0] if baths else '',
#                         'Area': areas[0] if areas else '',
#                         'Mobile': mobiles[0] if mobiles else '',
#                         'Phone': phones[0] if phones else '',
#                         'Whatsapp': whatsapps[0] if whatsapps else '',
#                         'Proxy Mobile': proxyMobiles[0] if proxyMobiles else '',
#                         'Phone Number': phone_numbers[0] if phone_numbers else '',
#                         'Mobile Number': mobile_numbers[0] if mobile_numbers else '',
#                         'Contact Name': contactNames[0] if contactNames else '',
#                         'Latitude': latitudes[0] if latitudes else '',
#                         'Longitude': longitudes[0] if longitudes else '',
#                         'Furnishing Status': furnishingStatus[0] if furnishingStatus else ''
#                     })

#                 except json.JSONDecodeError as e:
#                     print(f"Error decoding JSON: {e}")
#             else:
#                 print("No valid JSON content found in the script.")

#         else:
#             print("There are not enough script tags on the page.")

#     else:
#         print(f"Failed to fetch the page. Status code: {response.status_code}")
#     time.sleep(3)

# csv_file_path = 'apartment_data.csv'
# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
#     csv_writer = csv.writer(csv_file)

#     csv_writer.writerow(['Price', 'Reference Number', 'Permit Number', 'Title', 'Rooms', 'Baths',
#                          'Area', 'Mobile', 'Phone', 'Whatsapp', 'Proxy Mobile', 'Phone Number',
#                          'Mobile Number', 'Contact Name', 'Latitude', 'Longitude', 'Furnishing Status'])

#     for apartment_data in all_apartment_data:
#         csv_writer.writerow([
#             apartment_data['Price'],
#             apartment_data['Reference Number'],
#             apartment_data['Permit Number'],
#             apartment_data['Title'],
#             apartment_data['Rooms'],
#             apartment_data['Baths'],
#             apartment_data['Area'],
#             apartment_data['Mobile'],
#             apartment_data['Phone'],
#             apartment_data['Whatsapp'],
#             apartment_data['Proxy Mobile'],
#             apartment_data['Phone Number'],
#             apartment_data['Mobile Number'],
#             apartment_data['Contact Name'],
#             apartment_data['Latitude'],
#             apartment_data['Longitude'],
#             apartment_data['Furnishing Status']
#         ])

# print(f"Data saved to {csv_file_path}")

import re
import requests
from bs4 import BeautifulSoup
import json
import csv
import time

url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
page_numbers = [
    '',
    'page-2/'
]

csv_file_path = 'apartment_data.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['Price', 'Reference Number', 'Permit Number', 'Title', 'Rooms', 'Baths',
                         'Area', 'Mobile', 'Phone', 'Whatsapp', 'Proxy Mobile', 'Phone Number',
                         'Mobile Number', 'Contact Name', 'Latitude', 'Longitude', 'Furnishing Status'])

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

                json_match = re.search(r'({.*})', fourth_last_script_content)

                if json_match:
                    json_content = json_match.group(1)

                    try:
                        data_dict = json.loads(json_content)

                        prices = re.findall(r'"price":\s*(\d+)', fourth_last_script_content)
                        reference_numbers = re.findall(r'"referenceNumber":\s*"([^"]+)"', fourth_last_script_content)
                        permit_numbers = re.findall(r'"permitNumber":\s*"([^"]+)"', fourth_last_script_content)
                        titles = re.findall(r'"title":\s*"([^"]+)"', fourth_last_script_content)
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
                        latitudes = re.findall(r'"lat":\s*([\d.]+)', fourth_last_script_content)
                        longitudes = re.findall(r'"lng":\s*([\d.]+)', fourth_last_script_content)
                        furnishingStatus = re.findall(r'"furnishingStatus":\s*"([^"]+)"', fourth_last_script_content)

                        # Write directly to CSV file for each apartment
                        for i in range(max(len(prices), len(reference_numbers), len(permit_numbers), len(titles), len(rooms),
                                        len(baths), len(areas), len(mobiles), len(phones), len(whatsapps), len(proxyMobiles),
                                        len(phone_numbers), len(mobile_numbers), len(contactNames), len(latitudes), len(longitudes),
                                        len(furnishingStatus))):
                            csv_writer.writerow([
                                prices[i] if i < len(prices) else '',
                                reference_numbers[i] if i < len(reference_numbers) else '',
                                permit_numbers[i] if i < len(permit_numbers) else '',
                                titles[i] if i < len(titles) else '',
                                rooms[i] if i < len(rooms) else '',
                                baths[i] if i < len(baths) else '',
                                areas[i] if i < len(areas) else '',
                                mobiles[i] if i < len(mobiles) else '',
                                phones[i] if i < len(phones) else '',
                                whatsapps[i] if i < len(whatsapps) else '',
                                proxyMobiles[i] if i < len(proxyMobiles) else '',
                                phone_numbers[i] if i < len(phone_numbers) else '',
                                mobile_numbers[i] if i < len(mobile_numbers) else '',
                                contactNames[i] if i < len(contactNames) else '',
                                latitudes[i] if i < len(latitudes) else '',
                                longitudes[i] if i < len(longitudes) else '',
                                furnishingStatus[i] if i < len(furnishingStatus) else ''
                            ])

                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                else:
                    print("No valid JSON content found in the script.")

            else:
                print("There are not enough script tags on the page.")

        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")

        # Introduce a delay of, for example, 2 seconds between requests
        time.sleep(2)

print(f"Data saved to {csv_file_path}")
