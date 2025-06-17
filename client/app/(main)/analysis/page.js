'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useEffect } from 'react';
import { useGlobalContext } from '@/context/GlobalContext';

export default function InvestmentAnalysis() {
   const { setCurrentPageTitle } = useGlobalContext();

  useEffect(() => {
    setCurrentPageTitle('AI Analysis Page');
  }, [setCurrentPageTitle]);

  const [formData, setFormData] = useState({
    Amount: '',
    term: 'long-term',
    risk: 'high',
    frequency: 'lump sum',
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/analysis`, {
        credentials: 'include',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('API request failed');

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Unexpected error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ml-64 p-8">
      {/* ===== Main Heading ===== */}
      <h1 className="text-4xl font-bold text-gray-800 mb-10">
        Investment Analysis Dashboard
      </h1>

      {/* ===== Form Section ===== */}
      <section className="bg-white shadow p-6 rounded-lg mb-10 text-black">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Investment Strategy Generator</h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block font-medium text-gray-700 mb-1">Investment Amount (INR)</label>
            <input
              type="number"
              name="Amount"
              value={formData.Amount}
              onChange={handleChange}
              required
              className="w-full border border-gray-300 px-4 py-2 rounded focus:outline-none focus:ring focus:border-blue-400"
            />
          </div>

          <div>
            <label className="block font-medium text-gray-700 mb-1">Investment Term</label>
            <select
              name="term"
              value={formData.term}
              onChange={handleChange}
              className="w-full border border-gray-300 px-4 py-2 rounded"
            >
              <option value="short-term">Short-Term</option>
              <option value="medium-term">Medium-Term</option>
              <option value="long-term">Long-Term</option>
            </select>
          </div>

          <div>
            <label className="block font-medium text-gray-700 mb-1">Risk Tolerance</label>
            <select
              name="risk"
              value={formData.risk}
              onChange={handleChange}
              className="w-full border border-gray-300 px-4 py-2 rounded"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div>
            <label className="block font-medium text-gray-700 mb-1">Investment Frequency</label>
            <select
              name="frequency"
              value={formData.frequency}
              onChange={handleChange}
              className="w-full border border-gray-300 px-4 py-2 rounded"
            >
              <option value="lump sum">Lump Sum</option>
              <option value="monthly">Monthly</option>
              <option value="quarterly">Quarterly</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="bg-gray-700  hover:bg-blue-700 text-white px-5 py-2 rounded shadow-md transition"
          >
            {loading ? 'Analyzing...' : 'Generate Recommendation'}
          </button>
        </form>

        {error && <p className="text-red-500 mt-4">{error}</p>}
      </section>

      {/* ===== Results Section ===== */}
      {result && (
        <section className="bg-white shadow p-6 rounded-lg space-y-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Investor Profile Summary</h2>
            <ul className="list-disc pl-6 text-gray-700">
              <li>Amount: {result.investorProfileSummary.InvestableAmount}</li>
              <li>Frequency: {result.investorProfileSummary.InvestmentFrequency}</li>
              <li>Risk Tolerance: {result.investorProfileSummary.RiskTolerance}</li>
              <li>Time Horizon: {result.investorProfileSummary.TimeHorizon}</li>
            </ul>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Recommendation Strategy</h2>
            <p className="text-gray-700 mb-2">{result.recommendationStrategy.description}</p>
            <p className="font-semibold text-gray-700">Focus Areas:</p>
            <ul className="list-disc pl-6 text-gray-700">
              {result.recommendationStrategy.focus.map((f, i) => (
                <li key={i}>{f}</li>
              ))}
            </ul>
            <p className="mt-2 text-gray-700">{result.recommendationStrategy.suitability}</p>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Portfolio Allocation</h2>
            <p className="text-gray-700"><strong>Suggestion:</strong> {result.portfolioAllocationNotes.suggestion}</p>
            <p className="text-gray-700 mt-1"><strong>Monitoring:</strong> {result.portfolioAllocationNotes.monitoring}</p>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Suggested Portfolio</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {result.suggestedPortfolio.map((stock, i) => (
                <Link key={i} href={`/stocks/${stock.assetIdentifier}`} passHref>
                  <div className="p-4 border rounded bg-gray-50 shadow hover:shadow-xl transition-all duration-300">
                    <h3 className="font-bold text-lg text-blue-800">{stock.assetName} ({stock.assetIdentifier})</h3>
                    <p className="text-sm text-gray-700 mb-1"><strong>Sector:</strong> {stock.assetClassOrSector}</p>
                    <p className="text-sm text-gray-700 mb-1"><strong>Risk:</strong> {stock.riskCategory}</p>
                    <p className="text-sm text-gray-700 mb-1"><strong>Action:</strong> {stock.suggestedAction}</p>
                    <p className="text-sm text-gray-600"><strong>Rationale:</strong> {stock.rationale}</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>

          <div className="text-xs text-gray-500 border-t pt-4">
            <strong>Disclaimer:</strong> {result.disclaimer}
          </div>
        </section>
      )}
    </div>
  );
}