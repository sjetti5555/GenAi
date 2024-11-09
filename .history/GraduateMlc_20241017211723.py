from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set the path to the ChromeDriver executable
chrome_driver_path = r"C:\\Users\\srira\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"  # Ensure this path is correct

# Function to scrape specified data
def scrape_data(start_id, end_id):
    # Set up the Selenium WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Navigate to the URL
    url = "https://ceoaperolls.ap.gov.in/AP_MLC_2024/ERO/Status_Update_2024/knowYourApplicationStatus.aspx"
    driver.get(url)

    # Wait for the "Graduate" tab to be clickable and click it
    graduate_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Graduate"))
    )
    graduate_tab.click()

    # Select the "Application ID" search type
    application_id_radio = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'GraduateAppID'))  # Adjust this ID based on the actual HTML
    )
    application_id_radio.click()

    # Prepare a list to hold the extracted data
    data_list = []

    try:
        # Loop through the specified range of application IDs
        for app_id in range(int(start_id.split('-')[1]), int(end_id.split('-')[1]) + 1):
            formatted_app_id = f"F18-{app_id:07d}"  # Format the application ID
            print(f"Processing Application ID: {formatted_app_id}")

            # Wait for the input field to be present and visible
            input_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'TextBox2'))
            )
            
            # Enter the application ID
            input_field.clear()  # Clear the input field before entering a new ID
            input_field.send_keys(formatted_app_id)

            # Click the search button
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'btnGraduates'))
            )
            search_button.click()

            # Wait for the results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'table'))  # Wait for the table to be present
            )

            # Find the table containing the data
            table = driver.find_element(By.TAG_NAME, 'table')  # Adjust this if there are multiple tables

            # Extract all rows from the table
            rows = table.find_elements(By.TAG_NAME, 'tr')

            # Loop through each row and extract data from <td> elements
            for row in rows[1:]:  # Skip the header row
                cells = row.find_elements(By.TAG_NAME, 'td')
                if cells and len(cells) >= 7:  # Ensure there are enough cells
                    app_id = cells[0].text.strip()  # App ID
                    ps_no = cells[1].text.strip()  # PS_NO
                    slno = cells[2].text.strip()  # SLNO
                    name = cells[3].text.strip()  # Name
                    relation_name = cells[4].text.strip()  # Relation Name
                    house_number = cells[5].text.strip()  # House Number
                    age = cells[6].text.strip()  # Age
                    data_list.append([app_id, ps_no, slno, name, relation_name, house_number, age])  # Append the extracted data

            # Optional: Add a delay to avoid overwhelming the server
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProcess interrupted. Saving collected data...")

    finally:
        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data_list, columns=['App ID', 'PS_NO', 'SLNO', 'Name', 'Relation Name', 'House Number', 'Age'])

        # Save the DataFrame to a CSV file
        df.to_csv('GraduateMlc.csv', index=False)

        print(f"Data extracted and saved to 'GraduateMlc.csv'. Total entries saved: {len(data_list)}.")

        # Close the browser
        driver.quit()

# Example usage
user_input = input("Enter the range of application IDs to process (e.g., 1-10): ")  # Get user input for the range
start_range, end_range = user_input.split('-')  # Split the input into start and end
start_application_id = f"F18-{int(start_range):07d}"  # Format the starting application ID
end_application_id = f"F18-{int(end_range):07d}"  # Format the ending application ID
scrape_data(start_application_id, end_application_id)
