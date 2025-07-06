import React, { useEffect, useState } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:5000";

export default function PaymentCalendar() {
  const [events, setEvents] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [eventsOnDate, setEventsOnDate] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/finance-calendar`)
      .then((res) => res.json())
      .then((data) => setEvents(data || []));
  }, []);

  useEffect(() => {
    const filtered = events.filter(
      (e) => e.date === selectedDate.toISOString().split("T")[0]
    );
    setEventsOnDate(filtered);
  }, [selectedDate, events]);

  return (
    <div className="p-6 bg-gray-900 text-white space-y-6">
      <h2 className="text-2xl font-bold">Cash Flow Calendar</h2>
      <Calendar
        onChange={setSelectedDate}
        value={selectedDate}
        className="bg-white text-black rounded-lg"
      />
      <div className="mt-4">
        <h3 className="text-lg font-semibold mb-2">
          Events on {selectedDate.toDateString()}
        </h3>
        {eventsOnDate.length === 0 ? (
          <p className="text-gray-400">No events for this day.</p>
        ) : (
          <ul className="space-y-2">
            {eventsOnDate.map((event, idx) => (
              <li
                key={idx}
                className="border border-gray-600 rounded p-3 bg-gray-800"
              >
                <div className="text-sm text-gray-300">{event.type.toUpperCase()}</div>
                <div className="font-bold">{event.name}</div>
                <div>${Math.abs(event.amount).toFixed(2)} — {event.account}</div>
                {event.reason && <div className="text-xs text-gray-400 italic">{event.reason}</div>}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
