# import csv

# # Read the content from the saved CSV file
# with open('fourth_last_script_content.csv', 'r', encoding='utf-8') as file:
#     csv_reader = csv.DictReader(file)

#     # Print 'ownerID' for each apartment
#     for index, record in enumerate(csv_reader, start=1):
#         owner_id = record.get('ownerID')
#         print(f"Apartment {index} - OwnerID: {owner_id}")


import csv
import json

# Read the content from the saved CSV file
with open('fourth_last_script_content.csv', 'r', encoding='utf-8') as file:
    # Assuming each row in the CSV is a string representation of a JSON object
    csv_reader = csv.reader(file)

    # Skip the header if needed
    header = next(csv_reader, None)

    # Print 'ownerID' for each valid row
    for index, row in enumerate(csv_reader, start=1):
        # Check if the row is not empty
        if row:
            try:
                # Parse the row as JSON
                json_data = json.loads(row[0])  # Assuming the JSON data is in the first column

                # Check if 'ownerID' is present in the JSON data
                owner_id = json_data.get('ownerID')
                if owner_id is not None:
                    print(f"Row {index} - OwnerID: {owner_id}")
                else:
                    print(f"Skipping Row {index} - Missing 'ownerID'")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON content for Row {index}: {e}")
        else:
            print(f"Skipping empty row {index}")

