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
from .models import ApartmentDetail,BuildingInformation,ProjectInformation,ValidatedInformation,PropertyDetail
import pandas as pd


def insert_data_from_csv():
    try:
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csvfiles/source_file_data.csv')
        df = pd.read_csv(csv_file_path,header=0)
        for index, row in df.iterrows():
            apartment_id = row['id']
            if not ApartmentDetail.objects.filter(apartment_id=apartment_id).exists():
                data = {
                    'apartment_id': row['id'],
                    'price': row['Price'],
                    'rooms': row['Rooms'],
                    'baths': row['Baths'],
                    'area': row['Area'],
                    'furnishing_status': row['Furnishing Status'],
                    'latitude': row['Latitude'],
                    'longitude': row['Longitude'],
                }
                apartment_detail = ApartmentDetail(**data)
                apartment_detail.save()
                print(f"Inserted data for apartment with ID {row.get('id')}")
    except FileNotFoundError:
        print(f"File {csv_file_path} not found.")

def insert_building_data_from_csv():
    try:
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csvfiles/building_information2.csv')
        df = pd.read_csv(csv_file_path, header=0)
        for index, row in df.iterrows():
            building_id = row['id']
            if not BuildingInformation.objects.filter(building_id=building_id).exists():
                data = {
                    'building_id': building_id,
                    'building_name': row['Building Name'],
                    'year_of_completion': row['Year of Completion'],
                    'total_floors': row['Total Floors'],
                    'swimming_pools': row['Swimming Pools'],
                    'total_parking_spaces': row['Total Parking Spaces'],
                    'elevators': row['Elevators']
                }
                building_information = BuildingInformation(**data)
                building_information.save()
            if pd.isnull(building_id):
                print(f"Skipping row {index} due to missing id value.")
                continue
            try:
                building_id = int(building_id)
            except ValueError:
                print(f"Skipping row {index} due to non-integer id value: {building_id}")
                continue
    except FileNotFoundError:
        print(f"File {csv_file_path} not found.")


def get_valid_value(value):
    if isinstance(value, str):
        if value.strip() == '':
            return ''
        else:
            return ' '.join(value.split())
    else:
        return value

def read_existing_ids(csv_file_path):
    existing_ids = set()
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            existing_ids.add(int(row[0]))  
    return existing_ids

def update_source_file_data():
    url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
    page_numbers = [''] + [f'page-{i}/' for i in range(2, 25)]
    current_directory = os.path.dirname(os.path.abspath(__file__))
    bayutdata_directory = os.path.dirname(current_directory)
    media_directory = os.path.join(bayutdata_directory, 'media')
    directory_path = os.path.join(media_directory, 'csvfiles')
    os.makedirs(directory_path, exist_ok=True)
    csv_file_path = os.path.join(directory_path, 'source_file_data.csv')
    existing_source_file_ids = read_existing_ids(csv_file_path)
    
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        for page_number in page_numbers:
            # current_url = f'{url}{page_number}'
            current_url = f'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/{page_number}'
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
                            ids = [int(id.strip()) for ids_string in listing_ids for id in re.findall(r'\d{7}', ids_string)]
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
                            
                            for i, id in enumerate(ids):
                                if id not in existing_source_file_ids:
                                    csv_writer.writerow([
                                        get_valid_value(id),
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


def insert_project_data_from_csv():
    try:
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csvfiles/project_information2.csv')
        df = pd.read_csv(csv_file_path, header=0)
        new_df = df.dropna()
        for index, row in new_df.iterrows():
            project_id = str(row['id']).strip()
            if not ProjectInformation.objects.filter(project_id=project_id).exists():
                data = {
                    'project_id': project_id,
                    'project_name': row['Project Name'],
                    'last_inspected': row['Last Inspected'],
                    'completion': row['Completion'],
                    'handover': row['Handover'],
                }
                project_information = ProjectInformation(**data)
                project_information.save()
            if pd.isnull(project_id):
                print(f"Skipping row {index} due to missing id value.")
                continue
            try:
                project_id = int(project_id)
            except ValueError:
                print(f"Skipping row {index} due to non-integer id value: {project_id}")
                continue
    except FileNotFoundError:
        print(f"File {csv_file_path} not found.")


def insert_validated_data_from_csv():
    try:
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csvfiles/validated_information2.csv')
        df = pd.read_csv(csv_file_path, header=0)
        for index, row in df.iterrows():
            validated_id = str(row['id']).strip()
            if not ValidatedInformation.objects.filter(validated_id=validated_id).exists():
                data = {
                    'validated_id': validated_id,
                    'developer': row['Developer'],
                    'ownership': row['Ownership'],
                    'built_up_area': row['Built-up Area'],
                    'usage': row['Usage'],
                    'balcony_size': row['Balcony Size'],
                    'total_building_area': row['Total Building Area'],
                    'parking_availability': row['Parking Availability']
                }
                validated_information = ValidatedInformation(**data)
                validated_information.save()
            if pd.isnull(validated_id):
                print(f"Skipping row {index} due to missing id value.")
                continue
            try:
                validated_id = int(validated_id)
            except ValueError:
                print(f"Skipping row {index} due to non-integer id value: {validated_id}")
                continue
    except FileNotFoundError:
        print(f"File {csv_file_path} not found.")


def insert_property_detail_from_csv():
    try:
        property_detail=PropertyDetail.objects.all()
        property_detail.delete()
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csvfiles/property_details.csv')
        df = pd.read_csv(csv_file_path, header=0)
        for index, row in df.iterrows():
            property_id = str(row['id']).strip()
            if not PropertyDetail.objects.filter(property_id=property_id).exists():
                completion_value = row['Completion']
                if pd.isna(completion_value) or completion_value.strip() == "":
                    completion_value = "Ready"  
                data = {
                    'property_id': property_id,
                    'type': row['Type'],
                    'purpose': row['Purpose'],
                    'completion': completion_value,
                    'added_on': row['Added on'],
                    'rent_frequency':row['Rent_Frequency'],
                }
                property_information = PropertyDetail(**data)
                property_information.save()
            if pd.isnull(property_id):
                print(f"Skipping row {index} due to missing id value.")
                continue
            try:
                property_id = int(property_id)
            except ValueError:
                print(f"Skipping row {index} due to non-integer id value: {property_id}")
                continue
    except FileNotFoundError:
        print(f"File {csv_file_path} not found.") 