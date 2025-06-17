'use client';
import Link from 'next/link';
import Image from 'next/image';
import HomeHeader from '@/components/HomeHeader';
import HomeFooter from '@/components/HomeFooter';
import myImage from '@/public/about.jpeg'

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-[#0B1340] text-white font-sans">
      {/* Header */}
      <HomeHeader />

      {/* Project Overview Section */}
      <section className="bg-gradient-to-b from-[#0B1340] to-[#1E3A8A] py-20 px-8 md:px-20">
        <h2 className="text-5xl font-bold text-center mb-12 text-[#E0F2FE] tracking-wide">About TRADENEXUS AI</h2>
        <div className="flex flex-col md:flex-row items-center justify-between gap-12 max-w-6xl mx-auto">
          <div className="md:w-1/2">
            <p className="text-[#A5BFFA] text-lg leading-relaxed mb-6">
              TRADENEXUS AI is a pioneering AI-powered platform designed to transform financial decision-making for individual investors. Developed by a dedicated team at the Department of Computer Science & Engineering, Maharaja Institute of Technology Mysore, our platform leverages real-time financial data, advanced sentiment analysis, and predictive machine learning algorithms to deliver intelligent trading recommendations and automated investment strategies. Built with cutting-edge technologies like Hugging Face Transformers, Random Forest, Next.js, and Flask, TRADENEXUS AI empowers users with institutional-grade financial intelligence, optimizing portfolio performance and enhancing decision-making precision.
            </p>
          </div>
          <div className="md:w-1/2">
            <Image
              src={myImage}
              alt="AI-Driven Financial Dashboard"
              width={500}
              height={400}
              className="rounded-xl shadow-2xl border-4 border-[#A5BFFA] transform hover:scale-[1.02] transition duration-500 w-full"
            />
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="bg-[#FFFFFF] text-[#0B1340] py-20 px-8 md:px-20">
        <h2 className="text-5xl font-bold text-center mb-16 text-[#0B1340] tracking-wide">Meet Our Team</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12">
          {[
{
"name": "Moin Shariff",
"usn": "4MH22CS094",
"bio": "A creative thinker with expertise in AI-driven solutions, Moin leads backend development for TRADENEXUS AI, leveraging Ollama and Gemini API for financial predictions and sentiment analysis.",
"image": "https://images.unsplash.com/photo-1522556189639-b1509e2e5306?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80",
"github": "https://github.com/moinshariff",
"linkedin": "https://linkedin.com/in/moinshariff"
},
{
"name": "Mohamed Sufyan",
"usn": "4MH22CS092",
"bio": "A tech enthusiast with a focus on AI and finance, Mohamed develops intuitive UI/UX for TRADENEXUS AI’s frontend, ensuring a seamless and accessible user experience.",
"image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80",
"github": "https://github.com/mohamedsufyan",
"linkedin": "https://linkedin.com/in/mohamedsufyan"
},
{
"name": "Mohammed Maaz",
"usn": "4MH22CS093",
"bio": "A skilled coder specializing in machine learning, Maaz manages TRADENEXUS AI’s database, ensuring robust data handling and security for real-time analytics.",
"image": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80",
"github": "https://github.com/mohammedmaaz",
"linkedin": "https://linkedin.com/in/mohammedmaaz"
},
{
"name": "Usama Azeem",
"usn": "4MH23CS412",
"bio": "An expert in backend systems and cybersecurity, Usama develops TRADENEXUS AI’s data visualizations and conversational AI, enhancing user interaction and insights.",
"image": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80",
"github": "https://github.com/usamaazeem",
"linkedin": "https://linkedin.com/in/usamaazeem"
}
].map((member, i) => (
            <div
              key={i}
              className="bg-[#F0F9FF] rounded-xl p-8 shadow-lg transform hover:shadow-2xl transition duration-500 flex flex-col items-center border border-[#A5BFFA]/20"
            >
              <Image
                src={member.image}
                alt={member.name}
                width={150}
                height={150}
                className="rounded-full mb-6 border-4 border-[#38BDF8] hover:border-[#A5BFFA] transition duration-300 shadow-md"
              />
              <h4 className="text-2xl font-semibold mb-2 text-[#0B1340]">{member.name}</h4>
              <p className="text-[#1E3A8A] mb-4 font-medium">{member.usn}</p>
              <p className="text-[#1E3A8A] text-center mb-6 leading-relaxed">{member.bio}</p>
              <div className="flex space-x-4">
                <a href={member.github} target="_blank" rel="noopener noreferrer" className="text-[#38BDF8] hover:text-[#A5BFFA] transition duration-300">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26.81-1 1.39-1.9 1.39h-1v-3c0-.55-.45-1-1-1H8.1l4.9-4.9 1.4 1.4c.39.39 1.02.39 1.41 0 .39-.39.39-1.02 0-1.41L12 7.1l-4.9 4.9H7c-.55 0-1 .45-1 1v3H5c-1.1 0-2-.9-2-2v-1.9c0-3.95 3.05-7.31 7-7.93V5c0 3.95 3.05 7.31 7 7.93v1.9c0 1.1-.9 2-2 2z" />
                  </svg>
                </a>
                <a href={member.linkedin} target="_blank" rel="noopener noreferrer" className="text-[#38BDF8] hover:text-[#A5BFFA] transition duration-300">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 0h-14c-2.76 0-5 2.24-5 5v14c0 2.76 2.24 5 5 5h14c2.76 0 5-2.24 5-5v-14c0-2.76-2.24-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.5c-.97 0-1.75-.78-1.75-1.75s.78-1.75 1.75-1.75 1.75.78 1.75 1.75-.78 1.75-1.75 1.75zm13.5 12.5h-3v-5.5c0-1.38-1.12-2.5-2.5-2.5s-2.5 1.12-2.5 2.5v5.5h-3v-11h3v1.5c.89-1.11 2.34-1.5 3.5-1.5 2.76 0 5 2.24 5 5v6z" />
                  </svg>
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Contact Section */}
      <section className="bg-gradient-to-b from-[#1E3A8A] to-[#0B1340] text-white py-20 px-10 text-center">
        <h3 className="text-4xl font-bold mb-8 text-[#E0F2FE] tracking-wide">Get in Touch</h3>
        <p className="text-lg mb-10 max-w-2xl mx-auto text-[#A5BFFA] leading-relaxed">
          Want to learn more about TRADENEXUS AI or collaborate with our team? Reach out to us today!
        </p>
        <Link href="mailto:support@tradenexus.ai" className="bg-[#38BDF8] hover:bg-[#7DD3FC] text-white px-8 py-4 rounded-lg font-semibold transition duration-300 shadow-lg">
          Contact Us
        </Link>
      </section>

      {/* Separation Line */}
      <hr className="border-t border-[#A5BFFA] mx-auto w-3/4" />

      {/* Footer */}
      <HomeFooter />
    </div>
  );
}