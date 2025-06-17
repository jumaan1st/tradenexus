'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { useEffect } from 'react';
import { useGlobalContext } from '@/context/GlobalContext';

export default function StocksForm() {

  const [company, setCompany] = useState('');
  const router = useRouter();
   const { setCurrentPageTitle } = useGlobalContext();

  useEffect(() => {
    setCurrentPageTitle('Predict Stock Price');
  }, [setCurrentPageTitle]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (company.trim()) {
      router.push(`/stocks/${encodeURIComponent(company)}`);
    }
  };

  return (
    <div className="ml-64 p-8 flex justify-center">
      <section className="bg-white shadow p-6 rounded-lg w-full max-w-2xl">
        <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">
          Search Company Stock
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            placeholder="Enter company name"
            className="w-full border p-2 rounded text-gray-700"
          />
          <button
            type="submit"
            className="w-full bg-gray-800 text-white py-2 rounded hover:bg-gray-900 transition"
          >
            Search
          </button>
        </form>
      </section>
    </div>
  );
}