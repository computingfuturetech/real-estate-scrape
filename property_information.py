import csv
import re
import requests
from bs4 import BeautifulSoup
import os

new_url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
page_numbers = [''] + [f'page-{i}/' for i in range(2, 25)]

def extract_property_information(url, listing_id):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        property_info_dict = {'id': listing_id}

        property_info = soup.find_all('ul', class_='_033281ab')
        rent_frquency_info=soup.find_all('span', class_='_56562304')
        if property_info:
            for value in property_info:
                li_tags = value.find_all('li')
                for li_tag in li_tags:
                    span_tags = li_tag.find_all('span')
                    if len(span_tags) >= 2:
                        first_span_value = span_tags[0].text.strip()
                        second_span_value = span_tags[1].text.strip()
                        if first_span_value in project_info_headers:
                            property_info_dict[first_span_value] = second_span_value
        if rent_frquency_info:
            for value in rent_frquency_info:
                span_tag = value.text.strip()
                if span_tag:
                    property_info_dict['Rent_Frequency'] = span_tag
        else:
            property_info_dict['Rent_Frequency'] = ''
                   
        return property_info_dict
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

csv_file_path = 'property_information.csv'
project_info_headers = ['id', 'Type','Purpose','Completion','Added on','Rent_Frequency']

with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=project_info_headers)
    csv_writer.writeheader()

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
                        for listing_id in listing_ids:
                            url = f'https://www.bayut.com/property/details-{listing_id}.html'
                            property_info = extract_property_information(url, listing_id)
                            if property_info:
                                    print(property_info)
                                    csv_writer.writerow(property_info)
