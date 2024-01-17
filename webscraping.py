from bs4 import BeautifulSoup
import requests
import csv

url = 'https://www.investing.com/equities/nike'
response = requests.get(url)
def write_to_csv(data, file_path='output.csv'):
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')  
    dives = soup.find_all('div', class_='min-w-0')
    if dives:
        for div in dives:
            name = div.find('h1')
            if name:
                data=([name.get_text(strip=True)])
                write_to_csv(['NAME'])
                write_to_csv(data)

    dives1 = soup.find_all('dl', class_='flex-1 sm:mr-8')
    if dives1:
        for div in dives1:
            div_elements = div.find_all('div')  
            if div_elements:
                for div_element in div_elements:
                    dt_elements = div_element.find_all('dt') 
                    dd_elements = div_element.find_all('dd')
                    min_length = min(len(dt_elements), len(dd_elements))
                    for i in range(min_length):
                        heading = dt_elements[i].find('span')
                        data = dd_elements[i].find('span')

                        if heading and data:
                            heading_text = heading.get_text(strip=True)
                            data_text = data.get_text(strip=True)
                            write_to_csv([heading_text])
                            write_to_csv([data_text])
    else:
        print('Error: Unable to find required elements on the page.')

else:
    print(f'Error: Unable to fetch the URL. Status code: {response.status_code}')
