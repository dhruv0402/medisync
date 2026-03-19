// User Types
export interface User {
  id: string;
  email: string;
  name: string;
  role: "patient" | "doctor" | "admin";
}

export interface AuthResponse {
  token: string;
  user: User;
}

// Appointment Types
export interface Doctor {
  id: string;
  name: string;
  specialization: string;
  email: string;
}

export interface Appointment {
  id: string;
  doctor_id: string;
  doctor_name: string;
  patient_id?: string;
  patient_name?: string;
  date: string;
  time: string;
  status: "confirmed" | "completed" | "cancelled" | "pending";
  reason?: string;
  notes?: string;
}

export interface Slot {
  id: string;
  time: string;
  available: boolean;
}

// Invoice Types
export interface Invoice {
  id: string;
  amount: number;
  status: "pending" | "paid";
  date: string;
  appointment_id: string;
  doctor_name: string;
  description: string;
}

// Admin Dashboard Types
export interface AdminDashboardData {
  total_revenue: number;
  today_revenue: number;
  pending_invoices: number;
  completed_appointments: number;
  top_doctor: {
    name: string;
    appointments_count: number;
  };
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface ApiError {
  message: string;
  status: number;
}

// Form Types
export interface LoginFormData {
  email: string;
  password: string;
}

export interface BookAppointmentFormData {
  doctor_id: string;
  slot_id: string;
  date: string;
  reason?: string;
}
