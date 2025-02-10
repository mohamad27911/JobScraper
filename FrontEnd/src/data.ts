import axios from "axios";

const api = axios.create({
    baseURL: "https://jobscraper-3k6f.onrender.com/",
});

const fetchJobData = async (title: string, site:string) => {
    try {
        const response = await api.get(`/jobs/${title}/${site}`);
        console.log(`Jobs Fetched Response:`, response.data);
        return response.data;
    } catch (error) {
        console.error(`Jobs fetch failed:`, error);
        throw error;
    }
};

export const FetchWeWorkRemotelyJobs = (title: string) => fetchJobData(title, "weworkremotely");
export const RemoteOkJobs = (title: string) => fetchJobData(title, "remoteok");
export const RemotiveJobs = (title: string) => fetchJobData(title, "remotive");
export const LinkedInJobs = (title: string) => fetchJobData(title, "linkedin");