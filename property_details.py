import csv
import re
import requests
from bs4 import BeautifulSoup

new_url = 'https://www.bayut.com/to-rent/apartments/dubai/dubai-marina/'
page_numbers = [''] + [f'page-{i}/' for i in range(2, 24)]


def extract_property_information(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        property_information = soup.find_all('span', class_='_2a806e1e')
        if property_information:
            property_info_text = ""
            for data in property_information:
                value = data.text.strip()
                property_info_text += value + "\n"
            property_info_lines = property_info_text.split('\n')
            property_info_lines = [line.strip() for line in property_info_lines if line.strip()]
            property_info_text = ' • '.join(property_info_lines)
        return property_info_text
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

csv_file_path1 = 'property_details.csv'
project_info_headers = ['id', 'rent_frequency', 'property_detail']

with open(csv_file_path1, 'a', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(project_info_headers)
    for page_number in page_numbers:
        current_url = f'{new_url}{page_number}?rent_frequency=daily'
        response = requests.get(current_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tags = soup.find_all('script')
            if script_tags:
                first_script = script_tags[0]
                first_script_content = first_script.get_text(strip=True)
                json_match = re.search(r'({.*})', first_script_content)
                if json_match:
                    listing_ids = re.findall(r'"listing_id":\s*\[([^\]]+)]', first_script_content)
                    rent_frequency = re.findall(r'"price_max":\s*[^,]+,\s*"rent_frequency":\s*"([^"]+)"', first_script_content)
                    if listing_ids:
                        listing_ids = [int(id.strip()) for id in listing_ids[0].split(',')]
                        if rent_frequency and len(rent_frequency) == 1:
                            rent_frequency = rent_frequency[0]
                            for i in range(len(listing_ids)):
                                url = f'https://www.bayut.com/property/details-{listing_ids[i]}.html'
                                property_info = extract_property_information(url)
                                if property_info:
                                    csv_writer.writerow([listing_ids[i], rent_frequency, property_info])








