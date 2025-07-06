import React, { useEffect, useState } from "react";
import {
  ArrowDownIcon,
  ArrowUpIcon,
  PlusCircleIcon,
  CreditCardIcon,
  ShieldCheckIcon,
} from "@heroicons/react/24/outline";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:5000";

export default function FinanceDashboard() {
  const [accounts, setAccounts] = useState([]);
  const [goals, setGoals] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/accounts`)
      .then(res => res.json())
      .then(data => setAccounts(data || []));
    fetch(`${API_BASE}/api/goals`)
      .then(res => res.json())
      .then(data => setGoals(data || []));
  }, []);

  const totalBalance = accounts.reduce((sum, acc) => sum + parseFloat(acc.balance || 0), 0);
  const totalBuffer = accounts.reduce((sum, acc) => sum + parseFloat(acc.buffer_required || 0), 0);
  const spendChange = "-3.2%"; // Placeholder
  const savingsChange = "+1.8%"; // Placeholder

  return (
    <section className="space-y-8">
      <h1 className="text-2xl font-bold text-white">Gold Digger Command</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Total Buffer Required */}
        <div className="bg-gray-800 rounded-lg p-5 shadow flex flex-col justify-between">
          <div className="flex justify-between items-center text-sm text-gray-400 uppercase">
            <span>Total Buffer Required</span>
            <span className="flex items-center text-red-400">
              <span className="inline-flex items-center justify-center w-5 h-5 mr-1">
                <ArrowDownIcon className="w-4 h-4" />
              </span>
              {spendChange}
            </span>
          </div>
          <div className="mt-4 text-3xl font-bold text-white">${totalBuffer.toFixed(2)}</div>
        </div>

        {/* Total Balance */}
        <div className="bg-gray-800 rounded-lg p-5 shadow flex flex-col justify-between">
          <div className="flex justify-between items-center text-sm text-gray-400 uppercase">
            <span>Total Balance</span>
            <span className="flex items-center text-green-400">
              <span className="inline-flex items-center justify-center w-5 h-5 mr-1">
                <ArrowUpIcon className="w-4 h-4" />
              </span>
              {savingsChange}
            </span>
          </div>
          <div className="mt-4 text-3xl font-bold text-white">${totalBalance.toFixed(2)}</div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gray-800 rounded-lg p-5 shadow">
          <span className="text-sm uppercase text-gray-400 mb-3 block">
            Quick Actions
          </span>
          <div className="flex flex-col space-y-3 md:space-y-0 md:flex-row md:space-x-3">
            {[
              { label: "Add Expense", icon: PlusCircleIcon, color: "bg-blue-600 hover:bg-blue-700" },
              { label: "Pay Bill", icon: CreditCardIcon, color: "bg-green-600 hover:bg-green-700" },
              { label: "Secure Funds", icon: ShieldCheckIcon, color: "bg-gray-700 hover:bg-gray-600" }
            ].map(action => (
              <button key={action.label} className={`flex items-center justify-center px-4 py-3 rounded-md ${action.color} text-white font-medium space-x-2`}>
                <span className="w-5 h-5 inline-flex items-center justify-center">
                  <action.icon className="w-5 h-5" />
                </span>
                <span>{action.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Financial Goals */}
      <div className="bg-gray-800 rounded-lg p-5 shadow">
        <h2 className="text-sm uppercase text-gray-400 mb-3">Goal Progress</h2>
        {goals.length === 0 ? (
          <p className="text-gray-400">No goals defined yet.</p>
        ) : (
          <ul className="space-y-4">
            {goals.map(goal => {
              const progress = Math.min(100, (goal.current_amount / goal.target_amount) * 100).toFixed(0);
              return (
                <li key={goal.name}>
                  <div className="text-white font-medium">{goal.name}</div>
                  <div className="text-sm text-gray-400 mb-1">
                    ${goal.current_amount} of ${goal.target_amount} by {goal.deadline}
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2.5">
                    <div className="bg-green-500 h-2.5 rounded-full" style={{ width: `${progress}%` }}></div>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </section>
  );
}
