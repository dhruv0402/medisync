"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import ProtectedRoute from "@/components/ProtectedRoute";
import LoadingSpinner from "@/components/LoadingSpinner";
import { invoiceAPI } from "@/lib/api";

interface Invoice {
  id: string;
  amount: number;
  status: string;
  date: string; // ISO string from backend
  appointment_id: string;
  doctor_name: string;
  description: string;
}

export default function InvoicesPage() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("all");
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null);

  useEffect(() => {
    const fetchInvoices = async () => {
      try {
        setLoading(true);
        const data = await invoiceAPI.getInvoices();
        const raw: any[] = Array.isArray(data)
          ? (data as any[])
          : (data as any)?.invoices ?? [];

        const normalized = raw.map((inv: any) => ({
          id: String(inv.id),
          amount: Number(inv.amount),
          status: inv.status,
          date: inv.issued_at,
          appointment_id: String(inv.appointment_id || ""),
          doctor_name: inv.doctor_name,
          description: inv.description || "Consultation",
        }));
        setInvoices(normalized);
      } catch (err) {
        setError("Failed to load invoices");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchInvoices();
  }, []);

  const handlePayment = async (invoiceId: string) => {
    try {
      await invoiceAPI.payInvoice(String(invoiceId));
      setInvoices((prev) =>
        prev.map((inv) =>
          inv.id === invoiceId ? { ...inv, status: "paid" } : inv
        )
      );
      setSelectedInvoice(null);
    } catch (err) {
      setError("Payment failed. Please try again.");
    }
  };

  const filteredInvoices =
    filter === "all"
      ? invoices
      : invoices.filter((inv) => inv.status === filter);

  const totalAmount = invoices.reduce((sum, inv) => sum + inv.amount, 0);
  const pendingAmount = invoices
    .filter((inv) => inv.status === "pending")
    .reduce((sum, inv) => sum + inv.amount, 0);

  const getStatusColor = (status: string) => {
    return status === "paid"
      ? "bg-green-100 text-success"
      : "bg-red-100 text-error";
  };

  return (
    <ProtectedRoute requiredRole="patient">
      <DashboardLayout>
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">Invoices</h1>
            <p className="text-secondary">View and manage your medical bills</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-error text-error rounded-lg">
              {error}
            </div>
          )}

          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="card p-6">
              <p className="text-secondary text-sm font-medium mb-1">Total Amount</p>
              <p className="text-3xl font-bold text-foreground">₹{totalAmount}</p>
            </div>
            <div className="card p-6 border-l-4 border-error">
              <p className="text-secondary text-sm font-medium mb-1">Pending</p>
              <p className="text-3xl font-bold text-error">₹{pendingAmount}</p>
            </div>
            <div className="card p-6 border-l-4 border-success">
              <p className="text-secondary text-sm font-medium mb-1">Paid</p>
              <p className="text-3xl font-bold text-success">₹{totalAmount - pendingAmount}</p>
            </div>
          </div>

          {/* Filters */}
          <div className="flex gap-2 mb-6">
            {["all", "pending", "paid"].map((status) => (
              <button
                key={status}
                onClick={() => setFilter(status)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === status
                    ? "bg-primary text-white"
                    : "bg-border text-foreground hover:bg-border-dark"
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            ))}
          </div>

          {/* Invoices Table */}
          {loading ? (
            <LoadingSpinner />
          ) : filteredInvoices.length === 0 ? (
            <div className="card p-12 text-center">
              <p className="text-secondary text-lg">No invoices found</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b-2 border-border">
                    <th className="text-left p-4 font-semibold text-foreground">Invoice ID</th>
                    <th className="text-left p-4 font-semibold text-foreground">Doctor</th>
                    <th className="text-left p-4 font-semibold text-foreground">Date</th>
                    <th className="text-left p-4 font-semibold text-foreground">Amount</th>
                    <th className="text-left p-4 font-semibold text-foreground">Status</th>
                    <th className="text-left p-4 font-semibold text-foreground">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredInvoices.map((invoice) => (
                    <tr key={invoice.id} className="table-row">
                      <td className="p-4 text-foreground font-mono text-sm">{invoice.id}</td>
                      <td className="p-4 text-foreground">{invoice.doctor_name}</td>
                      <td className="p-4 text-foreground">{new Date(invoice.date).toLocaleDateString()}</td>
                      <td className="p-4 text-foreground font-semibold">₹{invoice.amount}</td>
                      <td className="p-4">
                        <span
                          className={`text-xs px-3 py-1 rounded-full font-medium ${getStatusColor(
                            invoice.status
                          )}`}
                        >
                          {invoice.status.charAt(0).toUpperCase() + invoice.status.slice(1)}
                        </span>
                      </td>
                      <td className="p-4">
                        {invoice.status === "pending" ? (
                          <button
                            onClick={() => setSelectedInvoice(invoice)}
                            className="text-primary text-sm font-medium hover:underline"
                          >
                            Pay Now
                          </button>
                        ) : (
                          <span className="text-secondary text-sm">-</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Payment Modal */}
          {selectedInvoice && (
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
              <div className="card max-w-md w-full p-6">
                <h2 className="text-2xl font-bold text-foreground mb-4">Confirm Payment</h2>
                <div className="space-y-4 mb-6">
                  <div>
                    <p className="text-sm text-secondary">Invoice ID</p>
                    <p className="font-mono text-foreground">{selectedInvoice.id}</p>
                  </div>
                  <div>
                    <p className="text-sm text-secondary">Amount</p>
                    <p className="text-2xl font-bold text-foreground">₹{selectedInvoice.amount}</p>
                  </div>
                  <div>
                    <p className="text-sm text-secondary">Description</p>
                    <p className="text-foreground">{selectedInvoice.description}</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={() => setSelectedInvoice(null)}
                    className="flex-1 btn-outline"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => handlePayment(selectedInvoice.id)}
                    className="flex-1 btn-primary"
                  >
                    Pay ₹{selectedInvoice.amount}
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
