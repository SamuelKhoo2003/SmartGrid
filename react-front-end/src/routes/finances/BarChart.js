import React from 'react';
import { Bar } from 'react-chartjs-2';

const BarChart = ({ data }) => {
  const chartOptions = {
    maintainAspectRatio: true, // Ensures the chart can grow to full width and height
    scales: {
      x: {
        title: {
          display: true,
          text: 'Days', // X axis title
          color: 'white', // X axis title color
          font: {
            weight: 'bold', // Make the title bold
          },
        },
        ticks: {
          color: 'white', // X axis ticks color
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)', // X axis grid lines color
        },
      },
      y: {
        title: {
          display: true,
          text: 'Costs ($)', // Y axis title
          color: 'white', // Y axis title color
          font: {
            weight: 'bold', // Make the title bold
          },
        },
        ticks: {
          color: 'white', // Y axis ticks color
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)', // Y axis grid lines color
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          color: 'white', // Legend label color
        },
      },
    },
  };

  return (
    <div className="chart-container">
      {data ? <Bar data={data} options={chartOptions} /> : <p>Loading earnings data...</p>}
    </div>
  );
};

export default BarChart;
