'use client';
import Link from 'next/link';
import Image from 'next/image';
import graphPic from "@/public/graph.png";
import HomeHeader from '@/components/HomeHeader';
import HomeFooter from '@/components/HomeFooter';
import { useState, useEffect } from 'react';

export default function LandingPage() {
  const [userName, setUserName] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/protected`, {
          method: 'GET',
          credentials: 'include', // Include cookies for authentication
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) throw new Error('Failed to fetch user data');

        const data = await response.json();
        setUserName(data.full_name.toUpperCase() || 'User'); // Use full_name from backend response
      } catch (error) {
        console.error('Error fetching user data:', error);
        setUserName(null); // No name if fetch fails
      }
    };

    fetchUserData();
  }, []);

  return (
    <div className="min-h-screen bg-[#0B1340] text-white font-sans">
      {/* Header */}
      <HomeHeader />

      {/* Welcome Message */}
      
      {/* Hero Section */}
      <section className="flex flex-col md:flex-row items-center justify-between p-10 md:p-20 bg-[#0B1340] bg-opacity-10">
        <div className="max-w-lg">
    {userName && (
          <h2 className="text-5xl font-bold leading-tight text-[#E0F2FE]">Welcome Back, {userName}!</h2>
        )}

          <h2 className="text-5xl font-bold mb-6 leading-tight text-[#E0F2FE]">Smarter Investing with TRADENEXUS AI</h2>
          <p className="text-[#A5BFFA] text-lg mb-8">
            Dive into a seamless financial journey with TRADENEXUS AI. Harness real-time market insights, AI-driven trading recommendations, and personalized portfolio strategies powered by cutting-edge technologies like Hugging Face Transformers, Next.js, and Flask.
          </p>
          <div className="flex space-x-4">
            <Link href="/portfolio" className="bg-[#38BDF8] hover:bg-[#7DD3FC] text-white px-6 py-3 rounded-lg font-medium transition">
              Get Started
            </Link>
            <Link href="/demo" className="border border-[#A5BFFA] text-[#A5BFFA] px-6 py-3 rounded-lg font-medium hover:bg-[#0B1340] transition">
              Watch Demo
            </Link>
          </div>
        </div>
        <div className="mt-10 md:mt-0 md:ml-10">
          <Image src={graphPic} alt="Financial Graph" width={600} height={400} className="rounded-lg shadow-xl transform hover:scale-105 transition" />
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-[#FFFFFF] text-[#0B1340] py-16 px-8 md:px-20" id='features'>
        <h3 className="text-4xl font-bold text-center mb-12 text-[#0B1340]">Why Choose TRADENEXUS AI?</h3>
        <div className="grid md:grid-cols-3 gap-10">
          {[
            {
              title: 'AI-Powered Insights',
              desc: 'Leverage advanced Hugging Face Transformers and ML models like Random Forest for precise, personalized buy/sell recommendations tailored to your risk profile.',
              icon: '🧠',
            },
            {
              title: 'Real-Time Market Data',
              desc: 'Access live stock performance, technical indicators (RSI, MACD, SMA), and fundamental metrics (EPS, P/E Ratio) via yfinance integration.',
              icon: '📊',
            },
            {
              title: 'Sentiment Analysis',
              desc: 'Understand market sentiment with NLP-powered analysis of 5-7 real-time news headlines using BERT and VADER models.',
              icon: '📰',
            },
            {
              title: 'Smart Portfolio Management',
              desc: 'Track gains/losses, visualize asset allocation, and optimize strategies with intuitive dashboards and real-time analytics.',
              icon: '📈',
            },
            {
              title: 'Conversational AI Assistant',
              desc: 'Engage with an NLP-powered chatbot that explains market trends, answers queries, and boosts financial literacy.',
              icon: '💬',
            },
            {
              title: 'Secure & Scalable',
              desc: 'Built with Flask backend, Next.js frontend, and robust encryption to ensure data privacy and seamless performance across devices.',
              icon: '🔒',
            },
          ].map((feature, i) => (
            <div key={i} className="bg-[#F0F9FF] rounded-lg p-6 shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4 text-[#38BDF8]">{feature.icon}</div>
              <h4 className="text-xl font-semibold mb-2">{feature.title}</h4>
              <p className="text-[#1E3A8A]">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-[#0B1340] text-white py-16 px-8 md:px-20">
        <h3 className="text-4xl font-bold text-center mb-12 text-[#A5BFFA]">How TRADENEXUS AI Works</h3>
        <div className="grid md:grid-cols-4 gap-8">
          {[
            {
              step: 'Step 1: Data Aggregation',
              desc: 'Collects real-time stock data, news feeds, and fundamental metrics using yfinance, BeautifulSoup4, and feedparser.',
            },
            {
              step: 'Step 2: Weighted Fusion Analysis',
              desc: 'Combines technical (40%), fundamental (30%), and sentiment (30%) analyses for accurate buy/sell signals.',
            },
            {
              step: 'Step 3: Predictive Modeling',
              desc: 'Uses Hugging Face Transformers and ML models to generate tailored trading recommendations.',
            },
            {
              step: 'Step 4: Actionable Insights',
              desc: 'Delivers personalized strategies and live portfolio tracking via an intuitive Next.js interface.',
            },
          ].map((step, i) => (
            <div key={i} className="text-center">
              <div className="bg-[#38BDF8] text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 font-bold">{i + 1}</div>
              <h4 className="text-xl font-semibold mb-2 text-[#A5BFFA]">{step.step}</h4>
              <p className="text-[#A5BFFA]">{step.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="bg-[#FFFFFF] text-[#0B1340] py-16 px-8 md:px-20">
        <h3 className="text-4xl font-bold text-center mb-12">What Our Users Say</h3>
        <div className="grid md:grid-cols-2 gap-10">
          {[
            {
              quote: 'TRADENEXUS AI transformed my trading experience with its accurate recommendations and easy-to-use interface.',
              author: 'Sarah K., Retail Investor',
            },
            {
              quote: 'The sentiment analysis feature gives me an edge in understanding market trends like never before.',
              author: 'James R., Day Trader',
            },
          ].map((testimonial, i) => (
            <div key={i} className="bg-[#F0F9FF] rounded-lg p-6 shadow-md">
              <p className="text-[#1E3A8A] italic mb-4">&quot;{testimonial.quote}&quot;</p>
              <p className="text-[#0B1340] font-semibold">{testimonial.author}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-[#0B1340] bg-opacity-10 text-white py-20 px-10 text-center">
        <h3 className="text-4xl font-bold mb-6">Join the Future of Investing</h3>
        <p className="text-lg mb-8 max-w-2xl mx-auto">
          Empower your financial decisions with TRADENEXUS AI. Start trading smarter with AI-driven insights, real-time analytics, and personalized strategies.
        </p>
        <Link href="/portfolio" className="bg-[#FFFFFF] text-[#0B1340] px-8 py-4 font-semibold rounded-lg hover:bg-[#F0F9FF] transition">
          Start Your Journey Today
        </Link>
      </section>

      {/* Separation Line */}
      <hr className="border-t border-[#A5BFFA] mx-auto w-3/4" />
      <HomeFooter/>
    </div>
  );
}