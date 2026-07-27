'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');
  const router = useRouter();

  useEffect(() => {
    const fetchPosts = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/auth/login');
        return;
      }

      try {
        let url = '/api/posts';
        if (filter !== 'all') {
          url += `?status_filter=${filter}`;
        }

        const res = await fetch(url, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || 'Failed to fetch posts');
        }

        setPosts(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load posts');
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
    const interval = setInterval(fetchPosts, 15000); // Poll every 15 seconds
    return () => clearInterval(interval);
  }, [filter, router]);

  const statusCounts = {
    draft: posts.filter(p => p.status === 'draft').length,
    scheduled: posts.filter(p => p.status === 'scheduled').length,
    published: posts.filter(p => p.status === 'published').length,
    failed: posts.filter(p => p.status === 'failed').length,
  };

  const getStatusBadge = (status: string) => {
    const colors: Record<string, string> = {
      draft: 'bg-yellow-500',
      scheduled: 'bg-blue-500',
      published: 'bg-green-500',
      failed: 'bg-red-500',
    };
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-white ${colors[status] || 'bg-gray-500'}`}>
        {status}
      </span>
    );
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center bg-gray-50"><div className="text-gray-600">Loading...</div></div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-white overflow-hidden shadow rounded-lg p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-yellow-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Draft</dt>
                  <dd className="text-3xl font-semibold text-gray-900">{statusCounts.draft}</dd>
                </dl>
              </div>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Scheduled</dt>
                  <dd className="text-3xl font-semibold text-gray-900">{statusCounts.scheduled}</dd>
                </dl>
              </div>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Published</dt>
                  <dd className="text-3xl font-semibold text-gray-900">{statusCounts.published}</dd>
                </dl>
              </div>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-red-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Failed</dt>
                  <dd className="text-3xl font-semibold text-gray-900">{statusCounts.failed}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="mb-6">
          <button
            onClick={() => alert('Create post not yet implemented')}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
          >
            Create Post
          </button>
        </div>

        <div className="mb-4">
          <label className="mr-2 text-sm font-medium text-gray-700">Filter:</label>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="block w-40 pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
          >
            <option value="all">All</option>
            <option value="draft">Draft</option>
            <option value="scheduled">Scheduled</option>
            <option value="published">Published</option>
            <option value="failed">Failed</option>
          </select>
        </div>

        {error && <div className="text-red-600 mb-4">{error}</div>}

        <h2 className="text-lg font-medium text-gray-900 mb-4">Posts</h2>
        {posts.length === 0 ? (
          <p className="text-gray-600">No posts found.</p>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {posts.map((post) => (
                <li key={post.id}>
                  <div className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <p className="text-sm text-gray-900 truncate max-w-md">{post.content.substring(0, 100)}{post.content.length > 100 ? '...' : ''}</p>
                      {getStatusBadge(post.status)}
                    </div>
                    <div className="mt-2 flex items-center text-sm text-gray-500">
                      <span>Provider: {post.provider_type}</span>
                      {post.scheduled_at && <span className="ml-4">Scheduled: {post.scheduled_at}</span>}
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