'use client';
import { useEffect, useState } from 'react';
import {
  ResponsiveContainer,
  BarChart,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Bar,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import Link from 'next/link';
import AddStock from '@/components/AddStock';
import { useGlobalContext } from '@/context/GlobalContext';

export default function PortfolioPage() {
  const [stocks, setStocks] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState('');
  const [editingStock, setEditingStock] = useState(null);
  const [newQuantity, setNewQuantity] = useState('');
  const [newPurchasePrice, setNewPurchasePrice] = useState('');
   const { setCurrentPageTitle } = useGlobalContext();

  useEffect(() => {
    setCurrentPageTitle('Portfolio Dashboard Page');
  }, [setCurrentPageTitle]);

  // Calculate portfolio metrics
  const portfolioMetrics = stocks.reduce(
    (acc, stock) => {
      const invested = stock.quantity * stock.purchasePrice;
      const current = stock.quantity * stock.currentPrice;
      return {
        totalInvested: acc.totalInvested + invested,
        totalCurrentValue: acc.totalCurrentValue + current,
      };
    },
    { totalInvested: 0, totalCurrentValue: 0 }
  );

  const portfolioPerformance = portfolioMetrics.totalInvested
    ? ((portfolioMetrics.totalCurrentValue - portfolioMetrics.totalInvested) /
        portfolioMetrics.totalInvested) *
      100
    : 0;

  // Fetch stocks from API
  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/get-stocks`,
          {
            method: 'GET',
            credentials: 'include',
          }
        );

        if (!res.ok) throw new Error('Failed to fetch stocks');

        const data = await res.json();
        setStocks(data);
        if (data.length > 0) setSelectedTicker(data[0].ticker);
      } catch (error) {
        console.error('Error fetching stocks:', error);
      }
    };

    fetchStocks();
  }, []);

  const getProfitPercent = (stock) => {
    const value = stock.quantity * stock.purchasePrice;
    const currentValue = stock.quantity * stock.currentPrice;
    return ((currentValue - value) / value) * 100;
  };

  const getChangeColor = (change) => {
    return change < 0
      ? 'text-red-500'
      : change > 5
      ? 'text-green-600'
      : 'text-gray-500';
  };

  const handleEditStock = (stock) => {
    setEditingStock(stock);
    setNewQuantity(stock.quantity);
    setNewPurchasePrice(stock.purchasePrice);
  };

  const handleUpdateStock = async () => {
    if (!confirm(`Are you sure you want to update ${editingStock.name}?`)) {
      return;
    }

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/edit-stock/${editingStock.id}`,
        {
          method: 'PUT',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            quantity: newQuantity,
            purchasePrice: newPurchasePrice,
          }),
        }
      );

      if (!res.ok) throw new Error('Failed to update stock');

      const updatedStocks = stocks.map((stock) =>
        stock.id === editingStock.id
          ? {
              ...stock,
              quantity: parseInt(newQuantity),
              purchasePrice: parseFloat(newPurchasePrice),
            }
          : stock
      );
      setStocks(updatedStocks);
      setEditingStock(null);
      setNewQuantity('');
      setNewPurchasePrice('');
      alert('Stock updated successfully');
    } catch (error) {
      console.error('Error updating stock:', error);
      alert('Failed to update stock');
    }
  };

  const handleDeleteStock = async (stockId, stockName) => {
    if (!confirm(`Are you sure you want to delete ${stockName}? This action cannot be undone.`)) {
      return;
    }

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/delete-stock/${stockId}`,
        {
          method: 'DELETE',
          credentials: 'include',
        }
      );

      if (!res.ok) throw new Error('Failed to delete stock');

      setStocks(stocks.filter((stock) => stock.id !== stockId));
      alert('Stock deleted successfully');
    } catch (error) {
      console.error('Error deleting stock:', error);
      alert('Failed to delete stock');
    }
  };

  return (
    <div className="ml-64 p-8">
     

      {/* ===== Add Stock Form ===== */}
      <AddStock setStocks={setStocks} />

 {/* ===== Portfolio Summary Card ===== */}
      <section className="bg-white shadow p-6 rounded-lg mb-10">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Portfolio Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg transform hover:scale-105 transition-transform duration-200">
            <p className="text-sm text-gray-500">Total Invested</p>
            <p className="text-xl font-semibold text-black">
              ₹{portfolioMetrics.totalInvested.toLocaleString()}
            </p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg transform hover:scale-105 transition-transform duration-200">
            <p className="text-sm text-gray-500">Current Value</p>
            <p className="text-xl font-semibold text-black">
              ₹{portfolioMetrics.totalCurrentValue.toLocaleString()}
            </p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg transform hover:scale-105 transition-transform duration-200">
            <p className="text-sm text-gray-500">Overall Performance</p>
            <p
              className={`text-xl font-semibold ${getChangeColor(portfolioPerformance)} animate-pulse`}
            >
              {portfolioPerformance.toFixed(2)}%
            </p>
          </div>
        </div>
      </section>
      {/* ===== Edit Stock Modal ===== */}
      {editingStock && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 text-black">
          <div className="bg-white p-6 rounded-lg shadow-xl">
            <h2 className="text-xl font-bold mb-4">Edit Stock: {editingStock.name}</h2>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700">Quantity</label>
              <input
                type="number"
                value={newQuantity}
                onChange={(e) => setNewQuantity(e.target.value)}
                className="mt-1 p-2 border rounded w-full"
                min="1"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700">Purchase Price</label>
              <input
                type="number"
                value={newPurchasePrice}
                onChange={(e) => setNewPurchasePrice(e.target.value)}
                className="mt-1 p-2 border rounded w-full"
                step="0.01"
                min="0"
              />
            </div>
            <div className="flex justify-end gap-4">
              <button
                onClick={() => setEditingStock(null)}
                className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
              <button
                onClick={handleUpdateStock}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ===== Table Section ===== */}
      <section className="bg-white shadow p-6 rounded-lg mb-10">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Your Stocks</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm text-left">
            <thead className="bg-gray-100 text-gray-700 font-semibold">
              <tr>
                <th className="p-3">Name</th>
                <th className="p-3">Ticker</th>
                <th className="p-3">Quantity</th>
                <th className="p-3">Buy Price</th>
                <th className="p-3">Current Price</th>
                <th className="p-3">Invested</th>
                <th className="p-3">Current Value</th>
                <th className="p-3">Change</th>
                <th className="p-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {stocks.map((stock) => {
                const value = stock.quantity * stock.purchasePrice;
                const currentValue = stock.quantity * stock.currentPrice;
                const change = getProfitPercent(stock);
                const changeColor = getChangeColor(change);
                return (
                  <tr
                    key={stock.id}
                    className="border-t text-black hover:bg-blue-50 hover:shadow-md transition-all duration-200"
                  >
                    <td className="p-3 font-medium">{stock.name}</td>
                    <td className="p-3">{stock.ticker}</td>
                    <td className="p-3">{stock.quantity}</td>
                    <td className="p-3">₹{stock.purchasePrice.toLocaleString()}</td>
                    <td className="p-3">₹{stock.currentPrice.toLocaleString()}</td>
                    <td className="p-3">₹{value.toLocaleString()}</td>
                    <td className="p-3">₹{currentValue.toLocaleString()}</td>
                    <td className={`p-3 font-semibold ${changeColor}`}>
                      {change.toFixed(2)}%
                    </td>
                    <td className="p-3">
                      <button
                        onClick={() => handleEditStock(stock)}
                        className="mr-2 px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteStock(stock.id, stock.name)}
                        className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      {/* ===== Asset Contribution Pie Chart ===== */}
      <section className="mb-10">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          Asset Distribution (Top 10)
        </h2>
        <div className="bg-white shadow p-6 rounded-lg h-96">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={
                  (() => {
                    const prepared = stocks.map((s) => ({
                      name: s.ticker,
                      value: s.quantity * s.currentPrice,
                    }));
                    const sorted = prepared.sort((a, b) => b.value - a.value);
                    const top10 = sorted.slice(0, 10);
                    const others = sorted.slice(10);
                    const otherValue = others.reduce(
                      (sum, s) => sum + s.value,
                      0
                    );
                    if (otherValue > 0) {
                      top10.push({ name: 'Other', value: otherValue });
                    }
                    return top10;
                  })()
                }
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={130}
                label
              >
                {stocks.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={
                      [
                        '#478CCF',
                        '#36C2CE',
                        '#77E4C8',
                        '#4535C1',
                        '#F19C79',
                        '#FAD02C',
                        '#ACD8AA',
                        '#D9BF77',
                        '#FF7F50',
                        '#A569BD',
                        '#BDC3C7',
                      ][index % 11]
                    }
                  />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* ===== Performance Chart with Dropdown ===== */}
      <section className="mb-10 text-black">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          Stock Performance
        </h2>

        <div className="mb-4">
          <label className="font-medium mr-2">Select Stock:</label>
          <select
            className="border p-2 rounded"
            value={selectedTicker}
            onChange={(e) => setSelectedTicker(e.target.value)}
          >
            {stocks.map((stock) => (
              <option key={stock.id} value={stock.ticker}>
                {stock.name} ({stock.ticker})
              </option>
            ))}
          </select>
        </div>

        <div className="bg-white shadow p-6 rounded-lg h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={stocks
                .filter((s) => s.ticker === selectedTicker)
                .map((s) => ({
                  ...s,
                  value: s.quantity * s.purchasePrice,
                  currentValue: s.quantity * s.currentPrice,
                }))}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ticker" />
              <YAxis tickFormatter={(value) => `₹${value.toLocaleString()}`} />
              <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
              <Legend />
              <Bar dataKey="value" fill="#478CCF" name="Invested Value" barSize={100} />
              <Bar dataKey="currentValue" fill="#36C2CE" name="Current Value" barSize={100} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* ===== Cards Section ===== */}
      <section>
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Stock Insights</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {stocks.map((stock) => {
            const value = stock.quantity * stock.purchasePrice;
            const currentValue = stock.quantity * stock.currentPrice;
            const profit = ((currentValue - value) / value) * 100;
            const borderColor =
              profit < 0
                ? 'border-red-500'
                : profit > 5
                ? 'border-green-500'
                : 'border-gray-300';
            const changeColor = getChangeColor(profit);

            return (
              <Link href={`/stocks/${stock.ticker}`} key={stock.id}>
                <div
                  className={`cursor-pointer bg-white shadow-md p-5 rounded-lg border-2 ${borderColor} hover:shadow-xl hover:bg-blue-50 transition-all duration-300`}
                >
                  <h3 className="text-xl font-semibold text-gray-900">
                    {stock.name}
                  </h3>
                  <p className="text-sm text-gray-500">
                    Ticker: {stock.ticker}
                  </p>
                  <p className="text-sm text-gray-500">
                    Quantity: {stock.quantity}
                  </p>
                  <p className="text-sm text-gray-500">
                    Buy Price: ₹{stock.purchasePrice.toLocaleString()}
                  </p>
                  <p className="text-sm text-gray-500">
                    Current Price: ₹{stock.currentPrice.toLocaleString()}
                  </p>
                  <p
                    className={`mt-2 font-semibold ${changeColor}`}
                  >
                    {profit.toFixed(2)}%
                  </p>
                </div>
              </Link>
            );
          })}
        </div>
      </section>
    </div>
  );
}