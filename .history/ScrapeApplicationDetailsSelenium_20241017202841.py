from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set the path to the ChromeDriver executable
chrome_driver_path = r"C:\\Users\\srira\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"   # Replace with your actual ChromeDriver path

# Function to scrape specified data
def scrape_data(application_id, count):
    # Set up the Selenium WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Navigate to the URL
    url = "https://ceoaperolls.ap.gov.in/AP_MLC_2024/ERO/Status_Update_2024/knowYourApplicationStatus.aspx"
    driver.get(url)

    # Wait for the page to load and find the input field
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'TextBox2')))
    
    # Enter the application ID
    input_field = driver.find_element(By.ID, 'TextBox2')
    input_field.send_keys(application_id)

    # Click the search button
    search_button = driver.find_element(By.ID, 'btnGraduates')
    search_button.click()

    # Wait for the results to load
    time.sleep(10)  # Adjust the sleep time as necessary

    # Find the table containing the data
    table = driver.find_element(By.TAG_NAME, 'table')  # Adjust this if there are multiple tables

    # Prepare a list to hold the extracted data
    data_list = []

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

    # Limit the number of entries to the specified count
    data_list = data_list[:count]

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data_list, columns=['App ID', 'PS_NO', 'SLNO', 'Name', 'Relation Name', 'House Number', 'Age'])

    # Save the DataFrame to a CSV file
    df.to_csv('application_details.csv', index=False)

    print(f"Data extracted and saved to 'application_details.csv'. Total entries saved: {len(data_list)}.")

    # Close the browser
    driver.quit()

# Example usage
application_id = "YOUR_APPLICATION_ID"  # Replace with the actual application ID
count = 5  # Specify how many entries you want to save
scrape_data(application_id, count)

