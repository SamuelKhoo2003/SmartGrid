import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowUp, faArrowDown } from '@fortawesome/free-solid-svg-icons';
// import './WeeklyComparison.css'; // Example CSS file for styling

const WeeklyComparison = ({ comparison }) => {
  const formatDifference = (value) => {
    return value.toFixed(2);
  };

  const renderTrendIcon = (trend) => {
    if (trend === 'increase') {
      return <FontAwesomeIcon icon={faArrowUp} className="increase-icon" />;
    } else if (trend === 'decrease') {
      return <FontAwesomeIcon icon={faArrowDown} className="decrease-icon" />;
    }
    return null;
  };

  return (
    <div className="weekly-comparison">
      <h2 className="comparison-title">Weekly Comparison</h2>
      <div className="comparison-item">
        <div className="comparison-label">Energy Bought:</div>
        <div className="comparison-value">
          {formatDifference(comparison.energyBought.difference)} J {renderTrendIcon(comparison.energyBought.trend)}
        </div>
      </div>
      <div className="comparison-item">
        <div className="comparison-label">Energy Sold:</div>
        <div className="comparison-value">
          {formatDifference(comparison.energySold.difference)} J {renderTrendIcon(comparison.energySold.trend)}
        </div>
      </div>
      <div className="comparison-item">
        <div className="comparison-label">Costs:</div>
        <div className="comparison-value">
          ${formatDifference(comparison.earnings.difference)} {renderTrendIcon(comparison.earnings.trend)}
        </div>
      </div>
    </div>
  );
};

export default WeeklyComparison;
