"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import ProtectedRoute from "@/components/ProtectedRoute";
import LoadingSpinner from "@/components/LoadingSpinner";
import { appointmentAPI } from "@/lib/api";
import { useAuth } from "@/app/context/AuthContext";

interface Appointment {
  id: number;
  doctor_name: string;
  patient_name?: string;
  date: string;
  time: string;
  status: string;
  reason?: string;
}

export default function AppointmentsPage() {
  const { user } = useAuth();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        setLoading(true);
        const data: any = await appointmentAPI.getMyAppointments();
        const rawAppointments = Array.isArray(data) ? data : data?.appointments || [];

        const normalizedAppointments: Appointment[] = rawAppointments.map((apt: any) => ({
          id: Number(apt.id),
          doctor_name: apt.doctor_name || apt.name || "Unknown Doctor",
          patient_name: apt.patient_name || apt.patient || "",
          date: apt.date || "",
          time: apt.time || `${apt.start_time || ""} - ${apt.end_time || ""}`,
          status: apt.status || "confirmed",
          reason: apt.reason || "",
        }));

        setAppointments(normalizedAppointments);
      } catch (err) {
        setError("Failed to load appointments");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchAppointments();
    }
  }, [user]);

  const handleCancel = async (appointmentId: number) => {
    if (!confirm("Are you sure you want to cancel this appointment?")) return;

    try {
      await appointmentAPI.cancelAppointment(appointmentId);
      setAppointments((prev) =>
        prev.map((apt) =>
          apt.id === appointmentId ? { ...apt, status: "cancelled" } : apt
        )
      );
    } catch (err) {
      setError("Failed to cancel appointment");
    }
  };

  const handleComplete = async (appointmentId: number) => {
    try {
      await appointmentAPI.completeAppointment(appointmentId);
      setAppointments((prev) =>
        prev.map((apt) =>
          apt.id === appointmentId ? { ...apt, status: "completed" } : apt
        )
      );
    } catch (err) {
      setError("Failed to complete appointment");
    }
  };

  const filteredAppointments =
    filter === "all"
      ? appointments
      : appointments.filter((apt) => apt.status === filter);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "confirmed":
        return "bg-green-100 text-success";
      case "completed":
        return "bg-blue-100 text-primary";
      case "cancelled":
        return "bg-red-100 text-error";
      default:
        return "bg-yellow-100 text-warning";
    }
  };

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">Appointments</h1>
            <p className="text-secondary">Manage your appointment schedule</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-error text-error rounded-lg">
              {error}
            </div>
          )}

          {/* Filters */}
          <div className="flex gap-2 mb-6 flex-wrap">
            {["all", "confirmed", "completed", "cancelled"].map((status) => (
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

          {loading ? (
            <LoadingSpinner />
          ) : filteredAppointments.length === 0 ? (
            <div className="card p-12 text-center">
              <p className="text-secondary text-lg">No appointments found</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b-2 border-border">
                    <th className="text-left p-4 font-semibold text-foreground">Doctor</th>
                    {user?.role !== "patient" && (
                      <th className="text-left p-4 font-semibold text-foreground">Patient</th>
                    )}
                    <th className="text-left p-4 font-semibold text-foreground">Date & Time</th>
                    {user?.role === "patient" && (
                      <th className="text-left p-4 font-semibold text-foreground">Reason</th>
                    )}
                    <th className="text-left p-4 font-semibold text-foreground">Status</th>
                    <th className="text-left p-4 font-semibold text-foreground">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredAppointments.map((apt) => (
                    <tr key={apt.id} className="table-row">
                      <td className="p-4 text-foreground">{apt.doctor_name}</td>
                      {user?.role !== "patient" && (
                        <td className="p-4 text-foreground">{apt.patient_name || "-"}</td>
                      )}
                      <td className="p-4 text-foreground">
                        <div>{apt.date}</div>
                        <div className="text-sm text-secondary">{apt.time}</div>
                      </td>
                      {user?.role === "patient" && (
                        <td className="p-4 text-secondary text-sm">{apt.reason || "-"}</td>
                      )}
                      <td className="p-4">
                        <span className={`text-xs px-3 py-1 rounded-full font-medium ${getStatusColor(apt.status)}`}>
                          {apt.status.charAt(0).toUpperCase() + apt.status.slice(1)}
                        </span>
                      </td>
                      <td className="p-4">
                        {user?.role === "patient" && apt.status === "confirmed" && (
                          <button
                            onClick={() => handleCancel(apt.id)}
                            className="text-error text-sm font-medium hover:underline"
                          >
                            Cancel
                          </button>
                        )}
                        {(user?.role === "doctor" || user?.role === "admin") &&
                          apt.status === "confirmed" && (
                            <button
                              onClick={() => handleComplete(apt.id)}
                              className="text-success text-sm font-medium hover:underline"
                            >
                              Complete
                            </button>
                          )}
                        {apt.status !== "confirmed" && (
                          <span className="text-secondary text-sm">-</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
