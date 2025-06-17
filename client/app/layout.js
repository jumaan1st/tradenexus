import { GlobalProvider } from '@/context/GlobalContext';
import './globals.css';

export const metadata = {
  title: 'TRADENEXUS AI - Portfolio Analyzer',
  description: 'AI that Thinks Finance',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <GlobalProvider>
          {children}
        </GlobalProvider>
      </body>
    </html>
  );
}
