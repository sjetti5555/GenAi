from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Set up the Selenium WebDriver (make sure to have the appropriate driver installed)
driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.

# Function to scrape job details from the current page
def scrape_jobs():
    job_titles = driver.find_elements(By.CSS_SELECTOR, 'a.card-title-link')
   
    job_position_types = driver.find_elements(By.CSS_SELECTOR, 'div.card-position-type > span')
    job_locations = driver.find_elements(By.CSS_SELECTOR, 'div.card-location > span')
    job_companies = driver.find_elements(By.CSS_SELECTOR, 'div.card-company > span')
    job_posted_times = driver.find_elements(By.CSS_SELECTOR, 'div.card-posted-time > span')
 
    return zip(job_titles, job_link, job_position_types, job_locations, job_companies, job_posted_times, job_pay)

# Navigate to the job listings page
url = 'https://www.dice.com/jobs?q=salesforce%20developer&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&language=en'
driver.get(url)

# Open a CSV file to save the data
with open('data/scraped_dice_jobs.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Job Title', 'Job Link', 'Job Position Type', 'Location', 'Company', 'Posted Time', 'Pay'])

    # Count the number of jobs gathered
    job_count = 0

    while True:
        # Wait for job cards to be present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.card')))

        # Scrape job details
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'div.card')
        for card in job_cards:
            try:
                job_title = card.find_element(By.CSS_SELECTOR, 'a.card-title-link').text.strip()  # Corrected selector for job title
                job_link = card.find_element(By.CSS_SELECTOR, 'a.card-title-link').get_attribute('href')
                job_position_type = card.find_element(By.CSS_SELECTOR, 'div.card-position-type > span').text.strip()
                job_location = card.find_element(By.CSS_SELECTOR, 'div.card-location > span').text.strip()
                job_company = card.find_element(By.CSS_SELECTOR, 'div.card-company > span').text.strip()
                job_posted_time = card.find_element(By.CSS_SELECTOR, 'div.card-posted-time > span').text.strip()
                job_pay = card.find_element(By.CSS_SELECTOR, 'div.card-pay > span').text.strip() if card.find_elements(By.CSS_SELECTOR, 'div.card-pay > span') else 'N/A'
                
                # Write the row to the CSV file
                writer.writerow([job_title, job_link, job_position_type, job_location, job_company, job_posted_time, job_pay])
                
                # Increment the job count
                job_count += 1
            except Exception as e:
                print(f"Error extracting job details: {e}")

        # Check for the "Next" button to navigate to the next page
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')  # Adjust the selector based on the actual HTML
            if "disabled" in next_button.get_attribute("class"):
                break  # Exit the loop if the "Next" button is disabled
            next_button.click()  # Click the "Next" button
            WebDriverWait(driver, 10).until(EC.staleness_of(job_cards[0]))  # Wait for the page to load
        except Exception as e:
            print("No more pages or an error occurred:", e)
            break  # Exit the loop if there are no more pages or an error occurs

    print(f"Data has been scraped and saved to 'data/scraped_dice_jobs.csv'.")
    print(f"Total jobs gathered: {job_count}")

# Close the browser
driver.quit()
