import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website
url = "https://ceoaperolls.ap.gov.in/AP_MLC_2024/ERO/Status_Update_2024/knowYourApplicationStatus.aspx"

# Function to scrape application status
def scrape_application_status(application_id):
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

        # Extract the headers
        headers = [header.text.strip() for header in table.find_all('th')]
        
        # Extract all rows from the table
        rows = table.find_all('tr')

        # Loop through each row and extract data from <td> elements
        for row in rows:
            cells = row.find_all('td')
            if cells:  # Check if there are any <td> elements
                data = [cell.text.strip() for cell in cells]  # Extract text and strip whitespace
                data_list.append(data)  # Append the extracted data to the list

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data_list, columns=headers)  # Use headers for column names

        # Save the DataFrame to a CSV file
        df.to_csv('application_status.csv', index=False)

        print("Data extracted and saved to 'application_status.csv'.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

# Example usage
application_id = "YOUR_APPLICATION_ID"  # Replace with the actual application ID
scrape_application_status(application_id)
