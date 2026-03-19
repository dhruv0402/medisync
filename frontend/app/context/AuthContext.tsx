"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { authAPI } from "@/lib/api";

interface User {
  id: string | number;
  email: string;
  name: string;
  role: "patient" | "doctor" | "admin";
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        localStorage.removeItem("user");
      }
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
  try {
    const response: any = await authAPI.login(email, password);
    console.log("LOGIN RESPONSE:", response);

    // 👇 Normalize response (THIS IS THE FIX)
    const userData: User = {
      id: response.id,
      email: response.email,
      name: response.name,
      role: response.role as "patient" | "doctor" | "admin",
    };

    localStorage.setItem("token", response.token || "");
    localStorage.setItem("user", JSON.stringify(userData));

    setUser(userData);

  } catch (error: any) {
    console.error("LOGIN ERROR:", error);
    throw error;
  }
};

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
