"use client";

import Link from "next/link";
import { useAuth } from "@/app/context/AuthContext";
import { useRouter, usePathname } from "next/navigation";
import { useState } from "react";

export default function Sidebar() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  if (!user) return null;

  const getNavLinks = () => {
    const baseLinks = [];
    
    if (user.role === "patient") {
      return [
        { href: "/dashboard", label: "Dashboard" },
        { href: "/appointments", label: "My Appointments" },
        { href: "/book-appointment", label: "Book Appointment" },
        { href: "/invoices", label: "Invoices" },
      ];
    } else if (user.role === "doctor") {
      return [
        { href: "/dashboard", label: "Dashboard" },
        { href: "/appointments", label: "Appointments" },
      ];
    } else if (user.role === "admin") {
      return [
        { href: "/admin-dashboard", label: "Dashboard" },
        { href: "/appointments", label: "Appointments" },
      ];
    }
    return baseLinks;
  };

  const navLinks = getNavLinks();

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setIsMobileOpen(!isMobileOpen)}
        className="fixed top-4 left-4 z-50 md:hidden bg-primary text-white p-2 rounded-lg"
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>

      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-0 h-screen w-64 bg-slate-900 text-white overflow-y-auto transition-transform duration-300 md:translate-x-0 z-40 ${
          isMobileOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="p-6">
          <h1 className="text-2xl font-bold text-accent">MediSync</h1>
          <p className="text-sm text-secondary-light mt-1">Hospital System</p>
        </div>

        {/* User Info */}
        <div className="px-6 py-4 border-t border-slate-700">
          <p className="text-sm text-secondary-light">Logged in as</p>
          <p className="font-semibold text-white truncate">{user.name}</p>
          <p className="text-xs text-secondary-light capitalize">{user.role}</p>
        </div>

        {/* Navigation Links */}
        <nav className="mt-6">
          {navLinks.map((link) => (
            <Link key={link.href} href={link.href}>
              <span
                className={`block px-6 py-3 transition-colors ${
                  pathname === link.href
                    ? "bg-primary border-l-4 border-accent"
                    : "hover:bg-slate-800"
                }`}
              >
                {link.label}
              </span>
            </Link>
          ))}
        </nav>

        {/* Logout Button */}
        <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-slate-700">
          <button
            onClick={handleLogout}
            className="w-full px-4 py-2 bg-error text-white rounded-lg hover:bg-red-600 transition-colors font-medium"
          >
            Logout
          </button>
        </div>
      </aside>

      {/* Overlay */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 md:hidden"
          onClick={() => setIsMobileOpen(false)}
        />
      )}
    </>
  );
}
