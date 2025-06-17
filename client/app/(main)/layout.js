"use client";

import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';
import { useState } from 'react';

export default function MainLayout({ children }) {
  const [messages, setMessages] = useState([]);
  const [isBotOpen, setIsBotOpen] = useState(false);
  const [input, setInput] = useState('');

  // Clear messages when chatbot is closed
  const handleCloseBot = () => {
    setIsBotOpen(false);
    setMessages([]); // Reset messages on close
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { user: input, timestamp: new Date().toISOString() };
    const updatedMessages = [...messages, newMessage].slice(-10);
    setMessages(updatedMessages);
    setInput('');

    try {
      const response = await fetch(process.env.NEXT_PUBLIC_API_URL + '/bot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: updatedMessages }),
      });
      const data = await response.json();
      if (data.response) {
        setMessages((prev) => [
          ...prev,
          { bot: data.response, timestamp: new Date().toISOString() },
        ].slice(-10));
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <Header />
        <main className="p-6 bg-gray-50 min-h-screen">{children}</main>
      </div>
      {/* Chatbot Button and Window */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => setIsBotOpen(!isBotOpen)}
          className={`w-14 h-14 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full flex items-center justify-center shadow-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-300 ${
            isBotOpen ? 'scale-0 opacity-0' : 'scale-100 opacity-100 animate-bounce'
          }`}
          aria-label="Toggle chatbot"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-7 h-7"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </button>
        {isBotOpen && (
          <div
            className="text-black fixed bottom-0 right-6 w-96 bg-white rounded-t-xl shadow-2xl border border-gray-100 overflow-hidden transform transition-all duration-300 ease-in-out animate-slide-up"
          >
            <div className="flex justify-between items-center p-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-t-xl">
              <span className="font-semibold text-lg">Chatbot</span>
              <button
                onClick={handleCloseBot}
                className="text-white hover:text-gray-200 text-xl font-bold transition"
                aria-label="Close chatbot"
              >
                ✕
              </button>
            </div>
            <div className="h-80 overflow-y-auto p-4 bg-gray-50">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`mb-3 flex ${
                    msg.user ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <span
                    className={`inline-block p-3 rounded-lg max-w-[80%] ${
                      msg.user
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-800'
                    } transition-all duration-200`}
                  >
                    {msg.user || msg.bot}
                  </span>
                </div>
              ))}
            </div>
            <div className="p-4 bg-white border-t border-gray-100">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  className="flex-1 p-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition bg-gray-50 hover:bg-white"
                  placeholder="Type a message..."
                />
                <button
                  onClick={sendMessage}
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
      <style jsx>{`
        @keyframes slide-up {
          from {
            transform: translateY(100%);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }
        @keyframes bounce {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-5px);
          }
        }
        .animate-slide-up {
          animation: slide-up 0.3s ease-in-out;
        }
        .animate-bounce {
          animation: bounce 2s infinite;
        }
      `}</style>
    </div>
  );
}