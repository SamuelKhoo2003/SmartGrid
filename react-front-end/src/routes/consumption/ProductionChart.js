import React from 'react';
import { Line } from 'react-chartjs-2';

const ProductionChart = ({ data }) => {
  const chartOptions = {
    maintainAspectRatio: true, // Ensures the chart can grow to full width and height
    scales: {
      x: {
        title: {
          display: true,
          text:'Days',
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
          text:'Energy Produced (J)',
          color: 'white', // X axis title color
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
    data ? (
      <div className="w-full h-full flex justify-center items-center">
        <Line data={data} options={chartOptions}/>
      </div>
    ) : (
      <p className="text-white">Loading production data...</p>
    )
  );
};

export default ProductionChart;
