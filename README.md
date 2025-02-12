
# Job Scraper using React + FastApi
This project is a job scraper API that collects remote job listings from multiple platforms and displays them in a React frontend. The backend is built using FastAPI, with Selenium handling web scraping. The frontend is developed using React, providing a seamless user experience for searching and viewing job listings.

<p align="center">
  <img src="JobsScraping.png" alt="Jobs Scraping" width="500"/>
</p>

## Full Project Link
You can view the full project here: [Job Scraper - Full Project](https://job-scraping-mohamad27911s-projects.vercel.app/)

## Table of Contents

*   [Technologies Used](#technologies-used)
*   [Getting Started](#getting-started)
*   [Backend Setup](#backend-setup)
*   [Frontend Setup](#frontend-setup)
*   [API Endpoints](#api-endpoints)
*   [Deployment](#deployment)
*   [Contributing](#contributing)

## Technologies Used

*   **Frontend**: React
*   **Backend**: FastAPI
*   **Web Scraping**: Selenium
*   **Database**: None (JSON file storage for job listings)
*   **Git**: For version control and pushing updates

## Getting Started

### Prerequisites

Before starting, ensure you have the following installed:

*   Python 3.x
*   Node.js and npm
*   Chrome WebDriver (for Selenium)
*   Git (for version control)

### Backend Setup

1.  Clone the repository:
    
    ```bash
    git clone https://github.com/mohamad27911/JobScraper.git
    git checkout dev
    ```

2.  Ensure you have Chrome WebDriver installed and properly set up.
4. Change directory to backend
     ```bash
    cd backend
    ```
2.  Create a virtual environment and install dependencies:
    
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\ctivate`
    ```
    
5. Download requirements
   ``` bash 
   pip install -r requirements.txt 
   ```
4. Change directory to src, where the main.py is located
     ```bash
    cd src
    ``` 
   
4.  Run the FastAPI server:
    
    ```bash
    uvicorn main:app --reload
    ```
    
    The API should now be running at `http://localhost:8000`.
    

### Frontend Setup

1.  Clone the frontend repository or navigate to the frontend directory:
    
    ```bash
    cd frontend
    ```

2.  Install the frontend dependencies:
    
    ```bash
    npm install
    ```

3.  Start the React development server:
    
    ```bash
    npm start
    ```
    
    The frontend should now be running at `http://localhost:5173`.
    

### Running the Application

*   The frontend will display job listings that the backend API scrapes from various job boards.
*   You can manually trigger scraping through the `/scrape-now` endpoint by clicking a button in the frontend.
*   The job listings are saved as JSON files and updated periodically every 24 hours.

## API Endpoints

*   **`/scrape-now`**: Manually triggers job scraping from various platforms.
    
    *   **Method**: `GET`
    *   **Response**: `{ "message": "Job scraping started manually" }`

*   **`/`**: Returns a simple welcome message to the API.
    
    *   **Method**: `GET`
    *   **Response**: `{ "message": "Welcome to the Job Scraper API" }`


## Deployment

For deploying the backend:

*   Choose a cloud provider or hosting solution that supports Python and selenium (I prefer Render).
*   For deployment of the frontend, you can use services like Vercel or Netlify.

### Git Integration

The project includes a Git integration to automatically push updates of scraped job listings to your repository every time new data is scraped. Make sure your local environment is set up with Git and has access to the remote repository.

## Contributing

Feel free to fork the repository and create pull requests. Contributions are welcome!
