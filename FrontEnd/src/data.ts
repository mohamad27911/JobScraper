import axios from "axios";

const api = axios.create({
  baseURL: "https://jobscraper-3k6f.onrender.com/", // Make sure this is the correct URL for your Render backend
});

const fetchJobData = async (site: string, title: string) => {
  try {
    const response = await api.get(`/jobs/${site}/${title}`);
    console.log(`${site} Fetched Response:`, response.data);
    return response.data;
  } catch (error) {
    console.error(`${site} fetch failed:`, error);
    throw error;
  }
};

export const FetchWeWorkRemotelyJobs = (title: string) => fetchJobData("weworkremotely", title);
export const RemoteOkJobs = (title: string) => fetchJobData("remoteok", title);
export const RemotiveJobs = (title: string) => fetchJobData("remotive", title);
export const LinkedInJobs = (title: string) => fetchJobData("linkedin", title);