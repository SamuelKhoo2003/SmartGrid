import React from 'react';
import ReactSpeedometer from 'react-d3-speedometer';
import './landing.css'
// possible can add total bought and sold for the day, so like a widget similar to weekly cost that is total bought and total sold
// EXTENSION TO DO
const TickBuySell = ({ currentAction, actionLog, totalBought, totalSold}) => {
  let speedometerValue;

  if (currentAction === 'BUY') {
    speedometerValue = Math.floor(Math.random() * (90 - 70 + 1)) + 70; // Random number between 70 and 90 for 'buy'
  } else if (currentAction === 'SELL') {
    speedometerValue = Math.floor(Math.random() * (30 - 10 + 1)) + 10; // Random number between 10 and 30 for 'sell'
  } else {
    speedometerValue = 50;
  }

  return (
    <div className="w-full flex items-center justify-center mt-10">
      <div className="bg-gray-500 bg-opacity-50 p-7 rounded-lg shadow-lg w-11/12 flex items-center justify-center">
        <div className="flex-1 items-center">
          <div className="total-action-bubble bg-gray-800 p-6 rounded-xl shadow-2xl text-center text-white mr-6">
            <p className="text-xl mb-1">Daily Energy Bought:</p>
            <p className="text-4xl font-bold mb-6">{totalBought.toFixed(2)} J</p>
            <p className="text-xl mb-1">Daily Energy Sold:</p>
            <p className="text-4xl font-bold">{totalSold.toFixed(2)} J</p>
          </div>
        </div>
        <div className="flex flex-col items-center">
          {/* Speedometer and Current Action */}
            <ReactSpeedometer
              maxValue={100}
              value={speedometerValue}
              needleColor="white"
              startColor='red'
              segments={9}
              endColor='green'
              textColor="white"
              currentValueText={currentAction}
              ringWidth={20} // Adjust ring width for a smoother appearance
              needleTransitionDuration={4000} // Adjust transition duration as needed
              needleTransition="easeElastic" // Use easeElastic for a smoother needle transition
              needleHeightRatio={0.7} // Adjust needle height ratio for better visibility
              needleBaseColor="white" // Base color of the needle
              needleBorderColor="white" // Needle border color
              needleThickness={3} // Adjust needle thickness
              labelFontSize="0px" // Hide labels
              valueTextFontSize="0px" // Hide value text
              height={180}
            />
          <div className="text-xl text-white text-center">
            Current Action: <span className={`${currentAction === 'SELL' ? 'text-red-500 font-bold' : currentAction === 'BUY' ? 'text-green-500 font-bold' : 'text-yellow-500 font-bold'}`}>
              {currentAction}
            </span>
          </div>
        </div>
        {/* Action Log */}
        <div className="flex-1 bg-gray-200 p-5 rounded-lg shadow-2xl ml-8 action-log">
          <h3 className="action-log-title">Action Log</h3>
          <ul className="overflow-y-auto max-h-40 list-none p-0">
            {actionLog
              .slice()
              .reverse()
              .map((log, index) => (
                <li key={index} className="action-log-item">
                  <span className="action-log-label">Tick {log.tick}</span>
                  <span className={`action-log-value ${log.action === 'BUY' ? 'text-green-500 font-bold' : log.action === 'SELL' ? 'text-red-500 font-bold' : 'text-yellow-500 font-bold'}`}>
                    {log.action}: <span className="text-gray-400">{log.value.toFixed(2)} J</span>
                  </span>
                </li>
              ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TickBuySell;
