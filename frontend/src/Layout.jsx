import React from "react";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import { Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="flex h-screen bg-[#1E2347] text-white overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-[#202942] text-white h-full p-4">
        <Sidebar />
      </div>

      {/* Main Content Area */}
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* Topbar */}
        <div className="flex justify-between items-center px-4 py-3 bg-[#2f3c6c] text-white shadow">
          <Topbar />
        </div>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto px-6 py-6">
          <Outlet />
        </main>

        {/* Footer */}
        <div className="bg-[#1c1f3c] p-4 border-t border-blue-600 text-white text-sm text-center">
          Shipmate Command Interface Coming Soon...
        </div>
      </div>
    </div>
  );
}
