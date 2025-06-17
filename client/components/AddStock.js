'use client';
import React, { useState } from 'react';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

export default function AddStock({setStocks}) {
  const [newStock, setNewStock] = useState({
    name: '',
    quantity: '',
    purchasePrice: '',
    currentPrice: false,
  });
  const [isLoading, setIsLoading] = useState(false);

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
        const result=response.data;
        const newData={
          _id: 9999,
          name: result["stock_info"]["name"],
          ticker: result["stock_info"]["symbol"],
          quantity: quantity,
          purchasePrice: result["stock_info"]["price"],
          currentPrice: result["stock_info"]["price"],
        }
        setNewStock({
          name: '',
          quantity: '',
          purchasePrice: '',
          currentPrice: false,
        });
        setStocks((prevStocks) => [...prevStocks, newData]);
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
    <section className="bg-white shadow p-6 rounded-lg mb-10 text-black">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Add New Stock</h2>
      <form
        className="grid grid-cols-1 md:grid-cols-2 gap-4"
        onSubmit={(e) => handleSubmit(e)}
      >
        <input
          type="text"
          placeholder="Company Name"
          className="border p-2 rounded col-span-1 md:col-span-2"
          value={newStock.name}
          onChange={(e) =>
            setNewStock({ ...newStock, name: e.target.value })
          }
          required
        />

        <input
          type="number"
          placeholder="Quantity"
          className={`border p-2 rounded ${
            newStock.currentPrice ? 'col-span-1 md:col-span-2' : ''
          }`}
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
          <label className="text-sm text-gray-700">OR Use Current Price</label>
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

        <button
          type="submit"
          className={`bg-gray-700 text-white font-semibold py-2 px-4 rounded col-span-1 md:col-span-2 transition ${
            isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-600'
          }`}
          disabled={isLoading}
        >
          {isLoading ? 'Adding Stock...' : 'Add Stock'}
        </button>
      </form>
    </section>
  );
}