import re
import requests
from bs4 import BeautifulSoup
import csv
import json

url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'

with open('output.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    def scraping():
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
                        listing_ids = re.findall(r'"listing_id":\s*\[([^\]]+)]', first_script_content)
                        if listing_ids:
                            listing_ids = [int(id.strip()) for id in listing_ids[0].split(',')]  # Convert to list of integers
                            print("Number of Listing IDs:", len(listing_ids))
                            for i in range(len(listing_ids)):
                              new_url=f'https://www.bayut.com/property/details-{listing_ids[i]}.html'
                              response = requests.get(new_url)
                              if response.status_code == 200:
                                  soup = BeautifulSoup(response.content, 'html.parser')
                                #   property_information = soup.find_all('ul', class_='_033281ab')
                                #   if property_information:
                                #     for data in property_information:
                                #         li_tags = data.find_all('li')
                                #         for li_tag in li_tags:
                                #             span_tags = li_tag.find_all('span')
                                #             if len(span_tags) >= 2:
                                #                 second_span_value = span_tags[1].text.strip()
                                #                 print(second_span_value)
                                  validated_information = soup.find_all('div', class_='_208d68ae')
                                  if validated_information:
                                     for div_tag in validated_information:
                                        ul_tags = div_tag.find_all('ul')
                                        if ul_tags:
                                            for li_tag in ul_tags:
                                                li_tags = li_tag.find_all('li')
                                                if li_tags:
                                                    for span_tag in li_tags:
                                                        span_tags = span_tag.find_all('span')
                                                        if len(span_tags) >= 2:
                                                            second_span_value = span_tags[1].text.strip()
                                                            print(second_span_value)
                                                        # if span_tags:
                                                        #     print("Find")
                                            #    if len(span_tags) >= 2:
                                            #         second_span_value = span_tags[1].text.strip()
                                            #         print(second_span_value)
                                          
                                    #  for data in validated_information:
                                    #      value = data.text.strip()
                                    #      print(value)
                                        # div_tags = data.find_all('div',class_='a7cd24f7')
                                        # if div_tags:
                                        #     print("Found")
                                        # for div_tag in div_tags:
                                        #     value=div_tag.text.strip()
                                        #     print(value)
                                    #         span_tags = div_tag.find_all('span')
                                    #         if len(span_tags) >= 1:
                                    #             first_span_value = span_tags[0].text.strip()
                                    #             print(first_span_value)


                        else:
                            print("No listing_id found.")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                else:
                    print("No valid JSON content found in the script.")
            else:
                print("No <script> tags found on the page.")

    # scraping()

    def find_validated_information():
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
                        new_url=f'https://www.bayut.com/property/details-8191142.html'
                        response = requests.get(new_url)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            # validated_information = soup.find_all('div', class_='a808fc60')
                            # if validated_information:
                                # print(validated_information)
                            fourth_div = soup.select('div ul li')# Assuming you want the fourth div (index 3)
                            for x in fourth_div:
                                print(x.text.strip())
                                    # if fourth_div:
                                    #     third_div_within_fourth = fourth_div.find_all('div')[2]  # Assuming you want the third div within the fourth div (index 2)
                                    #     if third_div_within_fourth:
                                    #         print(third_div_within_fourth)
                                    #     else:
                                    #         print("Third div within the fourth div not found in the current element")
                                    # else:
                                    #     print("Fourth div not found in the current element")
                                
                                    # for li_tag in ul_tag:
                                    #     li_tags = li_tag.find_all('li',class_='_783e1309')
                                    #     print(li_tags)
                                #         if li_tags:
                                #             for span_tag in li_tags:
                                #                 span_tags = span_tag.find_all('span')
                                #                 if len(span_tags) >= 2:
                                #                     second_span_value = span_tags[1]
                                                    # second_span_soup = BeautifulSoup(str(second_span_value), 'html.parser')
                                                    # div_tags = second_span_soup.find_all('div')
                                                    # for div_outer in second_span_value:
                                                    #     div1=div_outer.find_all('div')
                                                    #     if div1:
                                                    #        print("find")
                                                        #    div2 = div1.find('div')
                                                        #    if div2:
                                                        #     print("find")
                                                        #    else:
                                                        #         print("No second nested div found in div1")
                                                        # else:
                                                        #     print("No div1 found in the current element")
                                                        # if div1:
                                                        #    for div in div1:
                                                            # div2 = div1.find('div')
                                                            # if div2:
                                                        #            print("find")
                                                    #     value=div.text.strip()
                                                                # print("Find")
                        else:
                            print("No listing_id found.")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                else:
                    print("No valid JSON content found in the script.")
            else:
                print("No <script> tags found on the page.")
    find_validated_information()


# https://fenix-data-es2.dubizzle.com/_msearch?filter_path=took%2C*.took%2C*.suggest.*.options.text%2C*.suggest.*.options._source.*%2C*.hits.total.*%2C*.hits.hits._source.*%2C*.hits.hits._score%2C*.hits.hits.highlight.*%2C*.error%2C*.aggregations.*.buckets.key%2C*.aggregations.*.buckets.doc_count%2C*.aggregations.*.buckets.complex_value.hits.hits._source%2C*.aggregations.*.filtered_agg.facet.buckets.key%2C*.aggregations.*.filtered_agg.facet.buckets.doc_count%2C*.aggregations.*.filtered_agg.facet.buckets.complex_value.hits.hits._source