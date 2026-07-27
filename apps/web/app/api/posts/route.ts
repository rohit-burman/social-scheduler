import { NextRequest, NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1];
    const { searchParams } = new URL(request.url);
    const statusFilter = searchParams.get('status_filter');
    const providerType = searchParams.get('provider_type');

    if (!token) {
      return NextResponse.json({ detail: 'No token provided' }, { status: 401 });
    }

    let url = `${API_URL}/api/v1/posts`;
    const params = new URLSearchParams();
    if (statusFilter) params.append('status_filter', statusFilter);
    if (providerType) params.append('provider_type', providerType);
    if (params.toString()) url += `?${params.toString()}`;

    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();

    if (!res.ok) {
      return NextResponse.json({ detail: data.detail || 'Failed to fetch posts' }, { status: res.status });
    }

    return NextResponse.json(data);
  } catch (err: any) {
    return NextResponse.json({ detail: 'Network error' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const token = request.headers.get('authorization')?.split(' ')[1];

    if (!token) {
      return NextResponse.json({ detail: 'No token provided' }, { status: 401 });
    }

    const res = await fetch(`${API_URL}/api/v1/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(body),
    });

    const data = await res.json();

    if (!res.ok) {
      return NextResponse.json({ detail: data.detail || 'Failed to create post' }, { status: res.status });
    }

    return NextResponse.json(data);
  } catch (err: any) {
    return NextResponse.json({ detail: 'Network error' }, { status: 500 });
  }
}