import { ArrowUpRight } from "lucide-react"

interface Job{
    title:string,
    company:string,
    location:string,
    posted:string,
    type:string,
    href:string,
    img:string
}
export const JobCard = ({ title, company, location, posted, href, img, type }:Job) => {
    
    return (
      <a
      target="_blank"
        href={href}
        className="flex flex-col gap-3 sm:gap-4 overflow-hidden rounded-lg bg-white shadow-md transition-all duration-300 hover:shadow-xl hover:scale-105 p-4 sm:p-6"
      >
        <div className="flex flex-col sm:flex-row justify-between items-center gap-3 sm:gap-8">
          <img
            className="w-12 h-12 sm:w-16 sm:h-16 rounded-full object-contain border-2 border-indigo-700"
            src={img || "/placeholder.svg"}
            alt=""
          />
          <span className="bg-indigo-700 text-gray-300 text-xs sm:text-sm font-bold px-3 py-1 sm:px-4 sm:py-2 rounded-xl">
            {type}
          </span>
        </div>
        <h1 className="text-lg sm:text-xl font-bold text-gray-800">{title}</h1>
        <h2 className="text-sm sm:text-base text-gray-600">{company}</h2>
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between text-xs sm:text-sm text-gray-500 gap-2 sm:gap-4">
          <span>{location}</span>
          <span>Posted: {posted}</span>
        </div>
        <div className="flex justify-end items-center gap-2 text-indigo-700">
        <span className="text-xs sm:text-sm font-medium hover:underline transition-all duration-300">View Job</span>
        <ArrowUpRight className="w-4 h-4 sm:w-5 sm:h-5" />
      </div>
      </a>
    )
  }
  
  