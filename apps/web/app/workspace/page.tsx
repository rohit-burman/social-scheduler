'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function WorkspacePage() {
  const [workspaces, setWorkspaces] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedWorkspace, setSelectedWorkspace] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchWorkspaces = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/auth/login');
        return;
      }

      try {
        const res = await fetch('/api/workspaces', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || 'Failed to fetch workspaces');
        }

        setWorkspaces(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load workspaces');
      } finally {
        setLoading(false);
      }
    };

    fetchWorkspaces();
  }, [router]);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center bg-gray-50"><div className="text-gray-600">Loading...</div></div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Workspaces</h1>
        {error && <div className="text-red-600 mb-4">{error}</div>}

        <div className="mb-6">
          <button
            onClick={() => alert('Create workspace not yet implemented')}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Create New Workspace
          </button>
        </div>

        <h2 className="text-lg font-medium text-gray-900 mb-4">Your Workspaces</h2>
        {workspaces.length === 0 ? (
          <p className="text-gray-600">No workspaces yet.</p>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {workspaces.map((ws) => (
                <li key={ws.id}>
                  <div className="px-4 py-4 sm:px-6 hover:bg-gray-50 cursor-pointer" onClick={() => {
                    setSelectedWorkspace(ws.id);
                    localStorage.setItem('current_workspace', ws.slug);
                    router.push(`/dashboard`);
                  }}>
                    <div className="flex items-center justify-between">
                      <div className="truncate">
                        <div className="text-sm font-medium text-blue-600 truncate">{ws.name}</div>
                        <div className="mt-1 flex items-center text-sm text-gray-500">
                          <span className="truncate">Slug: {ws.slug}</span>
                          <span className="ml-2 flex-shrink-0 text-gray-400">Role: {ws.role}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}