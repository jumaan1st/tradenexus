'use client';
import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

export default function AddStockModal({ setStocks, onClose }) {
  const [newStock, setNewStock] = useState({
    name: '',
    quantity: '',
    purchasePrice: '',
    currentPrice: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = (e) => {
    e.preventDefault();
    const { name, quantity, purchasePrice, currentPrice } = newStock;

    if (!name || !quantity) {
      alert('Name and Quantity are required.');
      return;
    }

    const hasPurchasePrice = purchasePrice && parseFloat(purchasePrice) > 0;
    const isCurrentPriceChecked = currentPrice === true;

    if (!hasPurchasePrice && !isCurrentPriceChecked) {
      alert('Either enter Purchase Price or check Current Price.');
      return;
    }

    const newEntry = {
      _id: Date.now().toString(),
      name,
      quantity: parseInt(quantity),
      purchasePrice: purchasePrice,
      currentPrice: currentPrice,
    };

    setIsLoading(true);

    axios
      .post(
        process.env.NEXT_PUBLIC_API_URL + '/add-stock',
        newEntry,
        {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json',
          },
        }
      )
      .then((response) => {
        console.log('Stock added successfully:', response.data);
        const result = response.data;
        const newData = {
          _id: 9999,
          name: result['stock_info']['name'],
          ticker: result['stock_info']['symbol'],
          quantity: quantity,
          purchasePrice: result['stock_info']['price'],
          currentPrice: result['stock_info']['price'],
        };
        setStocks((prevStocks) => [...prevStocks, newData]);
        setNewStock({
          name: '',
          quantity: '',
          purchasePrice: '',
          currentPrice: false,
        });
        onClose(); // Close the modal
        router.push('/portfolio'); // Redirect to portfolio
      })
      .catch((error) => {
        console.error('Error adding stock:', error);
        alert('Failed to add stock: ' + (error.response?.data?.message || error.message));
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-800">Add New Stock</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
            title="Close"
          >
            <i className="fas fa-times"></i>
          </button>
        </div>
        <form
          className="grid grid-cols-1 gap-4"
          onSubmit={(e) => handleSubmit(e)}
        >
          <input
            type="text"
            placeholder="Company Name"
            className="border p-2 rounded"
            value={newStock.name}
            onChange={(e) =>
              setNewStock({ ...newStock, name: e.target.value })
            }
            required
          />

          <input
            type="number"
            placeholder="Quantity"
            className="border p-2 rounded"
            value={newStock.quantity}
            onChange={(e) =>
              setNewStock({ ...newStock, quantity: e.target.value })
            }
            required
          />

          {!newStock.currentPrice && (
            <input
              type="number"
              placeholder="Purchase Price"
              className="border p-2 rounded"
              value={newStock.purchasePrice}
              onChange={(e) =>
                setNewStock({ ...newStock, purchasePrice: e.target.value })
              }
            />
          )}

          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-700">Use Current Price</label>
            <input
              type="checkbox"
              className="border p-2 rounded"
              checked={newStock.currentPrice}
              onChange={(e) => {
                const isChecked = e.target.checked;
                setNewStock((prev) => ({
                  ...prev,
                  currentPrice: isChecked,
                  purchasePrice: isChecked ? '' : prev.purchasePrice,
                }));
              }}
            />
          </div>

          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="bg-gray-300 text-black py-2 px-4 rounded hover:bg-gray-400"
            >
              Cancel
            </button>
            <button
              type="submit"
              className={`bg-gray-700 text-white font-semibold py-2 px-4 rounded transition ${
                isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-600'
              }`}
              disabled={isLoading}
            >
              {isLoading ? 'Adding Stock...' : 'Add Stock'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}