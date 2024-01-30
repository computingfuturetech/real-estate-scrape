from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import re
import requests

new_url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
response = requests.get(new_url)

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
                listing_ids = [int(id.strip()) for id in listing_ids[0].split(',')]  # Convert to list of integers
                print("Number of Listing IDs:", len(listing_ids))

                # Set the header outside the loop
                csv_file_path = 'building_information.csv'
                building_info_headers = ['id', 'Building Name', 'Year of Completion', 'Total Floors', 'Swimming Pools',
                                         'Total Parking Spaces', 'Total Building Area', 'Elevators', 'abc']

                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(building_info_headers)  # Write header only once

                    for i in range(len(listing_ids)):
                        url = f'https://www.bayut.com/property/details-{listing_ids[i]}.html'
                        driver = webdriver.Chrome()

                        try:
                            driver.get(url)
                            wait = WebDriverWait(driver, 10)
                            target_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_208d68ae')))

                            if target_element:
                                target_element.click()
                                wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_84dd8fa0')))
                                page_source = driver.page_source
                                soup = BeautifulSoup(page_source, 'html.parser')

                                div_information = soup.find_all('div', class_='_208d68ae')
                                if div_information:
                                    for data in div_information:
                                        h2_tag = data.find_all('h2')
                                        if h2_tag:
                                            for value in h2_tag:
                                                name = value.text.strip()
                                                if name == 'Building Information':
                                                    building_information = soup.find_all('ul', class_='_84dd8fa0')
                                                    if len(building_information) > 1:
                                                        data_row = [listing_ids[i]] + ['NA'] * (
                                                                len(building_info_headers) - 1)
                                                        for value in building_information:
                                                            li_tags = value.find_all('li')
                                                            for li_tag in li_tags:
                                                                span_tags = li_tag.find_all('span')
                                                                if len(span_tags) >= 2:
                                                                    first_span_value = span_tags[0].text.strip()
                                                                    second_span_value = span_tags[1].text.strip()
                                                                    if first_span_value in building_info_headers:
                                                                        index = building_info_headers.index(
                                                                            first_span_value)
                                                                        data_row[index] = second_span_value

                                                        csv_writer.writerow(data_row)  

                            else:
                                print("Target element not found.")
                        except Exception as e:
                            print(f"An error occurred: {e}")
                        finally:
                            driver.quit()
