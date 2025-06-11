import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website
url = "https://ceoaperolls.ap.gov.in/AP_MLC_2024/ERO/Status_Update_2024/knowYourApplicationStatus.aspx"

# Function to scrape house number data
def scrape_house_number(application_id):
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

        # Prepare a list to hold the house numbers
        house_numbers = []

        # Extract all rows from the table
        rows = table.find_all('tr')

        # Loop through each row and extract data from <td> elements
        for row in rows:
            cells = row.find_all('td')
            if cells and len(cells) > 0:  # Check if there are any <td> elements
                # Assuming the "House Number" is in a specific column, adjust the index as needed
                house_number = cells[3].text.strip()  # Adjust index based on the actual column position
                house_numbers.append(house_number)  # Append the extracted house number to the list

        # Create a DataFrame from the extracted house numbers
        df = pd.DataFrame(house_numbers, columns=['House Number'])  # Create a DataFrame with one column

        # Save the DataFrame to a CSV file
        df.to_csv('data/house_numbers.csv', index=False)

        print("House numbers extracted and saved to 'data/house_numbers.csv'.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

# Example usage
application_id = "YOUR_APPLICATION_ID"  # Replace with the actual application ID
scrape_house_number(application_id)
