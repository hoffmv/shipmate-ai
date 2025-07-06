import React, { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:5000";

export default function GoalEditor() {
  const [goals, setGoals] = useState([]);
  const [newGoal, setNewGoal] = useState({
    name: "",
    target_amount: "",
    current_amount: "",
    deadline: "",
    priority: "medium",
  });

  useEffect(() => {
    fetchGoals();
  }, []);

  const fetchGoals = async () => {
    const res = await fetch(`${API_BASE}/api/goals`);
    const data = await res.json();
    setGoals(data || []);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewGoal((prev) => ({ ...prev, [name]: value }));
  };

  const handleAddGoal = async () => {
    const res = await fetch(`${API_BASE}/api/goals`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newGoal),
    });
    if (res.ok) {
      setNewGoal({ name: "", target_amount: "", current_amount: "", deadline: "", priority: "medium" });
      fetchGoals();
    }
  };

  const handleDeleteGoal = async (name) => {
    await fetch(`${API_BASE}/api/goals/${encodeURIComponent(name)}`, {
      method: "DELETE",
    });
    fetchGoals();
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow space-y-6">
      <h2 className="text-white text-xl font-bold">Manage Financial Goals</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {["name", "target_amount", "current_amount", "deadline"].map((field) => (
          <input
            key={field}
            name={field}
            type={field.includes("amount") ? "number" : "text"}
            placeholder={field.replace("_", " ").toUpperCase()}
            value={newGoal[field]}
            onChange={handleInputChange}
            className="px-3 py-2 rounded bg-gray-700 text-white"
          />
        ))}
        <select
          name="priority"
          value={newGoal.priority}
          onChange={handleInputChange}
          className="px-3 py-2 rounded bg-gray-700 text-white"
        >
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
        <button
          onClick={handleAddGoal}
          className="col-span-full bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white font-semibold"
        >
          Add Goal
        </button>
      </div>

      <ul className="divide-y divide-gray-700 mt-6">
        {goals.map((goal) => (
          <li key={goal.name} className="py-3 flex justify-between items-center">
            <div className="text-white">
              <div className="font-bold">{goal.name}</div>
              <div className="text-sm text-gray-400">
                ${goal.current_amount} / ${goal.target_amount} by {goal.deadline} ({goal.priority})
              </div>
            </div>
            <button
              onClick={() => handleDeleteGoal(goal.name)}
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
