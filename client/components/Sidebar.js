'use client';
import Link from 'next/link';


export default function Sidebar() {
   
  const menuItems = [
    { name: 'Portfolio Overview', href: '/portfolio' },
    { name: 'AI Analysis', href: '/analysis' },
    { name: 'Prediction', href: '/stocks' },
    { name: 'Trends', href: '/trends' },
    // { name: 'Profile', href: '/profile' },
    // { name: 'Settings', href: '/settings' },
  ];

  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen fixed">
      <div className="p-6 text-center font-bold text-xl border-b border-gray-700">
        <Link href="/" passHref>
        <i className="fas fa-chart-line mr-2"></i> TRADENEXUS AI
        </Link>
      </div>
      <ul className="mt-4 space-y-2 px-4">
        {menuItems.map((item, i) => (
          <li key={i}>
            <Link href={item.href} passHref>
              <div className="p-3 hover:bg-gray-700 rounded cursor-pointer flex items-center">
                <i className="fas fa-angle-right mr-2"></i> {item.name}
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </aside>
  );
}
