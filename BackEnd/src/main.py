from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from selenium.webdriver.support.ui import Select
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://job-scraping-mohamad27911s-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/jobs/{title}/{site}")
async def get_jobs(title: str, site: str):
    jobs = await scrape_jobs(title, site)
    return JSONResponse(content=jobs)

async def scrape_jobs(title: str, site: str):
    """Helper function for job scraping on each site"""
    try:
        if site == "weworkremotely":
            return await scrape_weworkremotely_jobs(title)
        elif site == "remotive":
            return await scrape_remotive_jobs(title)
        elif site == "remoteok":
            return await remoteokJobs(title)
        elif site == "linkedin":
            return await linkedInJobs(title)
        else:
            raise HTTPException(status_code=400, detail="Invalid site")

    except Exception as e:
        logging.error(f"Error scraping {site}: {e}")
        return []

async def scrape_weworkremotely_jobs(title):
    """Scrapes job listings from We Work Remotely."""
    url = f"https://weworkremotely.com/remote-jobs/search?term={title}"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        jobs = []
        try:
            jobs_list = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="category-17"]/article/ul')))
            job_items = jobs_list.find_elements(By.TAG_NAME, 'li')
            
            for job in job_items:
                if "view-all" in job.get_attribute('class'):
                    continue
                job_data = {
                    "title": job.find_element(By.CLASS_NAME, 'title').text,
                    "company": job.find_element(By.CLASS_NAME, 'company').text,
                    "location": job.find_element(By.CLASS_NAME, 'region.company').text,
                    "href": job.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                    "site": "weworkremotely"
                }
                jobs.append(job_data)
        except Exception as e:
            logging.error(f"Error extracting job details from WeWorkRemotely: {e}")
        return jobs
    except Exception as e:
        logging.error(f"Error scraping WeWorkRemotely: {e}")
        return []

async def scrape_remotive_jobs(title):
    """Scrapes job listings from Remotive."""
    url = f"https://remotive.io/remote-jobs?query={title}"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        jobs = []
        try:
            job_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#hits > ul > div[x-data]')))
            for job in job_items:
                job_data = {
                    "title": job.find_element(By.CSS_SELECTOR, '.remotive-bold').text,
                    "company": job.find_element(By.CSS_SELECTOR, '.remotive-bold').text,
                    "location": job.find_element(By.CSS_SELECTOR, '.tag-small').text,
                    "href": job.find_element(By.CSS_SELECTOR, 'a.remotive-url-visit').get_attribute('href'),
                    "site": "remotive"
                }
                jobs.append(job_data)
        except Exception as e:
            logging.error(f"Error extracting job details from Remotive: {e}")
        return jobs
    except Exception as e:
        logging.error(f"Error scraping Remotive: {e}")
        return []

async def remoteokJobs(title):
    """Scrapes job listings from RemoteOK."""
    url = f"https://remoteok.com/remote-{title}-jobs"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        jobs = []
        try:
            job_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#jobsboard > tbody > tr[class*="job"]')))
            for job in job_items:
                job_data = {
                    "title": job.find_element(By.TAG_NAME, 'h2').text,
                    "company": job.find_element(By.TAG_NAME, 'h3').text,
                    "location": job.find_element(By.CLASS_NAME, 'location').text,
                    "href": job.find_element(By.XPATH, './td[1]/a').get_attribute('href'),
                    "site": "remoteok"
                }
                jobs.append(job_data)
        except Exception as e:
            logging.error(f"Error extracting job details from RemoteOK: {e}")
        return jobs
    except Exception as e:
        logging.error(f"Error scraping RemoteOK: {e}")
        return []

async def linkedInJobs(title):
    """Scrapes job listings from LinkedIn."""
    url = f"https://www.linkedin.com/jobs/search/?keywords={title}&location=remote"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        jobs = []
        try:
            job_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'base-search-card')))
            for job in job_items:
                try:
                    title = job.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title').text
                    company = job.find_element(By.CSS_SELECTOR, 'a.base-search-card__subtitle').text
                    location = job.find_element(By.CSS_SELECTOR, 'div.job-search-card__location').text
                    link = job.find_element(By.CSS_SELECTOR, 'a.base-card__full-link').get_attribute('href')
                    job_data = {"title": title, "company": company, "location": location, "link": link, "site": "linkedin"}
                    jobs.append(job_data)
                except Exception as e:
                    logging.error(f"Error extracting job details from LinkedIn: {e}")
            return jobs
        except Exception as e:
            logging.error(f"Linkedin scrape wait error: {e}")
            return []
    except Exception as e:
        logging.error(f"Error scraping LinkedIn: {e}")
        return []

@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)