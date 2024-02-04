import csv
import re
import requests
from bs4 import BeautifulSoup

new_url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
page_numbers = [
    '',
    'page-2/',
    'page-3/',
    'page-4/',
    'page-5/',
    'page-6/',
    'page-7/',
    'page-8/',
    'page-9/',
    'page-10/',
    'page-11/',
    'page-12/',
    'page-13/',
    'page-14/',
    'page-15/',
    'page-16/',
    'page-17/',
    'page-18/',
    'page-19/',
    'page-20/',
    'page-21/',
    'page-22/',
    'page-23/',
    'page-24/'
]

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
            return None
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

csv_file_path1 = 'property_information.csv'
project_info_headers = ['id', 'property_detail']

with open(csv_file_path1, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(project_info_headers)

    for page_number in page_numbers:
        current_url = f'{new_url}{page_number}'
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
                    if listing_ids:
                        listing_ids = [int(id.strip()) for id in listing_ids[0].split(',')]
                        for i in range(len(listing_ids)):
                            url = f'https://www.bayut.com/property/details-{listing_ids[i]}.html'
                            property_info = extract_property_information(url)
                            if property_info:
                                csv_writer.writerow([listing_ids[i], property_info])







