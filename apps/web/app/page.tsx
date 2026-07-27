'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function HomePage() {
  const [user, setUser] = useState<any>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h1 className="mt-6 text-center text-4xl font-extrabold text-gray-900">
            Social Scheduler
          </h1>
          <p className="mt-2 text-center text-sm text-gray-600">
            Workspace-based social content automation scheduler
          </p>
        </div>

        <div className="flex gap-4 justify-center">
          <Link
            href="/auth/login"
            className="group relative w-32 flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Login
          </Link>
          <Link
            href="/auth/signup"
            className="group relative w-32 flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            Sign Up
          </Link>
        </div>

        {token && (
          <div className="bg-gray-100 rounded-lg p-6">
            <p className="text-gray-700">You are logged in. Go to your workspace to get started.</p>
            <Link
              href="/workspace"
              className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Go to Workspace
            </Link>
          </div>
        )}
      </div>
    </main>
  );
}