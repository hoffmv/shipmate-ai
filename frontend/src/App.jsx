import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./Layout";

// Core Pages
import FinanceDashboard from "./pages/FinanceDashboard";
import GoalEditor from "./pages/GoalEditor";
import PaymentCalendar from "./pages/PaymentCalendar";
import AccountEditor from "./pages/AccountEditor";
import DocumentUploader from "./pages/DocumentUploader";
import LedgerViewer from "./pages/LedgerViewer";

// Other Divisions
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
          <Route path="goals" element={<GoalEditor />} />
          <Route path="calendar" element={<PaymentCalendar />} />
          <Route path="accounts" element={<AccountEditor />} />
          <Route path="upload" element={<DocumentUploader />} />
          <Route path="ledger" element={<LedgerViewer />} />
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
