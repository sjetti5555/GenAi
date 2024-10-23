import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website
url = "https://ceoaperolls.ap.gov.in/AP_MLC_2024/ERO/Status_Update_2024/knowYourApplicationStatus.aspx"

# Function to scrape specified data
def scrape_data(application_id, count):
    # Create a session
    session = requests.Session()

    # Prepare the payload with the application ID
    payload = {
        'TextBox2': application_id,  # The name of the input field for Application ID
        'btnGraduates': 'Search'  # The name of the submit button
    }

    # Send a POST request to submit the application ID
    response = session.post(url, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the data
        table = soup.find('table')  # Adjust this if there are multiple tables

        # Check if the table was found
        if table is None:
            print("No table found in the response. Please check the HTML structure.")
            return

        # Prepare a list to hold the extracted data
        data_list = []

        # Extract all rows from the table
        rows = table.find_all('tr')

        # Loop through each row and extract data from <td> elements
        for row in rows[1:]:  # Skip the header row
            cells = row.find_all('td')
            if cells and len(cells) >= 4:  # Ensure there are enough cells
                app_id = cells[0].text.strip()  # App ID
                name = cells[1].text.strip()  # Name
                relation_name = cells[2].text.strip()  # Relation Name
                house_number = cells[3].text.strip()  # House Number
                data_list.append([app_id, name, relation_name, house_number])  # Append the extracted data

        # Limit the number of entries to the specified count
        data_list = data_list[:count]

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data_list, columns=['App ID', 'Name', 'Relation Name', 'House Number'])

        # Save the DataFrame to a CSV file
        df.to_csv('application_status.csv', index=False)

        print(f"Data extracted and saved to 'application_status.csv'. Total entries saved: {len(data_list)}.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

# Example usage
application_id = "YOUR_APPLICATION_ID"  # Replace with the actual application ID
count = 5  # Specify how many entries you want to save
scrape_data(application_id, count)
