import { useState } from "react";
import Select, { SingleValue } from "react-select";

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


function FilterInput() {
  const [selectedOption, setSelectedOption] = useState<SingleValue<Option>>(null);

  const handleChange = (newValue: SingleValue<Option>) => {
    setSelectedOption(newValue);
  };

  const handleSearch = () => {
    if (selectedOption) {
      console.log("Searching for:", selectedOption.value);
    } else {
      console.log("No option selected");
    }
  };

  return (
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
  );
}

export default FilterInput;
