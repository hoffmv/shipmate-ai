import React from "react";
import {
  ArrowDownIcon,
  ArrowUpIcon,
  PlusCircleIcon,
  CreditCardIcon,
  ShieldCheckIcon,
} from "@heroicons/react/24/outline";

const dummyData = {
  spend: {
    title: "Total Spend",
    amount: "$2,450",
    change: "-3.2%",
    positive: false,
  },
  savings: {
    title: "Savings",
    amount: "$8,900",
    change: "+1.8%",
    positive: true,
  },
  bills: [
    {
      name: "Utilities",
      due: "2024-07-10",
      amount: "$120",
      icon: CreditCardIcon,
    },
    {
      name: "Internet",
      due: "2024-07-12",
      amount: "$60",
      icon: CreditCardIcon,
    },
    {
      name: "Insurance",
      due: "2024-07-15",
      amount: "$200",
      icon: ShieldCheckIcon,
    },
  ],
  actions: [
    {
      label: "Add Expense",
      icon: PlusCircleIcon,
      color: "bg-blue-600 hover:bg-blue-700",
    },
    {
      label: "Pay Bill",
      icon: CreditCardIcon,
      color: "bg-green-600 hover:bg-green-700",
    },
    {
      label: "Secure Funds",
      icon: ShieldCheckIcon,
      color: "bg-gray-700 hover:bg-gray-600",
    },
  ],
};

export default function FinanceDashboard() {
  return (
    <section className="space-y-8">
      <h1 className="text-2xl font-bold text-white">Gold Digger Command</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[dummyData.spend, dummyData.savings].map((item, idx) => (
          <div
            key={idx}
            className="bg-gray-800 rounded-lg p-5 shadow flex flex-col justify-between"
          >
            <div className="flex justify-between items-center text-sm text-gray-400 uppercase">
              <span>{item.title}</span>
              <span
                className={`flex items-center ${
                  item.positive ? "text-green-400" : "text-red-400"
                }`}
              >
                <span className="inline-flex items-center justify-center w-4 h-4 mr-1">
                  {item.positive ? (
                    <ArrowUpIcon className="w-4 h-4" />
                  ) : (
                    <ArrowDownIcon className="w-4 h-4" />
                  )}
                </span>
                {item.change}
              </span>
            </div>
            <div className="mt-4 text-3xl font-bold text-white">{item.amount}</div>
          </div>
        ))}

        {/* Actions */}
        <div className="bg-gray-800 rounded-lg p-5 shadow">
          <span className="text-sm uppercase text-gray-400 mb-3 block">
            Quick Actions
          </span>
          <div className="flex flex-col space-y-3 md:space-y-0 md:flex-row md:space-x-3">
            {dummyData.actions.map((action) => (
              <button
                key={action.label}
                className={`flex items-center justify-center px-4 py-3 rounded-md ${action.color} text-white font-medium space-x-2`}
              >
                <span className="inline-flex w-5 h-5">
                  <action.icon className="w-5 h-5" />
                </span>
                <span>{action.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Upcoming Bills */}
      <div className="bg-gray-800 rounded-lg p-5 shadow">
        <div className="flex justify-between items-center mb-4">
          <span className="text-sm uppercase text-gray-400">Upcoming Bills</span>
          <button className="text-blue-500 text-sm hover:underline">
            View All
          </button>
        </div>
        <ul className="divide-y divide-gray-700">
          {dummyData.bills.map((bill) => (
            <li key={bill.name} className="flex items-center py-3">
              <div className="bg-gray-700 p-2 rounded-full mr-4 w-8 h-8 flex items-center justify-center">
                <bill.icon className="h-5 w-5 text-blue-400" />
              </div>
              <div className="flex-1">
                <div className="text-white font-medium">{bill.name}</div>
                <div className="text-sm text-gray-400">Due {bill.due}</div>
              </div>
              <div className="text-lg font-semibold text-white">
                {bill.amount}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
