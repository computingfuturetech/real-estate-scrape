import re
import requests
from bs4 import BeautifulSoup
import json
import csv
import time

url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
page_numbers = [''] + [f'page-{i}/' for i in range(2, 25)]

csv_file_path = 'source_file_data1.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['id','Price', 'Reference Number', 'Permit Number', 'Title', 'Rooms', 'Baths',
                         'Area', 'Mobile','Phone','Whatsapp','Proxy_mobile','Phone_number','Mobile_number', 'Contact Name', 'Latitude', 'Longitude', 'Furnishing Status'])

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
                        for i in range(max(len(prices), len(reference_numbers), len(permit_numbers), len(titles), len(rooms),
                                        len(baths), len(areas), len(mobiles), len(phones), len(whatsapps), len(proxyMobiles),
                                        len(phone_numbers), len(mobile_numbers), len(contactNames), len(latitudes), len(longitudes),
                                        len(furnishingStatus))):
                            csv_writer.writerow([
                                ids[i] if i < len(ids) else '',
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

print(f"Data saved to {csv_file_path}")
