import axios from "axios";

const API_BASE_URL = "http://localhost:5001/api";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) {
  const cfg = config as any;

  cfg.headers = cfg.headers || {};
  cfg.headers.Authorization = `Bearer ${token}`;
}
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle responses
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

// Auth APIs
export const authAPI = {
  login: (email: string, password: string) =>
    apiClient.post("/auth/login", { email, password }),
};

// Appointment APIs
export const appointmentAPI = {
  getDoctors: (departmentId: string | number) =>
    apiClient.get(`/appointments/doctors?department_id=${departmentId}`),
  getSlots: (doctorId: number, date: string) =>
    apiClient.get(`/appointments/slots?doctor_id=${doctorId}&date=${date}`),
  bookAppointment: (data: any) =>
    apiClient.post("/appointments/book", data),
  getMyAppointments: () =>
    apiClient.get("/appointments"),
  cancelAppointment: (appointmentId: number) =>
    apiClient.delete(`/appointments/${appointmentId}`),
  completeAppointment: (appointmentId: number) =>
    apiClient.put(`/appointments/complete/${appointmentId}`, {}),
};

// Invoice APIs
export const invoiceAPI = {
  getInvoices: () =>
    apiClient.get("/invoices"),
  payInvoice: (invoiceId: string) =>
    apiClient.post(`/invoices/pay/${invoiceId}`, {}),
};

// Admin APIs
export const adminAPI = {
  getDashboard: () =>
    apiClient.get("/admin/dashboard"),
};

// Health check
export const healthCheck = () =>
  apiClient.get("/health");

export default apiClient;
