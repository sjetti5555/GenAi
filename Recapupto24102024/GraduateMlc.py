from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import threading
from queue import Queue
from webdriver_manager.chrome import ChromeDriverManager

# Set the path to the ChromeDriver executable
chrome_driver_path = r"C:\\Users\\srira\\Downloads\\chromedriver-win64\\chromedriver.exe"   # Ensure this path is correct

# Function to scrape specified data for a range of application IDs
def scrape_data(queue, data_list):
    # Set up the Selenium WebDriver in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    while not queue.empty():
        formatted_app_id = queue.get()
        print(f"Processing Application ID: {formatted_app_id}")

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

        try:
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
            time.sleep(0.5)  # Reduced sleep time

        except Exception as e:
            print(f"Error processing {formatted_app_id}: {e}")

        finally:
            queue.task_done()

    driver.quit()

# Function to manage threading
def run_scraper_in_threads(start_id, end_id, num_threads=10):
    data_list = []
    queue = Queue()
    
    # Populate the queue with application IDs
    for app_id in range(int(start_id.split('-')[1]), int(end_id.split('-')[1]) + 1):
        formatted_app_id = f"F18-{app_id:07d}"
        queue.put(formatted_app_id)

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=scrape_data, args=(queue, data_list))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return data_list

# Example usage
try:
    user_input = input("Enter the range of application IDs to process (e.g., 1-50000): ")  # Get user input for the range
    start_range, end_range = user_input.split('-')  # Split the input into start and end
    start_application_id = f"F18-{int(start_range):07d}"  # Format the starting application ID
    end_application_id = f"F18-{int(end_range):07d}"  # Format the ending application ID

    # Run the scraper with threading
    data = run_scraper_in_threads(start_application_id, end_application_id)

    # Save the collected data to a CSV file
    df = pd.DataFrame(data, columns=['App ID', 'PS_NO', 'SLNO', 'Name', 'Relation Name', 'House Number', 'Age'])
    df.to_csv('GraduateMlc.csv', index=False)
    print(f"Data extracted and saved to 'GraduateMlc.csv'. Total entries saved: {len(data)}.")

except KeyboardInterrupt:
    print("\nProcess interrupted. Saving collected data...")
    # Save the collected data to a CSV file
    df = pd.DataFrame(data, columns=['App ID', 'PS_NO', 'SLNO', 'Name', 'Relation Name', 'House Number', 'Age'])
    df.to_csv('GraduateMlc_partial.csv', index=False)
    print(f"Partial data saved to 'GraduateMlc_partial.csv'. Total entries saved: {len(data)}.")

except Exception as e:
    print(f"An error occurred: {e}")
