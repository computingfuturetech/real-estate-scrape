import csv
import requests
from bs4 import BeautifulSoup


base_url = 'https://www.investing.com/equities/'
brand_names = [
    'nike',
    'coca-cola-co',
    'microsoft-corp',
    '3m-co',
    'american-express',
    'amgen-inc',
    'apple-computer-inc',
    'boeing-co',
    'cisco-sys-inc',
    'goldman-sachs-group',
    'ibm',
    'intel-corp',
    'jp-morgan-chase',
    'mcdonalds',
    'salesforce-com',
    'verizon-communications',
    'visa-inc',
    'wal-mart-stores',
    'disney',
]
file = open('output.csv', 'a', newline='', encoding='utf-8')
writer = csv.writer(file)

def scraping():
    url = f'{base_url}{brand_names[0]}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        headings= soup.find_all('dt', class_='font-semibold text-[#181C21] flex-1')
        if headings:
            header_row = []
            header_row.extend(heading.text.strip() for heading in headings)
            writer.writerow(header_row)
        else:
            print("Not found")

    for brand_name in brand_names:
        url = f'{base_url}{brand_name}'
        response = requests.get(url) 
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            name_tag = soup.find('h1', class_='text-xl text-left font-bold leading-7 md:text-3xl md:leading-8 mb-2.5 md:mb-2 text-[#232526] rtl:soft-ltr')
            name = name_tag.text.strip() if name_tag else 'N/A'
            all_data = soup.find_all('dd', class_='text-[#232526] whitespace-nowrap')
            if all_data:
                data_values = [name]

                for data in all_data:
                    value = data.text.strip()
                    data_values.append(value)
                writer.writerow(data_values)
            else:
                print("Data not found")
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
    file.close()
scraping()



