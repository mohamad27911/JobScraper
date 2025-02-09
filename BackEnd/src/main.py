from fastapi import FastAPI
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uvicorn
from fastapi import BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from selenium.webdriver.support.ui import Select
import tempfile
import logging
from undetected_chromedriver import Chrome, ChromeOptions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
origins = [
    "http://localhost:5173",  # Allow the frontend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize driver only once
driver = None

def create_driver():
    """Creates and configures the Chrome driver."""
    global driver  # Use the global driver variable
    if driver is None:
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-dev-shm-usage")

        try:
            driver = Chrome(options=options) # using undetected chromedriver
            logging.info("Chrome driver initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing Chrome driver: {e}")
            raise  # Re-raise the exception to prevent the app from starting

# Shutdown event to quit the driver when FastAPI app shuts down
@app.on_event("startup")
async def startup_event():
    create_driver()

# Shutdown event to quit the driver when FastAPI app shuts down
@app.on_event("shutdown")
def shutdown_event():
    global driver
    if driver:
        driver.quit()
        logging.info("Chrome driver quit successfully.")

def scrape_weworkremotely_jobs(title):
    url = f"https://weworkremotely.com/remote-jobs/search?search_uuid=&term={title}&button=&past_24_hours"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        try:
            jobs_list = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="category-17"]/article/ul')))
            job_items = jobs_list.find_elements(By.TAG_NAME, 'li')
            jobs = []

            for job in job_items:
                try:
                    if "view-all" in job.get_attribute('class'):
                        continue
                    driver.execute_script("arguments[0].scrollIntoView();", job)
                    job_links = job.find_elements(By.TAG_NAME, 'a')
                    href = job_links[-1].get_attribute("href")
                    title = job.find_element(By.CLASS_NAME, 'title').text
                    company_info = job.find_elements(By.CLASS_NAME, 'company')
                    company = company_info[0].text if len(company_info) > 0 else "Unknown"
                    job_type = company_info[1].text if len(company_info) > 1 else "Not specified"
                    location = job.find_element(By.CLASS_NAME, 'region.company').text if job.find_elements(By.CLASS_NAME, 'region.company') else "Not specified"
                    posted = job.find_element(By.CLASS_NAME, 'listing-date__date').text if job.find_elements(By.CLASS_NAME, 'listing-date__date') else "Not provided"
                    # driver.execute_script("arguments[0].scrollIntoView();", job)
                    img_src = "No Image"  # Default value
                    try:
                        img = job.find_element(By.CLASS_NAME, 'flag-logo').get_attribute('style')
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
                        "img": img_src
                    }
                    jobs.append(job_as_JSON)

                except Exception as e:
                    logging.error(f"Error extracting job details: {e}")

            return jobs

        except Exception as e:
            logging.error(f"Job listings not found or error: {e}")
            return []
    except Exception as e:
        logging.error(f"Exception in scrape_weworkremotely_jobs: {e}")
        return []


@app.get("/jobs/weworkremotely/{title}")
async def get_weworkremotely_jobs(title: str):
    jobs = scrape_weworkremotely_jobs(title)
    return JSONResponse(content={"jobs": jobs})


def scrape_remotive_jobs(title):
    url = f"https://remotive.io/remote-jobs?query={title}"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        try:
            # Wait for job listings container
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#hits > ul > div[x-data]")))

            # Try selecting "Sort by newest"
            try:
                sort_by_dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sort-by select')))
                select = Select(sort_by_dropdown)
                select.select_by_index(1)  # Sort by Newest
                time.sleep(3)  # Wait for sorting to apply
            except Exception:
                logging.info("Sort dropdown not found, skipping sorting step.")

            # Fetch job items **AFTER** sorting
            job_items = driver.find_elements(By.CSS_SELECTOR, '#hits > ul > div[x-data]')

            jobs = []
            for job in job_items:
                try:
                    # Extract job link
                    job_link = job.find_element(By.CSS_SELECTOR, 'a.remotive-url-visit').get_attribute('href')

                    # Extract title and company name
                    title_element = job.find_elements(By.CSS_SELECTOR, '.remotive-bold')
                    job_title = title_element[0].text if len(title_element) > 0 else "Unknown"
                    company_name = title_element[-1].text if len(title_element) > 1 else "Not specified"

                    # Extract job location (fallback to "Remote")
                    job_tags = job.find_elements(By.CSS_SELECTOR, '.tag-small')
                    location = job_tags[0].text if job_tags else "Remote"

                    # Extract posting date
                    posted = "Not provided"
                    posted_elements = job.find_elements(By.XPATH, './/div[contains(@class, "tw-hidden sm:tw-flex")]/span/span')
                    if posted_elements:
                        posted = posted_elements[0].text.strip()

                    # Extract company logo
                    img_element = job.find_elements(By.CSS_SELECTOR, 'img')
                    img_src = img_element[0].get_attribute('src') if img_element else "No Image"

                    # Store job details as dictionary
                    job_as_JSON = {
                        "title": job_title,
                        "company": company_name,
                        "location": location,
                        "posted": posted,
                        "href": job_link,
                        "type": "Remote",
                        "img": img_src
                    }
                    jobs.append(job_as_JSON)

                except Exception as e:
                    logging.error(f"Error extracting job details: {e}")

            # print(jobs)
            return jobs

        except Exception as e:
            logging.error(f"Job listings not found or error: {e}")
            return []
    except Exception as e:
        logging.error(f"Exception in scrape_remotive_jobs: {e}")
        return []


@app.get("/jobs/remotive/{title}")
async def get_remotive_jobs(title: str):
    jobs = scrape_remotive_jobs(title)
    return JSONResponse(content={"jobs": jobs})


# Scrape filters
def scrapeFilter():
    url = f"https://remoteok.com/"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        search_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="jobsboard"]/thead/tr/th/div[2]/input')))
        search_input.click()
        filters_modal = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/div[4]')))

        filter_items = filters_modal.find_elements(By.XPATH, './/div')
        logging.info(f"Number of filters found: {len(filter_items)}")
        filters = []

        for filter in filter_items:
            filters.append(filter.text)

        return filters
    except Exception as e:
        logging.error(f"Error in scrapeFilter: {e}")
        return []

@app.get("/filters")
async def get_filters():
    filters = scrapeFilter()
    return JSONResponse(content={"filters": filters})


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


@app.get("/jobs/remoteok/{title}")
async def scrape_remoteok(title: str):
    jobs = remoteokJobs(title)
    return JSONResponse(content=jobs)


# Function for LinkedIn job scraping
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
                        "type": "Remote"
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


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)