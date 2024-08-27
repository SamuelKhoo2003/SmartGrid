import React from 'react';

const WeeklyEarnings = ({ earnings }) => (
  <div className="earnings-counter bg-gray-800 p-6 rounded-lg shadow-lg text-center text-white">
    <h2 className="text-xl font-semibold mb-4">Weekly Costs:</h2>
    <p className="text-4xl font-bold">${earnings.toFixed(2)}</p>
  </div>
);

export default WeeklyEarnings;
