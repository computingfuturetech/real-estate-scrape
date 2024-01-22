# from selenium import webdriver
# import json

# url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)

# try:
#     driver.get(url)
#     rendered_html = driver.page_source
#     start_index = rendered_html.find('window.state = {')
#     if start_index != -1:
#         json_data_str = rendered_html[start_index + len('window.state = {'):]
#         end_index = json_data_str.find('</script>')
#         if end_index != -1:
#             json_data_str = json_data_str[:end_index]
#             print(json_data_str)
#             json_data = json.loads(json_data_str)
#             print(json.dumps(json_data, indent=2))
# except Exception as e:
#     print(f"Error: {e}")

# finally:
#     driver.quit()


# from selenium import webdriver
# import json
# import re

# url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)

# try:
#     driver.get(url)
#     print("Page loaded successfully")

#     # Execute JavaScript to get the content within the script tag
#     script_content = driver.execute_script('return window.state;')

#     if script_content:
#         json_data_str = json.dumps(script_content, indent=2)
#         print("Formatted JSON data:")
#         print(json_data_str)
#     else:
#         print("Content not found within script tag.")

# except Exception as e:
#     print(f"Error: {e}")

# finally:
#     driver.quit()

import requests
from bs4 import BeautifulSoup

url = 'https://www.bayut.com/for-sale/apartments/dubai/dubai-marina/'  # Replace with your actual URL

# Fetch the HTML content from the URL
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all script tags
    script_tags = soup.find_all('script')

    # Ensure there are at least four script tags
    if len(script_tags) >= 4:
        # Get the fourth-to-last script tag
        fourth_last_script = script_tags[-4]

        # Extract the content of the fourth-to-last script tag
        fourth_last_script_content = fourth_last_script.get_text(strip=True)

        # Save the content to a file
        with open('fourth_last_script_content.csv', 'w', encoding='utf-8') as file:
            file.write(fourth_last_script_content)

        print("Fourth-to-last script tag content saved to 'fourth_last_script_content.csv'")
    else:
        print("There are not enough script tags on the page.")

else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")






