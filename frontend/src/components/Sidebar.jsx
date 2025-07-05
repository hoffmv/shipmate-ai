import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  const navItems = [
    { label: "Gold Digger Command", to: "/finance" },
    { label: "Casino Royale Division", to: "/trading" },
    { label: "Clipboard Warriors HQ", to: "/admin" },
    { label: "Time Lords Operations", to: "/scheduling" },
    { label: "Mouthpiece Command", to: "/comms" },
    { label: "Meat Wagon Ops", to: "/wellness" },
    { label: "Skunkworks Shenanigans", to: "/rnd" }
  ];

  return (
    <div className="w-64 h-full bg-[#202942] text-white">
      <h2 className="text-md font-semibold mb-4">Shipmate Divisions</h2>
      <ul className="space-y-2 text-sm">
        {navItems.map((item) => (
          <li key={item.to}>
            <NavLink
              to={item.to}
              className={({ isActive }) =>
                isActive
                  ? 'text-blue-400 font-semibold'
                  : 'hover:text-blue-300'
              }
            >
              {item.label}
            </NavLink>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
