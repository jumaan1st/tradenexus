'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useGlobalContext } from '@/context/GlobalContext';

export default function MarketTrends() {
  const [usMarketData, setUsMarketData] = useState({ gainers: [], losers: [] });
  const [indianMarketData, setIndianMarketData] = useState({
    mostActiveNSE: [],
    mostActiveBSE: [],
    gainersNifty: [],
    gainersSensex: [],
    losersNifty: [],
    losersSensex: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [mostActiveIndex, setMostActiveIndex] = useState('NSE');
  const [gainersIndex, setGainersIndex] = useState('Nifty');
  const [losersIndex, setLosersIndex] = useState('Nifty');
  const { setCurrentPageTitle } = useGlobalContext();

  useEffect(() => {
    setCurrentPageTitle('Current Trends');
  }, [setCurrentPageTitle]);

  // Fetch US and Indian market data
  useEffect(() => {
    const fetchMarketData = async () => {
      setLoading(true);
      setError('');

      try {
        // Fetch US market data
        const usRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/market-data-us`, {
          method: 'GET',
          credentials: 'include',
        });
        if (!usRes.ok) throw new Error('Failed to fetch US market data');
        const usData = await usRes.json();
        setUsMarketData({ gainers: usData[0], losers: usData[1] });

        // Fetch Indian market data
        const inRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/market-data-in`, {
          method: 'GET',
          credentials: 'include',
        });
        if (!inRes.ok) throw new Error('Failed to fetch Indian market data');
        const inData = await inRes.json();
        setIndianMarketData({
          mostActiveNSE: inData[0],
          mostActiveBSE: inData[1],
          gainersNifty: inData[2],
          gainersSensex: inData[3],
          losersNifty: inData[4],
          losersSensex: inData[5],
        });
      } catch (err) {
        setError(err.message || 'Unexpected error fetching market data');
      } finally {
        setLoading(false);
      }
    };

    fetchMarketData();
  }, []);

  return (
    <div className="ml-64 p-8 text-black">
      {/* ===== Main Heading ===== */}
      <h1 className="text-4xl font-bold text-gray-800 mb-10">
        Market Trends Dashboard
      </h1>

      {loading && <p className="text-gray-600">Loading market data...</p>}
      {error && <p className="text-red-500 mb-4">{error}</p>}

      {!loading && !error && (
        <>
          {/* ===== Indian Market - Most Active (NSE/BSE) ===== */}
          <section className="mb-10">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold text-gray-800">
                Indian Market - Most Active
              </h2>
              <select
                className="border p-2 rounded"
                value={mostActiveIndex}
                onChange={(e) => setMostActiveIndex(e.target.value)}
              >
                <option value="NSE">NSE</option>
                <option value="BSE">BSE</option>
              </select>
            </div>
            <div className="bg-white shadow p-6 rounded-lg">
              <div className="overflow-x-auto">
                <table className="min-w-full text-sm text-left">
                  <thead className="bg-gray-100 text-gray-700 font-semibold">
                    <tr>
                      <th className="p-3">Company</th>
                      <th className="p-3">Price (₹)</th>
                      <th className="p-3">Change (₹)</th>
                      <th className="p-3">Value (₹ Cr.)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(mostActiveIndex === 'NSE'
                      ? indianMarketData.mostActiveNSE
                      : indianMarketData.mostActiveBSE
                    ).map((stock, index) => (
                      <tr key={index} className="border-t hover:bg-gray-100">
                        <td className="p-3 font-medium">
                          <Link href={`/stocks/${stock.Company}`} className="text-blue-800 hover:underline">
                            {stock.Company}
                          </Link>
                        </td>
                        <td className="p-3">₹{stock.Price.toFixed(2)}</td>
                        <td className="p-3" style={{ color: stock.Change >= 0 ? '#16a34a' : '#ef4444' }}>
                          {stock.Change >= 0 ? '+' : ''}{stock.Change.toFixed(2)}
                        </td>
                        <td className="p-3">₹{stock["Value  (Rs Cr.)"].toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </section>

          {/* ===== Indian Market - Top Gainers (Nifty/Sensex) ===== */}
          <section className="mb-10">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold text-gray-800">
                Indian Market - Top Gainers
              </h2>
              <select
                className="border p-2 rounded"
                value={gainersIndex}
                onChange={(e) => setGainersIndex(e.target.value)}
              >
                <option value="Nifty">Nifty</option>
                <option value="Sensex">Sensex</option>
              </select>
            </div>
            <div className="bg-white shadow p-6 rounded-lg">
              <div className="overflow-x-auto">
                <table className="min-w-full text-sm text-left">
                  <thead className="bg-gray-100 text-gray-700 font-semibold">
                    <tr>
                      <th className="p-3">Company</th>
                      <th className="p-3">Price (₹)</th>
                      <th className="p-3">Change (₹)</th>
                      <th className="p-3">Gain (%)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(gainersIndex === 'Nifty'
                      ? indianMarketData.gainersNifty
                      : indianMarketData.gainersSensex
                    ).map((stock, index) => (
                      <tr key={index} className="border-t hover:bg-gray-100">
                        <td className="p-3 font-medium">
                          <Link href={`/stocks/${stock.Company}`} className="text-blue-800 hover:underline">
                            {stock.Company}
                          </Link>
                        </td>
                        <td className="p-3">₹{stock.Price.toFixed(2)}</td>
                        <td className="p-3 text-green-600">
                          {stock.Change >= 0 ? '+' : ''}{stock.Change.toFixed(2)}
                        </td>
                        <td className="p-3 text-green-600">
                          {stock["%Gain"] >= 0 ? '+' : ''}{stock["%Gain"].toFixed(2)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </section>

          {/* ===== Indian Market - Top Losers (Nifty/Sensex) ===== */}
          <section className="mb-10">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold text-gray-800">
                Indian Market - Top Losers
              </h2>
              <select
                className="border p-2 rounded"
                value={losersIndex}
                onChange={(e) => setLosersIndex(e.target.value)}
              >
                <option value="Nifty">Nifty</option>
                <option value="Sensex">Sensex</option>
              </select>
            </div>
            <div className="bg-white shadow p-6 rounded-lg">
              <div className="overflow-x-auto">
                <table className="min-w-full text-sm text-left">
                  <thead className="bg-gray-100 text-gray-700 font-semibold">
                    <tr>
                      <th className="p-3">Company</th>
                      <th className="p-3">Price (₹)</th>
                      <th className="p-3">Change (₹)</th>
                      <th className="p-3">Loss (%)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(losersIndex === 'Nifty'
                      ? indianMarketData.losersNifty
                      : indianMarketData.losersSensex
                    ).map((stock, index) => (
                      <tr key={index} className="border-t hover:bg-gray-100">
                        <td className="p-3 font-medium">
                          <Link href={`/stocks/${stock.Company}`} className="text-blue-800 hover:underline">
                            {stock.Company}
                          </Link>
                        </td>
                        <td className="p-3">₹{stock.Price.toFixed(2)}</td>
                        <td className="p-3 text-red-500">{stock.Change.toFixed(2)}</td>
                        <td className="p-3 text-red-500">{stock["%Loss"].toFixed(2)}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </section>

          {/* ===== US Market Section ===== */}
          <section className="mb-10">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              US Market - Top Gainers
            </h2>
            <div className="bg-white shadow p-6 rounded-lg">
              <div className="overflow-x-auto">
                <table className="min-w-full text-sm text-left">
                  <thead className="bg-gray-100 text-gray-700 font-semibold">
                    <tr>
                      <th className="p-3">Name</th>
                      <th className="p-3">Ticker</th>
                      <th className="p-3">Price ($)</th>
                      <th className="p-3">Change ($)</th>
                      <th className="p-3">Change (%)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {usMarketData.gainers.map((stock, index) => (
                      <tr key={index} className="border-t hover:bg-gray-100">
                        <td className="p-3 font-medium">
                          <Link href={`/stocks/${stock.Name}`} className="text-blue-800 hover:underline">
                            {stock["Unnamed: 1"]}
                          </Link>
                        </td>
                        <td className="p-3">{stock.Name}</td>
                        <td className="p-3">${stock.Price.toFixed(2)}</td>
                        <td className="p-3 text-green-600">
                          {stock.Change >= 0 ? '+' : ''}{stock.Change.toFixed(2)}
                        </td>
                        <td className="p-3 text-green-600">
                          {stock["Change%"] >= 0 ? '+' : ''}{stock["Change%"].toFixed(2)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </section>

          <section className="mb-10">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              US Market - Top Losers
            </h2>
            <div className="bg-white shadow p-6 rounded-lg">
              <div className="overflow-x-auto">
                <table className="min-w-full text-sm text-left">
                  <thead className="bg-gray-100 text-gray-700 font-semibold">
                    <tr>
                      <th className="p-3">Name</th>
                      <th className="p-3">Ticker</th>
                      <th className="p-3">Price ($)</th>
                      <th className="p-3">Change ($)</th>
                      <th className="p-3">Change (%)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {usMarketData.losers.map((stock, index) => (
                      <tr key={index} className="border-t hover:bg-gray-100">
                        <td className="p-3 font-medium">
                          <Link href={`/stocks/${stock.Name}`} className="text-blue-800 hover:underline">
                            {stock["Unnamed: 1"]}
                          </Link>
                        </td>
                        <td className="p-3">{stock.Name}</td>
                        <td className="p-3">${stock.Price.toFixed(2)}</td>
                        <td className="p-3 text-red-500">{stock.Change.toFixed(2)}</td>
                        <td className="p-3 text-red-500">{stock["Change%"].toFixed(2)}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        </>
      )}
    </div>
  );
}