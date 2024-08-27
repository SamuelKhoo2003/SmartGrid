import React from 'react';
import Speedometer from 'react-d3-speedometer';

const EarningsSpeedometer = ({ average7Days, average30Days }) => {
    // Function to determine speedometer value based on percentage difference
    const getSpeedometerValue = () => {
      if (average30Days === 0) return 50; // Handle division by zero case if average30Days is zero
      // Calculate percentage difference
      const percentageDifference = ((average7Days - average30Days) / average30Days) * 100;
      // Normalize value to fit within 0-100 range
      const normalizedValue = 50 + (percentageDifference / 2); // Offset to center at 50 and scale to 100
      return Math.max(0, Math.min(100, normalizedValue)); // Ensure value is within 0-100
    };

  // Format numbers to 2 decimal places
  const formatNumber = (number) => {
    return number.toFixed(2);
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <Speedometer
          value={getSpeedometerValue()}
          minValue={0}
          maxValue={100}
          needleColor="white"
          startColor="green"
          segments={7}
          endColor="red"
          height={200}
          ringWidth={30} // Adjust ring width for appearance
          needleTransitionDuration={2000} // Example transition duration
          valueFormat="d" // Remove value label
          valueTextFontSize='0' // Remove value text
          labelFontSize="0" // Remove labels completely
        />
      </div>
      <div style={{ display: 'flex', justifyContent: 'center'}}>
        <div style={{ marginRight: '20px' }}>
          <p>Monthly Day Average</p>
          <p className="font-bold">{formatNumber(average30Days)}</p>
        </div>
        <div>
          <p>Weekly Day Average</p>
          <p className="font-bold">{formatNumber(average7Days)}</p>
        </div>
      </div>
      <p style={{ marginTop: '10px' }}>
        Currently <span style={average7Days > average30Days ? { fontWeight: 'bold', color: 'rgba(255, 102, 102, 0.8)' } : average7Days < average30Days ? { fontWeight: 'bold', color: 'rgba(102, 255, 102, 0.8)' } : { fontWeight: 'bold', color: 'rgba(192, 192, 192, 0.8)' }}>
          {average7Days > average30Days ? 'Above' : average7Days < average30Days ? 'Below' : 'Equal to'}
        </span> Monthly Average
      </p>
    </div>
  );
};

export default EarningsSpeedometer;
