'use client';
import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import { useGlobalContext } from '@/context/GlobalContext';
import AddStockModal from './AddStockModal'; // Adjust the path as needed

export default function Header() {
  const { currentPageTitle } = useGlobalContext();
  const [query, setQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [stocks, setStocks] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/protected`, {
          method: 'GET',
          credentials: 'include',
        });

        if (!res.ok) {
          router.push('/login');
        }

        const data = await res.json();
        console.log('Auth check passed:', data);
      } catch (err) {
        console.error(err);
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      const encodedQuery = encodeURIComponent(query.trim());
      router.push(`/stocks/${encodedQuery}`);
    }
  };

  const handleLogout = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/logout`, {
        method: 'POST',
        credentials: 'include',
      });

      if (!res.ok) {
        throw new Error('Failed to log out');
      }

      router.push('/login');
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  return (
    <header className="ml-64 bg-white shadow-md p-4 flex justify-between items-center sticky top-0 z-50 text-black">
      <h1 className="text-lg font-semibold">{currentPageTitle}</h1>
      <div className="flex items-center gap-4">
        <form
          className="flex items-center border rounded-md px-2"
          onSubmit={handleSearch}
        >
          <input
            type="text"
            placeholder="Search Stocks"
            className="p-2 outline-none text-sm"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button type="submit" className="text-blue-600 font-medium px-2">
            Search
          </button>
        </form>

       <button
  onClick={() => setIsModalOpen(true)}
  className="bg-gray-700 text-white w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-600 transition"
  title="Add Stock"
>
  <i className="fas fa-plus text-sm"></i>
</button>


        <i
          className="fas fa-sign-out-alt text-red-500 text-xl cursor-pointer"
          onClick={handleLogout}
          title="Logout"
        ></i>
      </div>

      {isModalOpen && (
        <AddStockModal
          setStocks={setStocks}
          onClose={() => setIsModalOpen(false)}
        />
      )}
    </header>
  );
}