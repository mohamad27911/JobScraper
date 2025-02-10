from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from selenium.webdriver.support.ui import Select
import concurrent.futures
import asyncio

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
            raise

# Shutdown event to quit the driver when FastAPI app shuts down
@app.on_event("startup")
async def startup_event():
    create_driver()

@app.on_event("shutdown")
def shutdown_event():
    global driver
    if driver:
        driver.quit()
        logging.info("Chrome driver quit successfully.")

# Helper function for job scraping on each site
async def scrape_site(url, site_type):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        if site_type == "weworkremotely":
            return await scrape_weworkremotely_jobs(wait)
        elif site_type == "remotive":
            return await scrape_remotive_jobs(wait)
        elif site_type == "remoteok":
            return await scrape_remoteok_jobs(wait)
        elif site_type == "linkedin":
            return await scrape_linkedin_jobs(wait)
        else:
            return []

    except Exception as e:
        logging.error(f"Error scraping {site_type}: {e}")
        return []

async def scrape_weworkremotely_jobs(wait):
    url = f"https://weworkremotely.com/remote-jobs"
    try:
        jobs_list = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="category-17"]/article/ul')))
        job_items = jobs_list.find_elements(By.TAG_NAME, 'li')
        jobs = []
        for job in job_items:
            if "view-all" in job.get_attribute('class'):
                continue
            job_data = {
                "title": job.find_element(By.CLASS_NAME, 'title').text,
                "company": job.find_element(By.CLASS_NAME, 'company').text,
                "location": job.find_element(By.CLASS_NAME, 'region.company').text,
                "href": job.find_element(By.TAG_NAME, 'a').get_attribute('href')
            }
            jobs.append(job_data)
        return jobs
    except Exception as e:
        logging.error(f"Error extracting job details: {e}")
        return []

async def scrape_remotive_jobs(wait):
    url = f"https://remotive.io/remote-jobs"
    try:
        job_items = driver.find_elements(By.CSS_SELECTOR, '#hits > ul > div[x-data]')
        jobs = []
        for job in job_items:
            job_data = {
                "title": job.find_element(By.CSS_SELECTOR, '.remotive-bold').text,
                "company": job.find_element(By.CSS_SELECTOR, '.remotive-bold').text,
                "location": job.find_element(By.CSS_SELECTOR, '.tag-small').text,
                "href": job.find_element(By.CSS_SELECTOR, 'a.remotive-url-visit').get_attribute('href')
            }
            jobs.append(job_data)
        return jobs
    except Exception as e:
        logging.error(f"Error extracting job details: {e}")
        return []

async def scrape_remoteok_jobs(wait):
    url = f"https://remoteok.com/"
    try:
        job_items = driver.find_elements(By.XPATH, '//*[@id="jobsboard"]/tbody/tr')
        jobs = []
        for job in job_items:
            job_data = {
                "title": job.find_element(By.TAG_NAME, 'h2').text,
                "company": job.find_element(By.TAG_NAME, 'h3').text,
                "location": job.find_element(By.CLASS_NAME, 'location').text,
                "href": job.find_element(By.XPATH, './td[1]/a').get_attribute('href')
            }
            jobs.append(job_data)
        return jobs
    except Exception as e:
        logging.error(f"Error extracting job details: {e}")
        return []

async def scrape_linkedin_jobs(wait):
    url = f"https://www.linkedin.com/jobs/search/?keywords=python&location=remote"
    try:
        job_items = driver.find_elements(By.CLASS_NAME, 'base-search-card')
        jobs = []
        for job in job_items:
            job_data = {
                "title": job.find_element(By.CLASS_NAME, 'base-search-card__title').text,
                "company": job.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text,
                "location": job.find_element(By.CLASS_NAME, 'job-search-card__location').text,
                "href": job.find_element(By.TAG_NAME, 'a').get_attribute('href')
            }
            jobs.append(job_data)
        return jobs
    except Exception as e:
        logging.error(f"Error extracting job details: {e}")
        return []

@app.get("/jobs/{site}/{title}")
async def get_jobs(site: str, title: str, background_tasks: BackgroundTasks):
    # Adding background tasks to fetch jobs concurrently
    background_tasks.add_task(scrape_jobs_concurrently, site, title)
    return JSONResponse(content={"message": "Job search in progress..."})

async def scrape_jobs_concurrently(site, title):
    urls = {
        "weworkremotely": f"https://weworkremotely.com/remote-jobs/search?term={title}",
        "remotive": f"https://remotive.io/remote-jobs?query={title}",
        "remoteok": f"https://remoteok.com/remote-{title}-jobs?order_by=date",
        "linkedin": f"https://www.linkedin.com/jobs/search/?keywords={title}&location=remote"
    }
    tasks = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for site_type, url in urls.items():
            tasks.append(executor.submit(scrape_site, url, site_type))
        # Wait for all tasks to finish
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
