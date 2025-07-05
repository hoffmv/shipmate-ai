import React from 'react';

const Topbar = () => {
  return (
    <div className="flex justify-between items-center px-4 py-2 bg-[#2f3c6c] text-white">
      <div className="text-lg font-semibold">Shipmate AI Command</div>
      <div className="flex items-center gap-4 text-sm">
        <button className="hover:underline">Settings</button>
        <button className="hover:underline">Logout</button>
        <img
          src="/avatar.png"
          alt="User Avatar"
          className="w-8 h-8 rounded-full border border-white"
        />
      </div>
    </div>
  );
};

export default Topbar;
