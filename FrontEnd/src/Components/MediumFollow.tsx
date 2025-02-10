import { ArrowRight } from 'lucide-react'
import pfp from "../assets/me.jpg"
export default function MediumFollow() {
    return (
        <section className="py-16 px-4 sm:px-6 lg:px-8 mb-16 text-black">
            <div className="max-w-4xl mx-auto text-center">
                <div className="flex justify-center mb-8">
                    <div className="relative w-82 h-82 p-1 rounded-full bg-gradient-to-r from-indigo-600 to-purple-700">
                        <img
                            src={pfp}
                            alt="Profile Picture"
                            className="rounded-full w-full h-full object-cover object-center bg-white p-1"
                        />
                    </div>

                </div>
                <h2 className="text-3xl sm:text-4xl font-extrabold  mb-4">
                    Big things are on the way
                </h2>
                <p className="text-xl  mb-8">
                    Follow me on <b className='bg-gradient-to-br from-indigo-600 to-purple-700 text-transparent bg-clip-text'>Medium</b>, I'll be sharing my first post soon.
                </p>
                <a
                    href="https://medium.com/@mohamad.mar72"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-gradient-to-r from-indigo-600 to-purple-700  hover:bg-indigo-50 transition duration-150 ease-in-out"
                >
                    Follow on Medium
                    <ArrowRight className="ml-2 -mr-1 h-5 w-5" aria-hidden="true" />
                </a>
            </div>
        </section>
    )
}
