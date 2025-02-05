import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/",
});

export const FetchWeWorkRemotelyJobs = async (title: string) => {
  try {
    const response = await api.get(`/jobs/weworkremotely/${title}`);
    console.log("Fetched Response:", response);
    return response.data;
  } catch (error) {
    console.error("FetchWeWorkRemotelyJobs failed:", error);
    throw error;
  }
};

export const RemoteOkJobs = async (title: string) => {
  try {
    const response = await api.get(`/jobs/remoteok/${title}`);
    console.log("RemoteOkJobs Fetched Response:", response);
    return response.data;
   
  } catch (error) {
    console.error("RemoteOkJobs failed:", error);
    throw error; 
  }
};

export const RemotiveJobs = async (title: string) => {
  try {
    const response = await api.get(`/jobs/remotive/${title}`);
    console.log("RemotiveJobs Fetched Response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Remotive failed:", error);
    throw error; 
  }
};

export const LinkedInJobs = async (title: string) => {
  try {
    const response = await api.get(`/jobs/linkedin/${title}`);
    console.log("LinkedIn Fetched Response:", response.data);
    return response.data; 
  } catch (error) {
    console.error("LinkedIn failed:", error);
    throw error;
  }
};
