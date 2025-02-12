from fastapi import FastAPI
# from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging
import json
import subprocess
from datetime import datetime
import os

app = FastAPI()
# scheduler = BackgroundScheduler()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global driver initialization
driver = None

def create_driver():
    """Creates and configures the Chrome driver."""
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--headless")
        try:
            driver = webdriver.Chrome(options=options)
            logging.info("Chrome driver initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing Chrome driver: {e}")
            exit() # Exit if the driver fails to start

def shutdown_driver():
    global driver
    if driver:
        driver.quit()
        logging.info("Chrome driver quit successfully.")

def scrape_weworkremotely_jobs(title):
    url = f"https://weworkremotely.com/remote-jobs/search?term={title}&sort=past_week"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        try:
            jobs_list = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "category-")]/article/ul')))
            job_items = jobs_list.find_elements(By.TAG_NAME, 'li')
            jobs = []

            for job in job_items:
                try:
                    if "view-all" in job.get_attribute('class') or "feature feature--ad" in job.get_attribute('class'):
                        continue
                    driver.execute_script("arguments[0].scrollIntoView();", job)
                    job_links = job.find_elements(By.TAG_NAME, 'a')
                    href = job_links[-1].get_attribute("href")
                    title = job.find_element(By.CLASS_NAME, 'new-listing__header__title').text
                    company = job.find_element(By.CLASS_NAME, 'new-listing__company-name').text if job.find_element(By.CLASS_NAME, 'new-listing__company-name') else "Unknown"
                    job_type = "Remote"
                    location = job.find_element(By.CLASS_NAME, 'new-listing__company-headquarters').text if job.find_element(By.CLASS_NAME, 'new-listing__company-headquarters') else "Not specified"
                    try:
                        posted = job.find_element(By.CLASS_NAME, 'new-listing__header__icons__date').text
                    except:
                        posted = "Not provided"
                    # driver.execute_script("arguments[0].scrollIntoView();", job)
                    img_src = "No Image"  # Default value
                    try:
                        img = job.find_element(By.CLASS_NAME, 'tooltip--flag-logo__flag-logo').get_attribute('style')
                        start = img.find('url("') + 5  # Find start of URL
                        img_src = img[start:len(img) - 3]  # Extract the image URL
                    except Exception:
                        pass  # If no image found, it will remain "No Image"
                    job_as_JSON = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "posted": posted,
                        "href": href,
                        "type": job_type,
                        "img": img_src,
                        "site":"WeWorkRemotely"
                    }
                    jobs.append(job_as_JSON)

                except Exception as e:
                    logging.error(f"Error extracting we work remotely job details: {e}")

            return jobs

        except Exception as e:
            logging.error(f"Job listings not found or error: {e}")
            return []
    except Exception as e:
        logging.error(f"Exception in scrape_weworkremotely_jobs: {e}")
        return []

def scrape_remotive_jobs(title):
    url = f"https://remotive.io/remote-jobs?query={title}"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        try:
            # Wait for job listings container
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="hits"]/ul')))

            # Try selecting "Sort by newest"
            try:
                sort_by_dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sort-by select')))
                select = Select(sort_by_dropdown)
                select.select_by_index(1)  # Sort by Newest
            except Exception:
                logging.info("Sort dropdown not found, skipping sorting step.")

            # Fetch job items AFTER sorting
            job_items = driver.find_elements(By.XPATH, '//*[@id="hits"]/ul/div')

            jobs = []
            for job in job_items:
                try:
                    # Extract job link
                    job_link = job.find_element(By.CSS_SELECTOR, 'a.remotive-url-visit').get_attribute('href')

                    # Extract job title & company name
                    title_elements = job.find_elements(By.CSS_SELECTOR, 'a.remotive-url-visit span')
                    job_title = title_elements[0].text.strip() if title_elements else "Unknown"
                    company_name = title_elements[2].text.strip() if len(title_elements) > 1 else "Not specified"
                    # Extract location (skip salary if detected)
                    location_elements = job.find_elements(By.CSS_SELECTOR, '.tag-small')
                    if len(location_elements) > 1:
                        location = location_elements[1].text.strip()
                        if any(currency in location for currency in ["$", "€", "£"]):
                            location = location_elements[2].text.strip() if len(location_elements) > 2 else "Remote"
                    else:
                        location = "Remote"

                    # Extract posting date
                    posted_element = job.find_elements(By.XPATH, './/span[contains(@class, "job-tile-apply-hide")]/span')
                    posted = posted_element[0].text.strip() if posted_element else "Not provided"

                    # Extract company logo
                    img_element = job.find_elements(By.CSS_SELECTOR, 'img')
                    img_src = img_element[0].get_attribute('data-lazyload') if img_element else "No Image"

                    # Store job details
                    job_as_JSON = {
                        "title": job_title,
                        "company": company_name,
                        "location": location,
                        "posted": posted,
                        "href": job_link,
                        "type": "Remote",
                        "img": img_src,
                        "site": "Remotive"
                    }
                    jobs.append(job_as_JSON)

                except Exception as e:
                    logging.error(f"Error extracting job details: {e}")

            return jobs

        except Exception as e:
            logging.error(f"Job listings not found or error: {e}")
            return []
    except Exception as e:
        logging.error(f"Exception in scrape_remotive_jobs: {e}")
        return []

def remoteokJobs(title):
    url = f"https://remoteok.com/remote-{title}-jobs?order_by=date"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="jobsboard"]/tbody')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="jobsboard"]/tbody/tr')))
            job_items = driver.find_elements(By.XPATH, '//*[@id="jobsboard"]/tbody/tr')
            job_items = [job for job in job_items if "job" in job.get_attribute('class')]
            jobs = []

            for job in job_items:
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", job)
                    link_element = job.find_element(By.XPATH, './td[1]/a')
                    href = link_element.get_attribute('href') if link_element else "No link"
                    title = job.find_element(By.TAG_NAME, 'h2').text if job.find_elements(By.TAG_NAME, 'h2') else "Unknown"
                    company = job.find_element(By.TAG_NAME, 'h3').text if job.find_elements(By.TAG_NAME, 'h3') else "Unknown"
                    location_elements = job.find_elements(By.CLASS_NAME, 'location')
                    location = location_elements[0].text if location_elements else "Unknown"
                    if "💰" in location:
                        location = "Specified in Job description"
                    posted_elements = job.find_elements(By.CLASS_NAME, 'time')
                    posted = posted_elements[0].text if posted_elements else "Not provided"
                    # driver.execute_script("arguments[0].scrollIntoView();", job)
                    img_elements = job.find_elements(By.TAG_NAME, 'img')
                    img = img_elements[0].get_attribute('src') if img_elements else "No Image"
                    job_as_JSON = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "posted": posted,
                        "href": href,
                        "img": img,
                        "type": "Remote",
                        "site": "Remoteok"
                    }
                    jobs.append(job_as_JSON)
                except Exception as e:
                    logging.error(f"Error extracting job details: {e}")
            return jobs
        except Exception as e:
            return {"error": "Job listings not found or error:", "message": str(e)}
    except Exception as e:
        logging.error(f"Exception in remoteokJobs: {e}")
        return []
def linkedInJobs(title):
    url = f"https://www.linkedin.com/jobs/search/?keywords={title}&location=remote&f_TPR=r86400"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        try:
            dismiss_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/button')))
            dismiss_button.click()
            logging.info("Dismissed LinkedIn login popup.")
        except Exception:
            logging.info("No login popup found or already closed.")

        job_list = []
        try:
            jobs_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search__results-list')))
            job_items = jobs_list.find_elements(By.TAG_NAME, 'li')
            for job in job_items:
                try:
                    job_data = {
                        "title": job.find_element(By.CLASS_NAME, 'base-search-card__title').text.strip(),
                        "company": job.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text.strip(),
                        "location": job.find_element(By.CLASS_NAME, 'job-search-card__location').text.strip(),
                        "posted": job.find_element(By.TAG_NAME, 'time').text.strip(),
                        "href": job.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                        "type": "Remote",
                         "site":"LinkedIn"
                    }

                    driver.execute_script("arguments[0].scrollIntoView();", job)

                    img_element = job.find_elements(By.TAG_NAME, 'img')
                    img = img_element[0].get_attribute('src') if img_element else "No Image"
                    job_data["img"] = img
                    job_list.append(job_data)

                except Exception as e:
                    logging.error(f"Error extracting job details: {e}")
            return job_list
        except Exception as e:
            logging.error(f"LinkedIn scraping error: {e}")
            return []
    except Exception as e:
        logging.error(f"Exception in linkedInJobs: {e}")
        return []



def scrape_jobs(jobs):
    """Main job scraping function."""
    create_driver()
    try:
        for title in jobs:
            all_jobs = []
            all_jobs.extend(linkedInJobs(title))
            all_jobs.extend(scrape_weworkremotely_jobs(title))
            all_jobs.extend(scrape_remotive_jobs(title))
            all_jobs.extend(remoteokJobs(title))
            save_to_json(title, all_jobs)
        push_to_git()  # Push changes to Git after scraping
    finally:
        shutdown_driver()

def push_to_git():
    repo_path = "C:/Users/User/Desktop/WEB/AI-Web-Integration/Jobs-Scraper"
    os.chdir(repo_path)

    # Timestamp for commit message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Git commands
    commands = [
        "git add .",
        f'git commit -m "Auto-update: {timestamp}"',
        "git push origin dev"]

    # Run Git commands
    try:
        for cmd in commands:
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(process.stdout, process.stderr)
    except subprocess.CalledProcessError as e:
        logging.error(f"Git push failed: {e}")

def save_to_json(title, data):
    filename = f"{title.lower().replace(' ', '_')}_jobs.json"
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Saved jobs for {title} to {filename}")
    except Exception as e:
        logging.error(f"Error saving JSON: {e}")

# API Endpoint to Manually Trigger Scraping
@app.get("/scrape-now")
def scrape_now():
    jobs = ["Software", "Developer", "Backend", "Front End", "Machine Learning", "Internship", "Data Science"]  # You can change this to whatever job titles you want to scrape
    scrape_jobs(jobs)
    return {"message": "Job scraping started manually"}

# Schedule the job to run every hour
# scheduler.add_job(scrape_jobs, "interval", hours=1, args=[["Software", "Developer", "Backend", "Front End", "Machine Learning", "Internship", "Data Science"]])  # Pass a list of jobs to scrape
# scheduler.start()

@app.get("/")
def home():
    return {"message": "Welcome to the Job Scraper API"}