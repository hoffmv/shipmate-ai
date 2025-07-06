import React, { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:5000";

export default function LedgerViewer() {
  const [ledger, setLedger] = useState([]);
  const [status, setStatus] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/api/ledger`)
      .then((res) => res.json())
      .then((data) => setLedger(data || []));
  }, []);

  const exportCSV = async () => {
    const res = await fetch(`${API_BASE}/api/ledger/export`);
    const result = await res.json();
    if (result.status === "success") {
      setStatus("Exported to: " + result.filename);
    } else {
      setStatus("Export failed.");
    }
  };

  return (
    <div className="p-6 bg-gray-900 text-white space-y-6 rounded-lg shadow">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">Transaction Ledger</h2>
        <button
          onClick={exportCSV}
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm text-white font-semibold"
        >
          Export to CSV
        </button>
      </div>
      {status && <div className="text-green-400 text-sm">{status}</div>}
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm bg-gray-800 rounded">
          <thead>
            <tr className="bg-gray-700 text-left">
              <th className="px-3 py-2">Timestamp</th>
              <th className="px-3 py-2">Type</th>
              <th className="px-3 py-2">Asset</th>
              <th className="px-3 py-2">Qty</th>
              <th className="px-3 py-2">Unit Price</th>
              <th className="px-3 py-2">Total</th>
              <th className="px-3 py-2">Profit?</th>
            </tr>
          </thead>
          <tbody>
            {ledger.map((entry) => (
              <tr key={entry.id} className="border-b border-gray-700">
                <td className="px-3 py-2">{entry.timestamp}</td>
                <td className="px-3 py-2">{entry.trade_type}</td>
                <td className="px-3 py-2">{entry.asset}</td>
                <td className="px-3 py-2">{entry.quantity}</td>
                <td className="px-3 py-2">${entry.price_per_unit.toFixed(2)}</td>
                <td className="px-3 py-2">${entry.total_value.toFixed(2)}</td>
                <td className="px-3 py-2 text-center">
                  {entry.is_profit ? "✅" : "❌"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
