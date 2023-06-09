from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import random
import time

def get_date(days : list):
    '''
        Funtion for calculating the job posted dates

        on the basis of the timedelta 

    '''
    dates=list()
    current_date = datetime.now()
    for day in days:
        if day.endswith('d+'):
            new_date = current_date - timedelta(days=30)
            dates.append(new_date.date())
        elif day.endswith('d'):
            num_days = int(day[:-1])
            new_date = current_date - timedelta(days=num_days)
            dates.append(new_date.date())
        elif day.endswith('h'):
            num_hours = int(day[:-1])
            new_date = current_date - timedelta(hours=num_hours)
            dates.append(new_date.date())
    return dates

def get_user_agent():
    '''
    The function for generating random user agents
    from the given list in the list
    
    '''
    user_agents = [
        "Mozilla/5.0 (Linux; Android 10; JNY-LX1; HMSCore 6.2.0.301) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4688.135 HuaweiBrowser/11.1.5.311 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4672.2 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; HRY-LX1T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4660.5 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; arm_64; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4684.0 YaBrowser/21.11.4.115.00 SA/3 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; Redmi Note 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4668.169 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.0; Ixion ML245) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.70 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36 GLS/95.10.6029.30",
        "Mozilla/5.0 (Linux; Android 10; Mi 9 SE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4650.4 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; arm_64; Android 11; SM-A315F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.3.105.00 SA/3 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.0; VT5000 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36"
        ]
    return random.choice(user_agents)

def close_popup(driver):
    """
    Close the pop-up if it appears.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    """
    try:
        close_button = driver.find_element(By.CSS_SELECTOR, "svg.modal_closeIcon-svg")
        close_button.click()
    except NoSuchElementException:
        pass  # Pop-up not found or already closed

# Set up the driver

def click_retry(driver):
    '''
        Refresh the posts button click function

    '''
    try:
        retry_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Retry your search')]")
        retry_button.click()
    except Exception:
        pass



def set_driver(search_job_title:str, search_location:str):
    options = Options()
    # options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--headless')  # Run in headless mode


    # options.add_argument('--no-sandbox')  # Bypass OS security model
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage') 
    # options.add_argument("--disable-javascript")
    options.add_argument(f"user-agent={get_user_agent()}")
    
    chromedriver_path = "chromedriver.exe"
    service = Service(chromedriver_path)
    
    driver = webdriver.Chrome(service=service, options=options)  # Replace with the path to your chromedriver executable
    driver.get("https://www.glassdoor.com/Job/index.htm")

    # Enter the job title and location in the search form
    key = driver.find_element(By.ID, "sc.keyword")
    key.clear()
    key.send_keys(search_job_title)
    

    location_input = driver.find_element(By.ID, "sc.location")
    location_input.click()  # Ensure the input field is focused
    location_input.send_keys(Keys.CONTROL + "a")  # Select all the text in the input field
    location_input.send_keys(Keys.BACKSPACE)  # Delete the selected text
    location_input.send_keys(search_location)
    
    search_button = driver.find_element(By.CSS_SELECTOR, ".universalSearch__UniversalSearchBarStyles__searchButton")
    search_button.click()
    
    see_all_jobs_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[data-test='jobs-location-see-all-link']")))
    see_all_jobs_link.click()
    
    time.sleep(5)
    
    platform = list()
    descrption_list=list()
    company_names=list()
    job_titles=list()
    locations=list()
    salaries = list()
    salaries1=list()
    salaries2=list()
    dates=list()
    links_list=list()
    is_remote=list()
    job_type=list()

    count = 0
    while True:
        descrption_list.clear()
        company_names.clear()
        job_titles.clear()
        locations.clear()
        salaries.clear()
        salaries1.clear()
        salaries2.clear()
        dates.clear()
        links_list.clear()
        job_type.clear()
        is_remote.clear()
        platform.clear()
        link_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-test='job-link']")
        for i in range(len(link_elements)):
            try:
                links_list.append(link_elements[i].get_attribute("href"))
                link_elements[i].click()
                time.sleep(5)
                click_retry(driver)
                close_popup(driver)
                time.sleep(5)
            except StaleElementReferenceException as exp:
                link_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-test='job-link']")  # Find the link elements again
                link_elements[i].click()
                time.sleep(5)
                click_retry(driver)
                close_popup(driver)
                time.sleep(5)
            except Exception as exp:
                print(exp)
                pass
            try:
                company_name = driver.find_element(By.CSS_SELECTOR, 'div[data-test="employerName"]')
                company_names.append(company_name.text.strip())
            except Exception:
                company_names.append(np.nan)
            
            try:
                job_title = driver.find_element(By.CSS_SELECTOR, 'div[data-test="jobTitle"]')
                job_titles.append(job_title.text.strip())
            except Exception:
                job_titles.append(np.nan)
            
            try:
                location = driver.find_element(By.CSS_SELECTOR, 'div[data-test="location"]')
                locations.append(location.text.strip())
            except Exception:
                locations.append(np.nan)

            try:
                salary = driver.find_element(By.CSS_SELECTOR, 'span[data-test="detailSalary"]')
                salaries1.append(salary.text.strip().replace("(Glassdoor est.)", "").replace("(Employer est.)", "").replace("Employer Provided Salary:", ""))
            except Exception:
                salaries1.append(np.nan)

            try:
                div_element = driver.find_element(By.XPATH, "//div[contains(@class, 'css-t3xrds') and text()='Show More']")
                time.sleep(5)
                div_element.click()# click the show more div
            except Exception:
                pass
            ###JOB DESCRIPTION
            time.sleep(5)
            
            try:
                description = driver.find_element(By.CLASS_NAME, 'jobDescriptionContent')
                descrption_list.append(description.text.strip())
                
                if 'remote' in description.text.strip().lower():
                    is_remote.append('TRUE')
                else:
                    is_remote.append('FALSE')
                
                if 'full-time' in description.text.strip().lower() or 'fulltime' in description.text.strip().lower() or 'full time' in description.text.strip().lower():
                    job_type.append('Full-Time')
                elif 'contract' in description.text.strip().lower():
                    job_type.append('Contract')
                elif 'part-time' in description.text.strip().lower() or 'parttime' in description.text.strip().lower() or 'part time' in description.text.strip().lower():
                    job_type.append('Part-time')
                else:
                    job_type.append(np.nan)
            
            except Exception:
                descrption_list.append(np.nan)

        salary_elements = driver.find_elements(By.CSS_SELECTOR, "div.salary-estimate")
        salaries2 = [element.text.replace("(Glassdoor est.)", "").replace("(Employer est.)", "") for element in salary_elements]
        print(salaries2)
        
        divs = driver.find_elements(By.CSS_SELECTOR, 'div.d-flex.align-items-end.ml-xsm.listing-age[data-test="job-age"]')
        dates = [div.text for div in divs]
        dates = get_date(dates)

        nan_count = pd.isna(salaries1).sum()
        threshold = 5  # Set your desired threshold here
    
        if nan_count > threshold:
            salaries = salaries2  # Use salaries2 if nan_count is greater than the threshold
        else:
            salaries = salaries1

        max_length = max(
        len(company_names),
        len(job_titles),
        len(locations),
        len(salaries),
        len(dates),
        len(descrption_list),
        len(links_list),
        len(job_type),
        len(is_remote)
    )
    
        company_names+= [np.nan] * (max_length - len(company_names))
        job_titles += [np.nan] * (max_length - len(job_titles))
        job_type += [np.nan] * (max_length - len(job_type))
        salaries += [np.nan] * (max_length - len(salaries))
        is_remote += [np.nan] * (max_length - len(is_remote))
        locations+= [np.nan] * (max_length - len(locations))
        platform += ['Glassdoor'] * (max_length - len(platform))
        links_list += [np.nan] * (max_length - len(links_list))
        dates += [np.nan] * (max_length - len(dates))
        descrption_list += [np.nan] * (max_length - len(descrption_list))
        # next_button.click()
        temp_df = pd.DataFrame({
            "company_name": company_names,
            "titles": job_titles,
            "locations": locations,
            "salary": salaries,
            "date": dates,
            "description": descrption_list,
            "link": links_list,
            "platform": "Glassdoor",
            "job_type": job_type,
            "is_remote": is_remote,
            "country": search_location
        })

        if count==0:
            temp_df.to_csv("File2002.csv", index=False)
            count=count+1
        else:
            temp_df.to_csv("File2002.csv", mode='a', index=False, header=False)

        time.sleep(5)
        close_popup(driver)
        next_button_visibility = driver.find_element(By.CSS_SELECTOR, "button.nextButton")
        is_disabled = next_button_visibility.get_attribute("disabled")

        if is_disabled:
            break  # Exit the loop if it's the last page

        next_button = driver.find_element(By.CSS_SELECTOR, "button.nextButton")  # Assign next_button inside the loop
        next_button.click()

    return "Completed Scraping"

if __name__=="__main__":
    search_job_title = "data engineer"
    search_location = "United States"
    print(set_driver(search_job_title=search_job_title, search_location=search_location))


