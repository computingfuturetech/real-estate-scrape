from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import re
import requests
import os

def scrape_and_write_data(url, headers, csv_file_path):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)
        target_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_208d68ae')))
        if target_element:
            target_element.click()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_84dd8fa0')))
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            div_information = soup.find_all('div', class_='_208d68ae')
            if div_information:
                all_information = soup.find_all('ul', class_='_84dd8fa0')
                if all_information:
                    data_row = [listing_ids[i]] + ['NA'] * (len(headers) - 1)
                    file_exists = os.path.isfile(csv_file_path)
                    file_empty = not file_exists or os.path.getsize(csv_file_path) == 0

                    existing_ids = []
                    if file_exists and not file_empty:
                        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
                            csv_reader = csv.reader(csv_file)
                            csv_header = next(csv_reader)  
                            for row in csv_reader:
                                if any(',' in value for value in row):
                                    existing_ids.append(row[0].strip())
                                    continue    
                                existing_ids.append(row[0].strip())

                    if str(listing_ids[i]) not in existing_ids:
                        for value in all_information:
                            li_tags = value.find_all('li')
                            for li_tag in li_tags:
                                span_tags = li_tag.find_all('span')
                                if len(span_tags) >= 2:
                                    first_span_value = span_tags[0].text.strip()
                                    second_span_value = span_tags[1].text.strip()
                                    if first_span_value in headers:
                                        index = headers.index(first_span_value)
                                        data_row[index] = second_span_value

                        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
                            csv_writer = csv.writer(csv_file)
                            if file_empty:
                                csv_writer.writerow(headers)
                            csv_writer.writerow(data_row)
        else:
            print("Target element not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()



def read_existing_ids(csv_file_path):
    existing_ids = set()
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            existing_ids.add(int(row[0]))  
    return existing_ids

existing_building_ids = read_existing_ids('building_information2.csv')
existing_validated_ids = read_existing_ids('validated_information2.csv')
existing_project_ids = read_existing_ids('project_information2.csv')


new_url = 'https://www.bayut.com/to-rent/apartments/dubai/dubai-marina/?rent_frequency=daily'
page_numbers = [''] + [f'page-{i}/' for i in range(2, 7)]

for page_number in page_numbers:
        current_url = f'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/{page_number}?rent_frequency=daily'
        # current_url = f'{new_url}{page_number}'
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
                        csv_file_path1 = 'building_information2.csv'
                        csv_file_path2 = 'validated_information2.csv'
                        csv_file_path3 = 'project_information2.csv'
                        

                        building_info_headers = ['id', 'Building Name', 'Year of Completion', 'Total Floors', 'Swimming Pools',
                                'Total Parking Spaces', 'Total Building Area', 'Elevators','Retail Centres']

                        validated_info_headers = ['id', 'Developer', 'Ownership', 'Built-up Area', 'Usage',
                                'Balcony Size', 'Total Building Area', 'Parking Availability']

                        project_info_headers = ['id', 'Project Name', 'Project Status', 'Last Inspected',
                                'Completion', 'Handover']

                        
                        for i in range(len(listing_ids)):
                            if listing_ids[i] in existing_building_ids or listing_ids[i] in existing_validated_ids or listing_ids[i] in existing_project_ids:
                                continue
                            url = f'https://www.bayut.com/property/details-{listing_ids[i]}.html'
                            scrape_and_write_data(url, building_info_headers, csv_file_path1)
                            scrape_and_write_data(url, validated_info_headers, csv_file_path2)
                            scrape_and_write_data(url, project_info_headers, csv_file_path3)






