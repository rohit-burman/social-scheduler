import { NextRequest, NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, password, name } = body;

    const res = await fetch(`${API_URL}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
    });

    const data = await res.json();

    if (!res.ok) {
      return NextResponse.json({ detail: data.detail || 'Registration failed' }, { status: res.status });
    }

    return NextResponse.json(data);
  } catch (err: any) {
    return NextResponse.json({ detail: 'Network error' }, { status: 500 });
  }
}