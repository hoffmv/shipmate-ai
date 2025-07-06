import React, { useState, useEffect } from "react";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:5000";

export default function AccountEditor() {
  const [accounts, setAccounts] = useState([]);
  const [newAccount, setNewAccount] = useState({
    name: "",
    type: "checking",
    balance: "",
    buffer_required: "",
    last_updated: new Date().toISOString().split("T")[0],
  });

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    const res = await fetch(`${API_BASE}/api/accounts`);
    const data = await res.json();
    setAccounts(data || []);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewAccount((prev) => ({ ...prev, [name]: value }));
  };

  const handleAddAccount = async () => {
    const res = await fetch(`${API_BASE}/api/accounts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newAccount),
    });

    if (res.ok) {
      setNewAccount({
        name: "",
        type: "checking",
        balance: "",
        buffer_required: "",
        last_updated: new Date().toISOString().split("T")[0],
      });
      fetchAccounts();
    }
  };

  const handleDelete = async (name) => {
    await fetch(`${API_BASE}/api/accounts/${encodeURIComponent(name)}`, {
      method: "DELETE",
    });
    fetchAccounts();
  };

  return (
    <div className="bg-gray-900 text-white p-6 rounded-lg shadow space-y-6">
      <h2 className="text-xl font-bold">Account Editor</h2>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <input
          name="name"
          placeholder="Account Name"
          value={newAccount.name}
          onChange={handleChange}
          className="bg-gray-700 text-white px-3 py-2 rounded"
        />
        <select
          name="type"
          value={newAccount.type}
          onChange={handleChange}
          className="bg-gray-700 text-white px-3 py-2 rounded"
        >
          <option value="checking">Checking</option>
          <option value="savings">Savings</option>
          <option value="credit">Credit</option>
          <option value="investment">Investment</option>
        </select>
        <input
          name="balance"
          type="number"
          placeholder="Balance"
          value={newAccount.balance}
          onChange={handleChange}
          className="bg-gray-700 text-white px-3 py-2 rounded"
        />
        <input
          name="buffer_required"
          type="number"
          placeholder="Buffer Required"
          value={newAccount.buffer_required}
          onChange={handleChange}
          className="bg-gray-700 text-white px-3 py-2 rounded"
        />
        <input
          name="last_updated"
          type="date"
          value={newAccount.last_updated}
          onChange={handleChange}
          className="bg-gray-700 text-white px-3 py-2 rounded"
        />
        <button
          onClick={handleAddAccount}
          className="md:col-span-5 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white font-semibold"
        >
          Add Account
        </button>
      </div>

      <ul className="divide-y divide-gray-700 mt-6">
        {accounts.map((acc) => (
          <li key={acc.name} className="py-3 flex justify-between items-center">
            <div>
              <div className="font-semibold">{acc.name} ({acc.type})</div>
              <div className="text-sm text-gray-400">
                Balance: ${acc.balance} | Buffer: ${acc.buffer_required} | Updated: {acc.last_updated}
              </div>
            </div>
            <button
              onClick={() => handleDelete(acc.name)}
              className="text-red-400 hover:text-red-300 text-sm"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
