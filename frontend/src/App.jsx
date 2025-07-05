import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./Layout";

// Actual pages – plug your real components in here
import FinanceDashboard from "./pages/FinanceDashboard";
import TradingDashboard from "./pages/TradingDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import SchedulingDashboard from "./pages/SchedulingDashboard";
import CommsDashboard from "./pages/CommsDashboard";
import WellnessDashboard from "./pages/WellnessDashboard";
import RNDDashboard from "./pages/RNDDashboard";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="finance" element={<FinanceDashboard />} />
          <Route path="trading" element={<TradingDashboard />} />
          <Route path="admin" element={<AdminDashboard />} />
          <Route path="scheduling" element={<SchedulingDashboard />} />
          <Route path="comms" element={<CommsDashboard />} />
          <Route path="wellness" element={<WellnessDashboard />} />
          <Route path="rnd" element={<RNDDashboard />} />
        </Route>
      </Routes>
    </Router>
  );
}
