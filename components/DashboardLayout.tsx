"use client";

import Sidebar from "./Sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 ml-0 md:ml-64 p-4 md:p-8">
        {children}
      </main>
    </div>
  );
}
