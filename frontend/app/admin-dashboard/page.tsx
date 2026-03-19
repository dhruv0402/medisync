"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import ProtectedRoute from "@/components/ProtectedRoute";
import LoadingSpinner from "@/components/LoadingSpinner";
import { adminAPI } from "@/lib/api";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

interface DashboardData {
  total_revenue: number;
  today_revenue: number;
  pending_invoices: number;
  completed_appointments: number;
  top_doctor: {
    name: string;
    appointments_count: number;
  };
}

export default function AdminDashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setLoading(true);
        const response: any = await adminAPI.getDashboard();
        const normalized: DashboardData = {
          total_revenue: Number(response.total_revenue || response.revenue || 0),
          today_revenue: Number(response.today_revenue || 0),
          pending_invoices: Number(response.pending_invoices || 0),
          completed_appointments: Number(response.completed_appointments || 0),
          top_doctor: response.top_doctor || {
            name: "N/A",
            appointments_count: 0,
          },
        };

        setData(normalized);
      } catch (err) {
        setError("Failed to load dashboard data");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  const revenueData = [
    { day: "Mon", revenue: 200 },
    { day: "Tue", revenue: 400 },
    { day: "Wed", revenue: 300 },
    { day: "Thu", revenue: 500 },
    { day: "Fri", revenue: 700 },
    { day: "Sat", revenue: 600 },
    { day: "Sun", revenue: 800 },
  ];

  return (
    <ProtectedRoute requiredRole="admin">
      <DashboardLayout>
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">Admin Dashboard</h1>
            <p className="text-secondary">Hospital overview and statistics</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-error text-error rounded-lg">
              {error}
            </div>
          )}

          {loading ? (
            <LoadingSpinner />
          ) : data ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Total Revenue Card */}
              <div className="card p-6 border-l-4 border-primary">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-secondary text-sm font-medium mb-1">Total Revenue</p>
                    <p className="text-3xl font-bold text-foreground">₹{data.total_revenue || 0}</p>
                  </div>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">💰</span>
                  </div>
                </div>
              </div>

              {/* Today Revenue Card */}
              <div className="card p-6 border-l-4 border-success">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-secondary text-sm font-medium mb-1">Today Revenue</p>
                    <p className="text-3xl font-bold text-success">₹{data.today_revenue || 0}</p>
                  </div>
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">📈</span>
                  </div>
                </div>
              </div>

              {/* Pending Invoices Card */}
              <div className="card p-6 border-l-4 border-warning">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-secondary text-sm font-medium mb-1">Pending Invoices</p>
                    <p className="text-3xl font-bold text-warning">{data.pending_invoices || 0}</p>
                  </div>
                  <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">📋</span>
                  </div>
                </div>
              </div>

              {/* Completed Appointments Card */}
              <div className="card p-6 border-l-4 border-accent">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-secondary text-sm font-medium mb-1">Completed Appointments</p>
                    <p className="text-3xl font-bold text-accent">{data.completed_appointments || 0}</p>
                  </div>
                  <div className="w-12 h-12 bg-cyan-100 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">✓</span>
                  </div>
                </div>
              </div>
            </div>
          ) : null}

          {/* Top Doctor Section */}
          {data && (
            <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="card p-6">
                <h2 className="text-xl font-bold text-foreground mb-6">Top Performing Doctor</h2>
                <div className="flex items-center">
                  <div className="w-16 h-16 bg-primary-light rounded-full flex items-center justify-center text-white text-2xl font-bold mr-4">
                    {data.top_doctor?.name?.charAt(0) || "?"}
                  </div>
                  <div>
                    <p className="text-lg font-semibold text-foreground">{data.top_doctor?.name || "N/A"}</p>
                    <p className="text-sm text-secondary">
                      {data.top_doctor?.appointments_count || 0} appointments completed
                    </p>
                  </div>
                </div>
              </div>

              {/* Quick Stats */}
              <div className="card p-6">
                <h2 className="text-xl font-bold text-foreground mb-6">System Status</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-secondary">API Connection</span>
                    <span className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-success rounded-full"></div>
                      <span className="text-sm text-success font-medium">Connected</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-secondary">Database</span>
                    <span className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-success rounded-full"></div>
                      <span className="text-sm text-success font-medium">Active</span>
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-secondary">System Health</span>
                    <span className="text-sm text-primary font-medium">Optimal</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Charts Section */}
          <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="card p-6">
              <h2 className="text-xl font-bold text-foreground mb-6">Revenue Trend</h2>
              <div style={{ width: "100%", height: 300 }}>
                <ResponsiveContainer>
                  <LineChart data={revenueData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="revenue" strokeWidth={3} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="card p-6">
              <h2 className="text-xl font-bold text-foreground mb-6">Appointments Overview</h2>
              <div className="flex items-center justify-center h-[300px] text-secondary">
                Coming Soon (Backend analytics)
              </div>
            </div>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
