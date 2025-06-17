import Link from 'next/link';
import { useState, useEffect } from 'react';

export default function HomeHeader() {
    const [isAuthorized, setIsAuthorized] = useState(false);

    useEffect(() => {
        const checkAuthorization = async () => {
            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/protected`, {
                    method: 'GET',
                    credentials: 'include', // Include cookies for authentication
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) throw new Error('Failed to fetch user data');

                setIsAuthorized(true); // User is authorized if fetch succeeds
            } catch (error) {
                console.error('Authorization check failed:', error);
                setIsAuthorized(false); // User is not authorized
            }
        };

        checkAuthorization();
    }, []);

    const handleLogout = async () => {
        try {
            await fetch(`${process.env.NEXT_PUBLIC_API_URL}/logout`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            setIsAuthorized(false); // Update state to reflect logout
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return (
        <header className="bg-[#0B1340] shadow-lg p-4 flex justify-between items-center sticky top-0 z-50 w-full">
            <div className="flex items-center space-x-3">
                <h1 className="text-2xl font-extrabold tracking-tight text-[#A5BFFA] md:text-3xl">TRADENEXUS AI</h1>
                <p className="text-xs text-[#A5BFFA] italic md:text-sm">AI that Thinks Finance</p>
            </div>
            <nav className="flex items-center space-x-4">
                <Link href="/about" className="text-[#A5BFFA] hover:text-white font-medium transition duration-200 text-sm md:text-base">About</Link>
                {isAuthorized ? (
                    <>
                        
                        <Link 
                            href="/portfolio" 
                            className="bg-[#38BDF8] hover:bg-[#7DD3FC] text-white px-4 py-1.5 rounded-md font-semibold transition duration-200 text-sm md:text-base md:px-5 md:py-2"
                        >
                            Get Started
                        </Link>
                        <button 
                            onClick={handleLogout} 
                            className="bg-[#A5BFFA] text-[#0B1340] px-4 py-1.5 rounded-md font-semibold hover:bg-[#D6E4FF] transition duration-200 text-sm md:text-base md:px-5 md:py-2 flex items-center"
                        >
                            Logout 
                        </button>
                    </>
                ) : (
                    <Link 
                        href="/login" 
                        className="bg-[#A5BFFA] text-[#0B1340] px-4 py-1.5 rounded-md font-semibold hover:bg-[#D6E4FF] transition duration-200 text-sm md:text-base md:px-5 md:py-2"
                    >
                        Login
                    </Link>
                )}
            </nav>
        </header>
    );
}