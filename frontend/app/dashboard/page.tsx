"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/app/context/AuthContext";
import DashboardLayout from "@/components/DashboardLayout";
import ProtectedRoute from "@/components/ProtectedRoute";
import LoadingSpinner from "@/components/LoadingSpinner";
import Link from "next/link";
import { appointmentAPI, invoiceAPI } from "@/lib/api";

interface Appointment {
  id: string;
  doctor_name: string;
  date: string;
  time: string;
  status: string;
}

interface Invoice {
  id: string;
  amount: number;
  status: string;
  date: string;
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (user?.role === "patient") {
          const [appointmentsDataRaw, invoicesDataRaw] = await Promise.all([
            appointmentAPI.getMyAppointments(),
            invoiceAPI.getInvoices(),
          ]);

          const appointmentsData: any[] = Array.isArray(appointmentsDataRaw)
            ? appointmentsDataRaw
            : (appointmentsDataRaw as any)?.appointments || [];

          const invoicesData: any[] = Array.isArray(invoicesDataRaw)
            ? invoicesDataRaw
            : (invoicesDataRaw as any)?.invoices || [];

          const mappedAppointments = appointmentsData.map((a: any) => ({
            id: String(a.id),
            doctor_name: a.doctor_name || a.name || "Unknown Doctor",
            date: new Date(a.date).toDateString(),
            time: `${a.start_time} - ${a.end_time}`,
            status: a.status,
          }));

          const mappedInvoices = invoicesData.map((i: any) => ({
            id: String(i.invoice_id || i.id),
            amount: i.amount,
            status: i.status,
            date: new Date(i.issued_at || i.date).toDateString(),
          }));

          setAppointments(mappedAppointments);
          setInvoices(mappedInvoices);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchData();
    }
  }, [user]);

  return (
    <ProtectedRoute requiredRole="patient">
      <DashboardLayout>
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">
              Welcome, {user?.name}!
            </h1>
            <p className="text-secondary">Manage your appointments and invoices</p>
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
            <Link href="/book-appointment">
              <button className="w-full btn-primary text-left">
                <span className="block font-semibold">Book New Appointment</span>
                <span className="text-sm opacity-90">Schedule a visit with a doctor</span>
              </button>
            </Link>
            <Link href="/invoices">
              <button className="w-full btn-outline text-left">
                <span className="block font-semibold">View Invoices</span>
                <span className="text-sm">Check and pay your bills</span>
              </button>
            </Link>
          </div>

          {loading ? (
            <LoadingSpinner />
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Upcoming Appointments */}
              <div className="card p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-foreground">Upcoming Appointments</h2>
                  <Link href="/appointments">
                    <span className="text-primary text-sm font-medium hover:underline">View All</span>
                  </Link>
                </div>

                {appointments.length === 0 ? (
                  <p className="text-secondary py-8 text-center">No upcoming appointments</p>
                ) : (
                  <div className="space-y-3">
                    {appointments.slice(0, 3).map((apt) => (
                      <div
                        key={apt.id}
                        className="p-3 border border-border rounded-lg hover:border-primary transition-colors"
                      >
                        <p className="font-semibold text-foreground">{apt.doctor_name}</p>
                        <p className="text-sm text-secondary">{apt.date} at {apt.time}</p>
                        <span className={`inline-block text-xs px-2 py-1 rounded-full mt-2 ${
                          apt.status === "confirmed"
                            ? "bg-green-100 text-success"
                            : "bg-yellow-100 text-warning"
                        }`}>
                          {apt.status}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Recent Invoices */}
              <div className="card p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-foreground">Recent Invoices</h2>
                  <Link href="/invoices">
                    <span className="text-primary text-sm font-medium hover:underline">View All</span>
                  </Link>
                </div>

                {invoices.length === 0 ? (
                  <p className="text-secondary py-8 text-center">No invoices yet</p>
                ) : (
                  <div className="space-y-3">
                    {invoices.slice(0, 3).map((inv) => (
                      <div
                        key={inv.id}
                        className="p-3 border border-border rounded-lg flex justify-between items-center"
                      >
                        <div>
                          <p className="font-semibold text-foreground">₹{inv.amount}</p>
                          <p className="text-xs text-secondary">{inv.date}</p>
                        </div>
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          inv.status === "paid"
                            ? "bg-green-100 text-success"
                            : "bg-red-100 text-error"
                        }`}>
                          {inv.status}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
