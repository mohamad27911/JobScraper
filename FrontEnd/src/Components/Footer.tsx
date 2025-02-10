import { Github, Linkedin } from "lucide-react"
import Medium from "../assets/medium.png"

function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-gradient-to-br from-indigo-600 to-purple-700 text-white py-8 sm:py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
          <div className="text-center md:text-left">
            <h3 className="text-xl font-bold mb-2">JobScraper</h3>
            <p className="text-sm opacity-75">Aggregating opportunities from across the web</p>
          </div>
          <div className="text-center">
          </div>
          <div className="flex justify-center md:justify-end space-x-4">
            {[
              { Icon: Github, link: "https://github.com/mohamad27911" },
              { Icon: Linkedin, link: "https://www.linkedin.com/in/mohamad-abdel-rahman" },
            ].map(({ Icon, link }, index) => (
              <a
                key={index}
                href={link}
                target="_blank"
                className="hover:text-indigo-200 transition-colors duration-300"
              >
                <Icon size={28} />
              </a>
            ))}

            <a
              href="https://medium.com/@mohamad.mar72"
              target="_blank"
              className="hover:text-indigo-200 transition-colors duration-300"
            >
              <img src={Medium} alt="Medium" className="w-7 h-7" />
            </a>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-indigo-500 text-center">
          <p className="text-sm opacity-75">&copy; {currentYear} Mohamad Abdel Rahman. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
