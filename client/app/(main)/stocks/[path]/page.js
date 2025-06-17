'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import React from 'react';
import { useGlobalContext } from '@/context/GlobalContext';

export default function StockPage({ params: paramsPromise }) {
  const router = useRouter();
  const params = React.use(paramsPromise);

  const [company, setCompany] = useState(decodeURIComponent(params.path || ''));
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [rawFilter, setRawFilter] = useState('');
  const [technicalFilter, setTechnicalFilter] = useState('');
  const [fundamentalFilter, setFundamentalFilter] = useState('');
  const { setCurrentPageTitle } = useGlobalContext();
  
    useEffect(() => {
      setCurrentPageTitle('AI Stock Prediction');
    }, [setCurrentPageTitle]);
  

  const fetchStock = async (companyName) => {
    if (!companyName.trim()) {
      setError('Please enter a valid company name.');
      setLoading(false);
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);
    try {
      console.log(`Fetching stock from: ${process.env.NEXT_PUBLIC_API_URL}/predict`);
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/predict`, {
        credentials: 'include',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company: companyName }),
      });

      if (!res.ok) throw new Error('Error fetching stock');

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError('Failed to fetch stock info.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (params?.path) fetchStock(decodeURIComponent(params.path));
  }, [params?.path]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (company.trim()) {
      router.push(`/stocks/${encodeURIComponent(company)}`);
    } else {
      setError('Please enter a company name.');
    }
  };

  // Helper function to safely format numbers
  const formatNumber = (value, decimals = 2, defaultValue = 'N/A') => {
    return typeof value === 'number' && !isNaN(value) ? value.toFixed(decimals) : defaultValue;
  };

  // Helper function to format percentages
  const formatPercentage = (value, decimals = 1, defaultValue = 'N/A') => {
    return typeof value === 'number' && !isNaN(value) ? `${(value * 100).toFixed(decimals)}%` : defaultValue;
  };

  // Helper function to format large numbers
  const formatLargeNumber = (value, currencySymbol, defaultValue = 'N/A') => {
    if (typeof value !== 'number' || isNaN(value)) return defaultValue;
    if (value >= 1e9) return `${currencySymbol}${(value / 1e9).toFixed(2)}B`;
    if (value >= 1e6) return `${currencySymbol}${(value / 1e6).toFixed(2)}M`;
    return `${currencySymbol}${value.toFixed(2)}`;
  };

  // Dynamic currency symbol
  const currencySymbol = result?.result?.CurrencySymbol || '₹';

  // Helper function to get verdict badge color
  const getVerdictBadgeColor = (verdict) => {
    if (!verdict) return 'bg-gray-200 text-gray-800';
    if (verdict.toLowerCase().includes('buy')) return 'bg-green-100 text-green-800';
    if (verdict.toLowerCase().includes('sell')) return 'bg-red-100 text-red-800';
    if (verdict.toLowerCase().includes('hold') || verdict.toLowerCase().includes('skip')) return 'bg-yellow-100 text-yellow-800';
    return 'bg-gray-200 text-gray-800';
  };

  // Sorting function for tables
  const sortData = (data, key, direction) => {
    return [...data].sort((a, b) => {
      let aValue = a[key] || '';
      let bValue = b[key] || '';
      if (key === 'Value') {
        // Handle currency, percentages, and numbers
        aValue = aValue.replace(currencySymbol, '').replace('%', '');
        bValue = bValue.replace(currencySymbol, '').replace('%', '');
        aValue = aValue.includes('B') ? parseFloat(aValue) * 1e9 : aValue.includes('M') ? parseFloat(aValue) * 1e6 : parseFloat(aValue) || 0;
        bValue = bValue.includes('B') ? parseFloat(bValue) * 1e9 : bValue.includes('M') ? parseFloat(bValue) * 1e6 : parseFloat(bValue) || 0;
      } else if (typeof aValue === 'string') {
        return direction === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
      }
      return direction === 'asc' ? aValue - bValue : bValue - aValue;
    });
  };

  const handleSort = (key) => {
    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc',
    }));
  };

  // Filter data based on search input
  const filterData = (data, filterText) => {
    return data.filter(item =>
      Object.values(item).some(value =>
        value && value.toString().toLowerCase().includes(filterText.toLowerCase())
      )
    );
  };

  // Prepare raw data for table
  const rawData = result?.raw_data?.stock_data
    ? [
        { Metric: 'Market Cap', Value: formatLargeNumber(result.raw_data.stock_data.market_cap, currencySymbol) },
        { Metric: 'Revenue', Value: formatLargeNumber(result.raw_data.stock_data.revenue, currencySymbol) },
        { Metric: 'P/E Ratio', Value: formatNumber(result.raw_data.stock_data.pe_ratio) },
        { Metric: 'EPS', Value: `${currencySymbol}${formatNumber(result.raw_data.stock_data.eps)}` },
        { Metric: 'Dividend Yield', Value: `${formatNumber(result.raw_data.stock_data.div_yield)}%` },
        { Metric: 'Revenue Growth', Value: formatPercentage(result.raw_data.stock_data.revenue_growth) },
        { Metric: 'Debt-to-Equity', Value: formatNumber(result.raw_data.stock_data.de_ratio, 3) },
        { Metric: 'ROE', Value: formatPercentage(result.raw_data.stock_data.roe, 2) },
      ]
    : [];

  // Prepare technical data for table
  const technicalData = result?.raw_data?.technical_analysis
    ? [
        { Metric: 'Current Price', Value: `${currencySymbol}${formatNumber(result.raw_data.technical_analysis.current_price)}` },
        { Metric: 'RSI', Value: formatNumber(result.raw_data.technical_analysis.rsi, 1) },
        { Metric: 'MACD', Value: formatNumber(result.raw_data.technical_analysis.macd) },
        { Metric: 'Momentum', Value: formatNumber(result.raw_data.technical_analysis.momentum) },
        { Metric: '5-Day SMA', Value: `${currencySymbol}${formatNumber(result.raw_data.technical_analysis.sma_5)}` },
        { Metric: '10-Day SMA', Value: `${currencySymbol}${formatNumber(result.raw_data.technical_analysis.sma_10)}` },
        { Metric: 'Volatility', Value: formatNumber(result.raw_data.technical_analysis.volatility) },
        { Metric: 'Price Trend', Value: formatNumber(result.raw_data.technical_analysis.price_trend) },
        { Metric: 'Signal', Value: formatNumber(result.raw_data.technical_analysis.signal) },
        { Metric: 'Volume Trend', Value: result.raw_data.technical_analysis.volume_trend || 'N/A' },
      ]
    : [];

  // Prepare fundamental data for table
  const fundamentalData = result?.raw_data?.stock_data
    ? [
        { Metric: 'P/E Ratio', Value: formatNumber(result.raw_data.stock_data.pe_ratio), Description: result?.result?.fundamental_overview?.valuation || 'No valuation available' },
        { Metric: 'EPS', Value: `${currencySymbol}${formatNumber(result.raw_data.stock_data.eps)}`, Description: result?.result?.fundamental_overview?.summary || 'No summary available' },
        { Metric: 'Dividend Yield', Value: `${formatNumber(result.raw_data.stock_data.div_yield)}%`, Description: result?.result?.fundamental_overview?.dividends || 'No dividend data available' },
        { Metric: 'Revenue Growth', Value: formatPercentage(result.raw_data.stock_data.revenue_growth), Description: result?.result?.fundamental_overview?.growth || 'No growth data available' },
        { Metric: 'Debt-to-Equity Ratio', Value: formatNumber(result.raw_data.stock_data.de_ratio, 3), Description: result?.result?.fundamental_overview?.leverage || 'No leverage data available' },
        { Metric: 'ROE', Value: formatPercentage(result.raw_data.stock_data.roe, 2), Description: result?.result?.fundamental_overview?.roe_analysis || 'No ROE analysis available' },
      ]
    : [];

  const sortedRawData = sortConfig.key ? sortData(rawData, sortConfig.key, sortConfig.direction) : rawData;
  const sortedTechnicalData = sortConfig.key ? sortData(technicalData, sortConfig.key, sortConfig.direction) : technicalData;
  const sortedFundamentalData = sortConfig.key ? sortData(fundamentalData, sortConfig.key, sortConfig.direction) : fundamentalData;
  const filteredRawData = filterData(sortedRawData, rawFilter);
  const filteredTechnicalData = filterData(sortedTechnicalData, technicalFilter);
  const filteredFundamentalData = filterData(sortedFundamentalData, fundamentalFilter);

  return (
    <div className="ml-64 p-8 bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
      {/* Search Form Section */}
      <section className="bg-white shadow-xl p-6 rounded-2xl mb-10 border border-gray-200 transition-all duration-300 hover:shadow-2xl">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Search Stock</h2>
        <form onSubmit={handleSearch} className="flex gap-3 items-center">
          <input
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            placeholder="Search another company..."
            className="flex-1 border border-gray-300 p-3 rounded-lg text-gray-700 focus:ring-2 focus:ring-gray-400 focus:outline-none transition duration-200"
          />
          <button
            type="submit"
            className="bg-gray-800 text-white px-6 py-3 rounded-lg hover:bg-gray-900 focus:ring-2 focus:ring-gray-400 focus:outline-none transition duration-200"
            disabled={loading}
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>
      </section>

      {/* Stock Analysis Header */}
      {result && (
        <section className="bg-white shadow-xl p-6 rounded-2xl mb-10 border border-gray-200 transition-all duration-300 hover:shadow-2xl">
          <h2 className="text-2xl font-bold text-gray-800">
            Stock Analysis for: {result?.raw_data?.stock_data?.company_name || decodeURIComponent(params.path || 'Unknown')}
          </h2>
        </section>
      )}

      {loading && <p className="text-center text-gray-600 text-lg animate-pulse">Loading...</p>}
      {error && <p className="text-center text-red-500 text-lg">{error}</p>}

      {result && !loading && !error && (
        <div className="space-y-8">
          {/* Investment Verdict */}
          <section className="bg-white shadow-xl p-6 rounded-2xl text-center border border-gray-200 transition-all duration-300 hover:shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Investment Verdict</h3>
            <span
              className={`inline-block px-4 py-2 rounded-full text-xl font-semibold ${getVerdictBadgeColor(result?.result?.investment_outlook?.verdict)} transition duration-200`}
            >
              {result?.result?.investment_outlook?.verdict || 'No verdict available'}
            </span>
          </section>

          {/* Raw Data Table */}
          <section className="bg-white shadow-xl p-6 rounded-2xl border border-gray-200 transition-all duration-300 hover:shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Raw Stock Data</h3>
            <input
              type="text"
              placeholder="Filter raw data..."
              value={rawFilter}
              onChange={(e) => setRawFilter(e.target.value)}
              className="mb-4 w-full border border-gray-300 p-3 rounded-lg text-gray-700 focus:ring-2 focus:ring-gray-400 focus:outline-none transition duration-200"
            />
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm text-left">
                <thead className="bg-gray-100 text-gray-700 font-semibold">
                  <tr>
                    <th className="p-3 cursor-pointer" onClick={() => handleSort('Metric')}>
                      Metric {sortConfig.key === 'Metric' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                    </th>
                    <th className="p-3 cursor-pointer" onClick={() => handleSort('Value')}>
                      Value {sortConfig.key === 'Value' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredRawData.length > 0 ? (
                    filteredRawData.map((entry, index) => (
                      <tr key={index} className="border-t text-gray-700 hover:bg-gray-50 transition duration-200">
                        <td className="p-3">{entry.Metric}</td>
                        <td className="p-3">{entry.Value}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="2" className="p-3 text-center text-gray-600">No data available</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          {/* Technical Data Table */}
          <section className="bg-white shadow-xl p-6 rounded-2xl border border-gray-200 transition-all duration-300 hover:shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Technical Analysis Data</h3>
            <input
              type="text"
              placeholder="Filter technical data..."
              value={technicalFilter}
              onChange={(e) => setTechnicalFilter(e.target.value)}
              className="mb-4 w-full border border-gray-300 p-3 rounded-lg text-gray-700 focus:ring-2 focus:ring-gray-400 focus:outline-none transition duration-200"
            />
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm text-left">
                <thead className="bg-gray-100 text-gray-700 font-semibold">
                  <tr>
                    <th className="p-3 cursor-pointer" onClick={() => handleSort('Metric')}>
                      Metric {sortConfig.key === 'Metric' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                    </th>
                    <th className="p-3 cursor-pointer" onClick={() => handleSort('Value')}>
                      Value {sortConfig.key === 'Value' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTechnicalData.length > 0 ? (
                    filteredTechnicalData.map((entry, index) => (
                      <tr key={index} className="border-t text-gray-700 hover:bg-gray-50 transition duration-200">
                        <td className="p-3">{entry.Metric}</td>
                        <td className="p-3">{entry.Value}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="2" className="p-3 text-center text-gray-600">No data available</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            <div className="mt-4 space-y-2 bg-gray-50 p-4 rounded-lg">
              <p className="text-gray-600">
                <strong>Summary:</strong> {result?.result?.technical_overview?.summary || 'No summary available'}
              </p>
              <p className="text-gray-600">
                <strong>RSI Analysis:</strong> {result?.result?.technical_overview?.rsi_analysis || 'No RSI analysis available'}
              </p>
              <p className="text-gray-600">
                <strong>MACD Analysis:</strong> {result?.result?.technical_overview?.macd_analysis || 'No MACD analysis available'}
              </p>
              <p className="text-gray-600">
                <strong>Momentum Analysis:</strong> {result?.result?.technical_overview?.momentum_analysis || 'No momentum analysis available'}
              </p>
              <p className="text-gray-600">
                <strong>SMA Analysis:</strong> {result?.result?.technical_overview?.sma_analysis || 'No SMA analysis available'}
              </p>
              <p className="text-gray-600">
                <strong>Price/Volume Trend:</strong> {result?.result?.technical_overview?.price_volume_trend || 'No price/volume trend available'}
              </p>
              <p className="text-gray-600">
                <strong>Volatility Analysis:</strong> {result?.result?.technical_overview?.volatility_analysis || 'No volatility analysis available'}
              </p>
              <p className="text-sm text-gray-500">
                Verdict: <span className={`inline-block px-2 py-1 rounded-full ${getVerdictBadgeColor(result?.raw_data?.technical_analysis?.verdict)}`}>{result?.raw_data?.technical_analysis?.verdict || 'N/A'}</span>
              </p>
            </div>
          </section>

          {/* Fundamental Analysis Table */}
          <section className="bg-white shadow-xl p-6 rounded-2xl border border-gray-200 transition-all duration-300 hover:shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Fundamental Analysis</h3>
            <input
              type="text"
              placeholder="Filter fundamental data..."
              value={fundamentalFilter}
              onChange={(e) => setFundamentalFilter(e.target.value)}
              className="mb-4 w-full border border-gray-300 p-3 rounded-lg text-gray-700 focus:ring-2 focus:ring-gray-400 focus:outline-none transition duration-200"
            />
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm text-left">
                <thead className="bg-gray-100 text-gray-700 font-semibold">
                  <tr>
                    <th className="p-3 cursor-pointer w-1/4" onClick={() => handleSort('Metric')}>
                      Metric {sortConfig.key === 'Metric' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                    </th>
                    <th className="p-3 cursor-pointer w-1/4" onClick={() => handleSort('Value')}>
                      Value {sortConfig.key === 'Value' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                    </th>
                    <th className="p-3 w-1/2">Description</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredFundamentalData.length > 0 ? (
                    filteredFundamentalData.map((entry, index) => (
                      <tr key={index} className="border-t text-gray-700 hover:bg-gray-50 transition duration-200">
                        <td className="p-3">{entry.Metric}</td>
                        <td className="p-3">{entry.Value}</td>
                        <td className="p-3">{entry.Description}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="3" className="p-3 text-center text-gray-600">No data available</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            <div className="mt-4 space-y-2 bg-gray-50 p-4 rounded-lg">
              <p className="text-gray-600">
                <strong>Summary:</strong> {result?.result?.fundamental_overview?.summary || 'No summary available'}
              </p>
              <p className="text-sm text-gray-500">
                Verdict: <span className={`inline-block px-2 py-1 rounded-full ${getVerdictBadgeColor(result?.raw_data?.fundamental_analysis?.verdict)}`}>{result?.raw_data?.fundamental_analysis?.verdict || 'N/A'}</span>
              </p>
            </div>
          </section>

          {/* Investment Outlook */}
          <section className="bg-white shadow-xl p-6 rounded-2xl border border-gray-200 transition-all duration-300 hover:shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Investment Outlook</h3>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-gray-700">
                <strong>Short-Term:</strong> {result?.result?.investment_outlook?.short_term || 'N/A'}
              </p>
              <p className="text-gray-700">
                <strong>Long-Term:</strong> {result?.result?.investment_outlook?.long_term || 'N/A'}
              </p>
              <p className="text-gray-700">
                <strong>Rationale:</strong> {result?.result?.investment_outlook?.rationale || 'No rationale provided'}
              </p>
            </div>
          </section>

          {/* Sentiment Analysis */}
          <section className="bg-white shadow-xl p-6 rounded-2xl border border-gray-200 transition-all duration-300 hover:shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Sentiment Analysis</h3>
            <p className="mb-4 text-gray-600">
              {result?.result?.sentiment_analysis?.summary || 'No sentiment summary available'}
            </p>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-green-600">Positive News</h4>
                <ul className="list-disc pl-5 text-sm text-gray-600">
                  {result?.result?.sentiment_analysis?.positive_news?.length > 0 ? (
                    result.result.sentiment_analysis.positive_news.map((news, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-green-600 mr-2">✔</span> {news}
                      </li>
                    ))
                  ) : (
                    <li>No positive news available</li>
                  )}
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-yellow-600">Neutral News</h4>
                <ul className="list-disc pl-5 text-sm text-gray-600">
                  {result?.result?.sentiment_analysis?.neutral_news?.length > 0 ? (
                    result.result.sentiment_analysis.neutral_news.map((news, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-yellow-600 mr-2">•</span> {news}
                      </li>
                    ))
                  ) : (
                    <li>No neutral news available</li>
                  )}
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-red-600">Negative News</h4>
                <ul className="list-disc pl-5 text-sm text-gray-600">
                  {result?.result?.sentiment_analysis?.negative_news?.length > 0 ? (
                    result.result.sentiment_analysis.negative_news.map((news, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-red-600 mr-2">✖</span> {news}
                      </li>
                    ))
                  ) : (
                    <li>No negative news available</li>
                  )}
                </ul>
              </div>
            </div>
          </section>

          {/* Suggestions */}
          <section className="bg-white shadow-xl p-6 rounded-2xl border border-gray-200 transition-all duration-300 hover:shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Suggestions</h3>
            <div className="bg-gray-50 border-l-4 border-gray-800 p-4 rounded-lg">
              <p className="text-gray-700 font-semibold">
                <strong>Entry Points:</strong> {result?.result?.Suggestions?.entry_points || 'N/A'}
              </p>
              <p className="text-gray-700 font-semibold">
                <strong>Exit Points:</strong> {result?.result?.Suggestions?.exit_points || 'N/A'}
              </p>
              <p className="text-gray-700">
                <strong>Risk Management:</strong> {result?.result?.Suggestions?.risk_management || 'N/A'}
              </p>
              <p className="text-gray-700">
                <strong>Monitoring:</strong> {result?.result?.Suggestions?.monitoring || 'N/A'}
              </p>
              <p className="text-gray-700">
                <strong>Diversification:</strong> {result?.result?.Suggestions?.diversification || 'N/A'}
              </p>
              <p className="text-gray-700">
                <strong>Missing Data:</strong> {result?.result?.Suggestions?.missing_data || 'No missing data noted'}
              </p>
            </div>
          </section>

          {/* Stock Price History */}
          <section className="bg-white shadow-xl p-6 rounded-2xl border border-gray-200 transition-all duration-300 hover:shadow-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Recent Stock Price History</h3>
            {result?.raw_data?.stock_data?.history?.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full text-sm text-left">
                  <thead className="bg-gray-100 text-gray-700 font-semibold">
                    <tr>
                      <th className="p-3 cursor-pointer" onClick={() => handleSort('Date')}>
                        Date {sortConfig.key === 'Date' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                      </th>
                      <th className="p-3 cursor-pointer" onClick={() => handleSort('Close')}>
                        Close {sortConfig.key === 'Close' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                      </th>
                      <th className="p-3 cursor-pointer" onClick={() => handleSort('High')}>
                        High {sortConfig.key === 'High' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                      </th>
                      <th className="p-3 cursor-pointer" onClick={() => handleSort('Low')}>
                        Low {sortConfig.key === 'Low' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                      </th>
                      <th className="p-3 cursor-pointer" onClick={() => handleSort('Volume')}>
                        Volume {sortConfig.key === 'Volume' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {sortData(result.raw_data.stock_data.history.slice(0, 5), sortConfig.key, sortConfig.direction).map((entry, index) => (
                      <tr key={index} className="border-t text-gray-700 hover:bg-gray-50 transition duration-200">
                        <td className="p-3">
                          {entry?.Date ? new Date(entry.Date).toLocaleDateString() : 'N/A'}
                        </td>
                        <td className="p-3">{currencySymbol}{formatNumber(entry?.Close)}</td>
                        <td className="p-3">{currencySymbol}{formatNumber(entry?.High)}</td>
                        <td className="p-3">{currencySymbol}{formatNumber(entry?.Low)}</td>
                        <td className="p-3">
                          {typeof entry?.Volume === 'number' ? entry.Volume.toLocaleString() : 'N/A'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-600">No stock price history available</p>
            )}
          </section>
        </div>
      )}
    </div>
  );
}