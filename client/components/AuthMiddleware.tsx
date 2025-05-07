'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';

interface AuthMiddlewareProps {
  children: React.ReactNode;
}

export default function AuthMiddleware({ children }: AuthMiddlewareProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const isGuest = localStorage.getItem('isGuest') === 'true';

    // Allow access to login page without authentication
    if (pathname === '/login') {
      setIsLoading(false);
      return;
    }

    // If no token and not guest, redirect to login
    if (!token && !isGuest) {
      router.push('/login');
      return;
    }

    setIsLoading(false);
  }, [pathname, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return <>{children}</>;
} 