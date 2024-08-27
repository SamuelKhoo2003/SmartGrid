import React, { useState } from 'react';

const EnergySavingTip = () => {
  const [energySavingTip, setEnergySavingTip] = useState('');

  // List of energy-saving tips
  const energySavingTips = [
    "Turn off lights when leaving a room to save energy.",
    "Use energy-efficient LED bulbs instead of incandescent ones to reduce electricity costs.",
    "Use a programmable thermostat to automatically adjust temperature settings and save on cooling costs.",
    "Unplug electronics and chargers when not in use to avoid phantom energy usage.",
    "Seal gaps and cracks around doors and windows to prevent air leaks and improve heating efficiency.",
    "Use appliances like dishwashers and washing machines during off-peak hours to take advantage of lower electricity rates.",
    "Install ceiling fans to improve air circulation and reduce reliance on air conditioning.",
    "Take advantage of natural light during the day to reduce the need for artificial lighting.",
    "Lower the thermostat in winter and raise it in summer to save on heating and cooling costs respectively."
  ];

  const selectRandomTip = () => {
    const randomIndex = Math.floor(Math.random() * energySavingTips.length);
    return energySavingTips[randomIndex];
  };

  useState(() => {
    setEnergySavingTip(selectRandomTip());
  }, []);

  return (
    <div className="energy-saving-tip-container">
      <p className="energy-saving-tip-text"><strong style={{ color: '#ff6600' }}>Daily Tip: </strong>{energySavingTip}</p>
    </div>
  );
};

export default EnergySavingTip;
