import { JobCard } from "./Components/JobCard";
import Intro from "./Components/Intro";
import Footer from "./Components/Footer";
import { FetchWeWorkRemotelyJobs, LinkedInJobs, RemoteOkJobs, RemotiveJobs } from "./data";
import { useEffect, useState} from "react";
import Select, { SingleValue } from "react-select";
import {SearchX } from "lucide-react";

// Define the type for your options
interface Option {
  value: string;
  label: string;
}

const options: Option[] = [
  { value: "Engineer", label: "Engineer" },
  { value: "Executive", label: "Executive" },
  { value: "Senior", label: "Senior" },
  { value: "Developer", label: "Developer" },
  { value: "Finance", label: "Finance" },
  { value: "Sys Admin", label: "Sys Admin" },
  { value: "JavaScript", label: "JavaScript" },
  { value: "Backend", label: "Backend" },
  { value: "Golang", label: "Golang" },
  { value: "Cloud", label: "Cloud" },
  { value: "Medical", label: "Medical" },
  { value: "Front End", label: "Front End" },
  { value: "Full Stack", label: "Full Stack" },
  { value: "Ops", label: "Ops" },
  { value: "Design", label: "Design" },
  { value: "React", label: "React" },
  { value: "InfoSec", label: "InfoSec" },
  { value: "Marketing", label: "Marketing" },
  { value: "Mobile", label: "Mobile" },
  { value: "Content Writing", label: "Content Writing" },
  { value: "SaaS", label: "SaaS" },
  { value: "Recruiter", label: "Recruiter" },
  { value: "Full Time", label: "Full Time" },
  { value: "API", label: "API" },
  { value: "Sales", label: "Sales" },
  { value: "Ruby", label: "Ruby" },
  { value: "Education", label: "Education" },
  { value: "DevOps", label: "DevOps" },
  { value: "Stats", label: "Stats" },
  { value: "Python", label: "Python" },
  { value: "Node", label: "Node" },
  { value: "English", label: "English" },
  { value: "Non Tech", label: "Non Tech" },
  { value: "Video", label: "Video" },
  { value: "Travel", label: "Travel" },
  { value: "Quality Assurance", label: "Quality Assurance" },
  { value: "Ecommerce", label: "Ecommerce" },
  { value: "Teaching", label: "Teaching" },
  { value: "Linux", label: "Linux" },
  { value: "Java", label: "Java" },
  { value: "Crypto", label: "Crypto" },
  { value: "Junior", label: "Junior" },
  { value: "Git", label: "Git" },
  { value: "Legal", label: "Legal" },
  { value: "Android", label: "Android" },
  { value: "Accounting", label: "Accounting" },
  { value: "Admin", label: "Admin" },
  { value: "Microsoft", label: "Microsoft" },
  { value: "Excel", label: "Excel" },
  { value: "PHP", label: "PHP" },
  { value: "Amazon", label: "Amazon" },
  { value: "Serverless", label: "Serverless" },
  { value: "CSS", label: "CSS" },
  { value: "Software", label: "Software" },
  { value: "Analyst", label: "Analyst" },
  { value: "Angular", label: "Angular" },
  { value: "iOS", label: "iOS" },
  { value: "Customer Support", label: "Customer Support" },
  { value: "HTML", label: "HTML" },
  { value: "Salesforce", label: "Salesforce" },
  { value: "Ads", label: "Ads" },
  { value: "Product Designer", label: "Product Designer" },
  { value: "HR", label: "HR" },
  { value: "SQL", label: "SQL" },
  { value: "C", label: "C" },
  { value: "Web Developer", label: "Web Developer" },
  { value: "NoSQL", label: "NoSQL" },
  { value: "Postgres", label: "Postgres" },
  { value: "C Plus Plus", label: "C Plus Plus" },
  { value: "Part Time", label: "Part Time" },
  { value: "Jira", label: "Jira" },
  { value: "C Sharp", label: "C Sharp" },
  { value: "SEO", label: "SEO" },
  { value: "Apache", label: "Apache" },
  { value: "Data Science", label: "Data Science" },
  { value: "Virtual Assistant", label: "Virtual Assistant" },
  { value: "React Native", label: "React Native" },
  { value: "Mongo", label: "Mongo" },
  { value: "Testing", label: "Testing" },
  { value: "Architecture", label: "Architecture" },
  { value: "Director", label: "Director" },
  { value: "Music", label: "Music" },
  { value: "Shopify", label: "Shopify" },
  { value: "Wordpress", label: "Wordpress" },
  { value: "Laravel", label: "Laravel" },
  { value: "Elasticsearch", label: "Elasticsearch" },
  { value: "Blockchain", label: "Blockchain" },
  { value: "Web3", label: "Web3" },
  { value: "Drupal", label: "Drupal" },
  { value: "Docker", label: "Docker" },
  { value: "GraphQL", label: "GraphQL" },
  { value: "Payroll", label: "Payroll" },
  { value: "Internship", label: "Internship" },
  { value: "Machine Learning", label: "Machine Learning" },
  { value: "Architect", label: "Architect" },
  { value: "Scala", label: "Scala" },
  { value: "Web", label: "Web" },
  { value: "Objective C", label: "Objective C" },
  { value: "Social Media", label: "Social Media" },
  { value: "Vue", label: "Vue" }
];

function App() {
  const [jobs, setJobs] = useState([]);
  const [job, setJob] = useState(""); // Default job
  const [isLoading, setIsLoading] = useState(false);
  const [selectedOption, setSelectedOption] = useState<SingleValue<Option>>(null);

  useEffect(() => {
    if (job) {
      fetchJobs(); // Trigger the job fetch when job state changes
    }
  }, [job]); // Dependency on job state

  const fetchJobs = async () => {
    setIsLoading(true);
    setJobs([]); // Clear previous jobs before fetching

    try {
      const jobSources = [
        LinkedInJobs(job),
        FetchWeWorkRemotelyJobs(job),
        RemoteOkJobs(job),
        RemotiveJobs(job),
      ];

      const responses = await Promise.all(jobSources);

      const allJobs = responses.reduce((acc, response) => {
        if (Array.isArray(response)) {
          return [...acc, ...response];
        } else if (response.jobs) {
          return [...acc, ...response.jobs];
        }
        return acc;
      }, []);
      console.log("All Jobs:", allJobs);
      setJobs(allJobs);
    } catch (error) {
      console.error("Error fetching jobs:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (newValue: SingleValue<Option>) => {
    setSelectedOption(newValue);
  };

  const handleSearch = () => {
    if (selectedOption) {
      console.log("Searching for:", selectedOption.value);
      setJob(selectedOption.value); // Set the job state and trigger useEffect to fetch jobs
    } else {
      console.log("No option selected");
    }
  };

  const funFacts = [
    "Over 30% of employees worldwide work remotely at least once a week. The future of work is flexible!",
    "The first job search engine was launched in 1996. It’s come a long way since then—now, job hunting is just a click away!",
    "Did you know? The average person applies to 20-30 jobs before landing an offer. Persistence is key!",
    "Remote work can save employees up to 40 minutes a day in commuting time. That’s almost 3 hours a week for more coffee breaks!",
    "In the tech industry, 60% of companies say they have difficulty finding skilled candidates. So, you’re in demand!",
    "More than 80% of job seekers are now using their phones to apply for jobs. Your next career move could be just a tap away!",
    "The term 'headhunter' comes from the 1950s when recruitment firms would literally seek out the best talent like a hunter seeking its prey.",
    "The average job seeker spends 11 hours per week searching for work. That’s the equivalent of a part-time job!",
    "In the world of remote jobs, the highest paying ones often come from tech and software development industries. Code your way to the top!",
    "There’s a rise in 'flexible job' listings, where employees can choose their hours and location—perfect for the digital nomad lifestyle."
  ];


  return (
    <>
      <div className="min-h-screen bg-gray-100 py-8 px-4 sm:py-12 sm:px-6 lg:px-8">
        <Intro />
        <div className="flex justify-between items-center gap-4 flex-col sm:flex-row mb-16 mx-auto container w-3/5">
          <div className="w-full">
            <Select
              options={options}
              value={selectedOption}
              onChange={handleChange}
              isSearchable
              placeholder="Select Job Title"
            />
          </div>
          <button
            onClick={handleSearch}
            className="bg-indigo-700 border-2 text-white font-bold hover:border-indigo-700 hover:text-indigo-700 hover:bg-white px-4 py-2 rounded-xl transition-all duration-300 cursor-pointer w-full sm:w-auto"
          >
            Search
          </button>
        </div>
        <div className="max-w-7xl mx-auto">

          {isLoading ? (
            <div className="flex flex-col items-center justify-center  bg-white text-gray-800">
              <div className="w-24 h-24 mb-8">
                <svg className="animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  >
                    <animateTransform
                      attributeName="transform"
                      type="rotate"
                      from="0 12 12"
                      to="360 12 12"
                      dur="1s"
                      repeatCount="indefinite"
                    />
                  </path>
                </svg>
              </div>
              <h2 className="text-3xl font-bold mb-6 animate-pulse bg-gradient-to-r from-indigo-600 to-purple-700 bg-clip-text text-transparent">
                Hunting for Jobs...
              </h2>
              <div className="text-center max-w-md px-4">
                <p className="mb-4 text-lg font-semibold text-indigo-600">Did you know?</p>
                <p className="italic text-purple-600">{funFacts[Math.floor(Math.random() * funFacts.length)]}</p>
              </div>
            </div>
          ) : jobs.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 px-4 bg-white text-gray-800">
              <SearchX className="w-24 h-24 text-indigo-600 mb-6" />
              <h2 className="text-3xl font-bold mb-4 text-center bg-gradient-to-r from-indigo-600 to-purple-700 bg-clip-text text-transparent">
                No jobs found for your search
              </h2>
              <p className="text-lg text-gray-600 mb-8 text-center max-w-md">
                Don't worry! New opportunities are added frequently. Try adjusting your search or check back later.
              </p>

            </div>
          ) : (
            <div><h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-6 sm:mb-8 text-center">
              Job Listings
            </h1>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                {jobs.filter(job => job.title !== "Unknown").map((card, index) => (
                  <JobCard key={index} {...card} />
                ))}

              </div></div>
          )}
        </div>
      </div>
      <Footer />
    </>
  );
}

export default App;
