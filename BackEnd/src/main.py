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
import os
import logging
import asyncio

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

# Use a single, shared WebDriver instance
driver = None

def create_driver():
    """Creates and configures the Chrome driver."""
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        try:
            driver = webdriver.Chrome(options=options)
            logging.info("Chrome driver initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing Chrome driver: {e}")
            raise  # Re-raise the exception to prevent the app from starting

@app.on_event("startup")
async def startup_event():
    create_driver()

@app.on_event("shutdown")
def shutdown_event():
    global driver
    if driver:
        driver.quit()
        logging.info("Chrome driver quit successfully.")

def scrape_weworkremotely_jobs(title):
    """Scrapes job listings from We Work Remotely."""
    url = f"https://weworkremotely.com/remote-jobs/search?term={title}"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        jobs = []
        job_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#category-17 > article > ul > li:not(.view-all)')))
        for job in job_elements:
            try:
                title = job.find_element(By.CSS_SELECTOR, 'span.title').text
                company = job.find_element(By.CSS_SELECTOR, 'span.company').text
                location = job.find_element(By.CSS_SELECTOR, 'span.region').text
                link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                img = job.find_element(By.CSS_SELECTOR, 'span.flag-logo').get_attribute('style')
                job_data = {"title": title, "company": company, "location": location, "link": link, "img": img}
                jobs.append(job_data)
            except Exception as e:
                logging.error(f"Error extracting job details from WeWorkRemotely: {e}")
        return jobs
    except Exception as e:
        logging.error(f"Error scraping WeWorkRemotely: {e}")
        return []

@app.get("/jobs/weworkremotely/{title}")
async def get_weworkremotely_jobs(title: str):
    jobs = scrape_weworkremotely_jobs(title)
    return JSONResponse(content=jobs)

def scrape_remotive_jobs(title):
    """Scrapes job listings from Remotive."""
    url = f"https://remotive.io/remote-jobs?query={title}"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        jobs = []
        job_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#hits > ul > div[x-data]')))
        for job in job_elements:
            try:
                title = job.find_element(By.CSS_SELECTOR, 'a.remotive-url-visit').text
                company = job.find_element(By.CSS_SELECTOR, 'div.company').text
                location = job.find_element(By.CSS_SELECTOR, 'div.location').text
                link = job.find_element(By.CSS_SELECTOR, 'a.remotive-url-visit').get_attribute('href')
                img = job.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                job_data = {"title": title, "company": company, "location": location, "link": link, "img": img}
                jobs.append(job_data)
            except Exception as e:
                logging.error(f"Error extracting job details from Remotive: {e}")
        return jobs
    except Exception as e:
        logging.error(f"Error scraping Remotive: {e}")
        return []

@app.get("/jobs/remotive/{title}")
async def get_remotive_jobs(title: str):
    jobs = scrape_remotive_jobs(title)
    return JSONResponse(content=jobs)

def scrape_remoteok(title):
    """Scrapes job listings from RemoteOK."""
    url = f"https://remoteok.com/remote-{title}-jobs"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        jobs = []
        job_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#jobsboard > tbody > tr[class*="job"]')))
        for job in job_elements:
            try:
                title = job.find_element(By.CSS_SELECTOR, 'h2').text
                company = job.find_element(By.CSS_SELECTOR, 'h3').text
                location = job.find_element(By.CSS_SELECTOR, 'div.location').text
                link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                img = job.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                job_data = {"title": title, "company": company, "location": location, "link": link, "img": img}
                jobs.append(job_data)
            except Exception as e:
                logging.error(f"Error extracting job details from RemoteOK: {e}")
        return jobs
    except Exception as e:
        logging.error(f"Error scraping RemoteOK: {e}")
        return []

@app.get("/jobs/remoteok/{title}")
async def get_remoteok_jobs(title: str):
    jobs = scrape_remoteok(title)
    return JSONResponse(content=jobs)

def linkedInJobs(title):
    """Scrapes job listings from LinkedIn."""
    url = f"https://www.linkedin.com/jobs/search/?keywords={title}&location=remote"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        jobs = []
        job_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.job-search-card')))
        for job in job_elements:
            try:
                title = job.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title').text
                company = job.find_element(By.CSS_SELECTOR, 'a.base-search-card__subtitle').text
                location = job.find_element(By.CSS_SELECTOR, 'div.job-search-card__location').text
                link = job.find_element(By.CSS_SELECTOR, 'a.base-card__full-link').get_attribute('href')
                img = job.find_element(By.CSS_SELECTOR, 'img.lazy-loaded').get_attribute('src')
                job_data = {"title": title, "company": company, "location": location, "link": link, "img": img}
                jobs.append(job_data)
            except Exception as e:
                logging.error(f"Error extracting job details from LinkedIn: {e}")
        return jobs
    except Exception as e:
        logging.error(f"Error scraping LinkedIn: {e}")
        return []

@app.get("/jobs/linkedin/{title}")
async def get_linkedin_jobs(title: str):
    jobs = linkedInJobs(title)
    return JSONResponse(content=jobs)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)