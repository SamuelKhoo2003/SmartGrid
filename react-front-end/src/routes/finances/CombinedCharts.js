import React from 'react';
import { Line, Pie } from 'react-chartjs-2';

const CombinedCharts = ({ lineChartData, pieChartData }) => {
  const lineChartOptions = {
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
          text:'Energy (J)',
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

  const pieChartOptions = {
    maintainAspectRatio: true, // Ensures the chart can grow to full width and height
    plugins: {
      title: {
        display: true,
        text: 'Weekly Insight', // Title for the Pie chart
        color: 'white', // Title color
        font: {
          size: 20, // Title font size
          weight: 'bold', // Title font weight
        },
      },
      legend: {
        labels: {
          color: 'white', // Legend label color
        },
      },
    },
  };

  return (
    <div className="flex flex-wrap">
      <div className="w-full md:w-3/4 p-4">
        <div className="chart-container">
          {lineChartData ? <Line data={lineChartData} options={lineChartOptions} /> : <p>Loading line chart data...</p>}
        </div>
      </div>
      <div className="w-full md:w-1/4 p-4 flex justify-center items-center mb-4">
        <div className="pie-container">
          {pieChartData ? <Pie data={pieChartData} options={pieChartOptions} /> : <p>Loading pie chart data...</p>}
          <div className="mt-4 text-white text-center">
                <p>Sold: <span style={{ color: 'rgba(123, 201, 134, 1)', fontWeight: 'bold' }}>{pieChartData.datasets[0].data[1].toFixed(2)}</span></p>
                <p>Bought: <span style={{ color: 'rgba(107, 174, 214, 1)', fontWeight: 'bold' }}>{pieChartData.datasets[0].data[0].toFixed(2)}</span></p>
              </div>
        </div>
      </div>
    </div>
  );
};

export default CombinedCharts;
