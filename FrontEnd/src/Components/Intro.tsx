import Linkedin from "../assets/LinkedIn_icon.svg.webp";
import RemoteOk from "../assets/remoteOk.webp";
import WWR from "../assets/weWrokRemotly.png";
import Remotive from "../assets/remotive.png";

export default function Intro() {
    return (
        <div className=" text-black ">
            <div className="container mx-auto px-4 ">
                <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-center mb-6 bg-gradient-to-br from-indigo-600 to-purple-700 text-transparent bg-clip-text">
                    Search For Remote Jobs
                </h1>

                <p className="text-xl sm:text-2xl text-center mb-12 max-w-3xl mx-auto">
                    Job listings from top platforms
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 max-w-5xl mx-auto">
                    {[{
                        href: "https://www.linkedin.com/jobs/",
                        icon: Linkedin,
                        title: "LinkedIn",
                        description: "Explore job opportunities from top companies globally, with powerful networking options."
                    },
                    {
                        href: "https://remoteok.io/",
                        icon: RemoteOk,
                        title: "RemoteOk",
                        description: "Find remote jobs from startups to large enterprises across various industries."
                    },
                    {
                        href: "https://weworkremotely.com/",
                        icon: WWR,
                        title: "We Work Remotely",
                        description: "Browse remote jobs in design, marketing, customer support, and more from global employers."
                    },
                    {
                        href: "https://remotive.io/",
                        icon: Remotive,
                        title: "Remotive",
                        description: "Discover remote job opportunities, specifically curated to match your lifestyle and skills."
                    }].map((feature, index) => (
                        <a key={index} href={feature.href} target="_blank" rel="noopener noreferrer" className="flex flex-col items-center text-center p-6 bg-opacity-10 rounded-lg backdrop-blur-sm hover:bg-opacity-20 transition-colors">
                            <img src={feature.icon} alt={feature.title} className="mb-4 w-18 h-18" />
                            <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                            <p className="text-sm opacity-80">{feature.description}</p>
                        </a>
                    ))}
                </div>

                <div className="mt-16 text-center">
                    <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-center mb-6 bg-gradient-to-br from-indigo-600 to-purple-700 text-transparent bg-clip-text">
                        Start Your Job Search
                    </h2>
                </div>

            </div>
        </div>
    );
}
