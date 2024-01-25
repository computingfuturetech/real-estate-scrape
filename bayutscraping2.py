import re
import requests
from bs4 import BeautifulSoup
import json
import csv

url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
page_numbers = [
    '',
    # 'page-2/',
    # Add more page numbers if needed
]

csv_file_path = 'apartment_data.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['Price', 'Reference Number', 'Permit Number', 'Title', 'Rooms', 'Baths',
                         'Area', 'Phone_number_list', 'Contact Name', 'Latitude', 'Longitude', 'Furnishing Status'])

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
                        titles = re.findall(r'"projectNumber":\s*[^,]+,\s*"title":\s*"([^"]+)"', fourth_last_script_content)
                        rooms = re.findall(r'"rooms":\s*(\d+)', fourth_last_script_content)
                        baths = re.findall(r'"baths":\s*(\d+)', fourth_last_script_content)
                        areas = re.findall(r'"area":\s*([\d.]+)', fourth_last_script_content)
                        phone_number_list = re.findall(r'"phoneNumber":\s*\{"mobile":\s*"([^"]+)",\s*"phone":\s*"([^"]+)",\s*"whatsapp":\s*"([^"]+)",\s*"proxyMobile":\s*"([^"]+)"', fourth_last_script_content)
                        print(phone_number_list)
                        # for i in len(phone_number_list):
                        #     print(phone_number_list[i])
                        # print(len(phone_number_list))
                        contactNames = re.findall(r'"contactName":\s*"([^"]+)"', fourth_last_script_content)
                        latitudes = re.findall(r'"state":\s*[^,]+,\s*"geography":\s*{\s*"lat":\s*([\d.]+)', fourth_last_script_content)
                        longitudes = re.findall(r'"state":\s*[^,]+,\s*"geography":\s*{\s*"lat":\s*[^,]+,\s*"lng":\s*([\d.]+)', fourth_last_script_content)
                        furnishingStatus = re.findall(r'"furnishingStatus":\s*"([^"]+)"', fourth_last_script_content)

                        # Write directly to CSV file for each apartment
                        for i in range(max(len(prices), len(reference_numbers), len(permit_numbers), len(titles), len(rooms),
                                        len(baths), len(areas), len(phone_number_list), len(contactNames), len(latitudes), len(longitudes),
                                        len(furnishingStatus))):
                            csv_writer.writerow([
                                prices[i] if i < len(prices) else '',
                                reference_numbers[i] if i < len(reference_numbers) else '',
                                permit_numbers[i] if i < len(permit_numbers) else '',
                                titles[i] if i < len(titles) else '',
                                rooms[i] if i < len(rooms) else '',
                                baths[i] if i < len(baths) else '',
                                areas[i] if i < len(areas) else '',
                                phone_number_list[i][0] if i < len(phone_number_list) else '',  # mobile
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

# print(f"Data saved to {csv_file_path}")