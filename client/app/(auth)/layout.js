export const metadata = {
  title: 'Auth',
  description: 'Authentication pages',
};

export default function AuthLayout({ children }) {
  return (
    <main className="bg-gray-50 min-h-screen">
      {children}
    </main>
  );
}