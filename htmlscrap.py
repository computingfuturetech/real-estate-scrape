import re
import requests
from bs4 import BeautifulSoup
import csv
import json

url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'

with open('output.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    def property_information():
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tags = soup.find_all('script')
            
            if script_tags:
                first_script = script_tags[0] 
                first_script_content = first_script.get_text(strip=True)
                json_match = re.search(r'({.*})', first_script_content)
                if json_match:
                    try:
                        # listing_ids = re.findall(r'"listing_id":\s*\[([^\]]+)]', first_script_content)
                        # if listing_ids:
                        #     listing_ids = [int(id.strip()) for id in listing_ids[0].split(',')]  # Convert to list of integers
                        #     print("Number of Listing IDs:", len(listing_ids))
                        #     for i in range(len(listing_ids)):
                            #   new_url=f'https://www.bayut.com/property/details-{listing_ids[i]}.html'
                        new_url=f'https://www.bayut.com/property/details-8376239.html'
                        response = requests.get(new_url)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            property_information = soup.find_all('ul', class_='_033281ab')
                            if property_information:
                                for data in property_information:
                                    li_tags = data.find_all('li')
                                    for li_tag in li_tags:
                                        span_tags = li_tag.find_all('span')
                                        if len(span_tags) >= 2:
                                            second_span_value = span_tags[1].text.strip()
                                            print(second_span_value)
                        else:
                            print("No listing_id found.")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                else:
                    print("No valid JSON content found in the script.")
            else:
                print("No <script> tags found on the page.")

    # property_information()

    def building_information():
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tags = soup.find_all('script')
            
            if script_tags:
                first_script = script_tags[0] 
                first_script_content = first_script.get_text(strip=True)
                json_match = re.search(r'({.*})', first_script_content)
                if json_match:
                    try:
                        new_url=f'https://www.bayut.com/property/details-8376239.html'
                        response = requests.get(new_url)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            building_information = soup.find_all('ul', class_='_84dd8fa0')
                            if building_information:
                                print("Found")
                            else:
                                print("Not Found")
                                # for data in building_information:
                                #     li_tags = data.find_all('li')
                                #     for li_tag in li_tags:
                                #         span_tags = li_tag.find_all('span')
                                #         if len(span_tags) >= 2:
                                #             second_span_value = span_tags[1].text.strip()
                                #             print(second_span_value)
                        else:
                            print("No listing_id found.")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                else:
                    print("No valid JSON content found in the script.")
            else:
                print("No <script> tags found on the page.")
        
    building_information()


    


