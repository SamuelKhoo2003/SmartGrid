import React from 'react';
import { Bar, Line } from 'react-chartjs-2';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretUp, faCaretDown, faEquals } from '@fortawesome/free-solid-svg-icons';
import './landing.css';

const TickAlgo = ({ currNaiveCosts, currOptimalCosts, naiveCosts, optimalCosts, storageCosts, naiveCostPerTick, optimalCostPerTick, storageCostPerTick }) => {
  const barChartData = {
    labels: ['Methods'],
    datasets: [
      {
        label: 'Naive',
        data: [currNaiveCosts],
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
      {
        label: 'Optimal',
        data: [currOptimalCosts],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const barChartOptions = {
    maintainAspectRatio: false, // Corrected option to disable aspect ratio
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Current Tick Cost ($)',
          color: 'white',
          font: {
            weight: 'bold',
          },
        },
        ticks: {
          stepSize: 1,
          color: 'white',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Methods',
          color: 'white',
          font: {
            weight: 'bold',
          },
        },
        ticks: {
          display: false,
          color: 'white',
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          color: 'white',
        },
      },
    },
  };

  const lineChartData = {
    labels: Array.from({ length: 60 }, (_, i) => i), // Labels for ticks 0-59
    datasets: [
      {
        label: 'Naive Costs',
        data: naiveCostPerTick,
        fill: true,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        tension: 0.4,
      },
      {
        label: 'Optimal Costs',
        data: optimalCostPerTick,
        fill: true,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        tension: 0.4,
      },
      {
        label: 'Optimal Costs + Potential Storage Sales',
        data: storageCostPerTick,
        fill: true,
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 2,
        tension: 0.4,
      },
    ],
  };

  const lineChartOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text:'Ticks',
          color: 'white', // X axis title color
          font: {
            weight: 'bold', // Make the title bold
          },
        },
        ticks: {
          color: 'white', // X axis ticks color
        },
      },
      y: {
        title: {
          display: true,
          text:'Costs ($)',
          color: 'white', // X axis title color
          font: {
            weight: 'bold', // Make the title bold
          },
        },
        ticks: {
          color: 'white', // Y axis ticks color
        },
      },
    },
    plugins:{
      legend: {
        labels: {
          color: 'white',
        },
      },
    },
  };

  const performanceComparison = currNaiveCosts - currOptimalCosts;

  let iconComponent = null;
  if (performanceComparison > 0) {
    iconComponent = <FontAwesomeIcon icon={faCaretUp} className="increase-icon fa-xl" />;
  } else if (performanceComparison < 0) {
    iconComponent = <FontAwesomeIcon icon={faCaretDown} className="decrease-icon fa-xl" />;
  } else {
    iconComponent = <FontAwesomeIcon icon={faEquals} className="equal-icon fa-xl" />;
  }
  
  let textColorClass = '';
  if (performanceComparison > 0) {
    textColorClass = 'text-green-500';
  } else if (performanceComparison < 0) {
    textColorClass = 'text-red-500';
  } else {
    textColorClass = 'text-gray-300';
  }
  
  return (
<div className="w-full flex flex-col items-center mt-10">
      <div className="bg-gray-500 bg-opacity-50 p-7 rounded-lg shadow-lg w-11/12 flex flex-col items-center">
        <div className="w-full flex items-center">
          <div className="w-full h-full flex-1">
            <h2 className="text-2xl font-semibold text-white text-center mb-4 ml-4">Cost Comparison</h2>
            <div className="w-full flex items-center justify-center">
              <Bar data={barChartData} options={barChartOptions} style={{height: '400px', width: '300px'}}/>
            </div>
            <div className="w-full flex flex-col items-center mt-3">
              <div className="total-action-bubble bg-gray-800 p-6 rounded-xl shadow-2xl text-center text-white ml-3">
                <p className="mb-1">Current Cost Difference:</p>
                <span className={`text-xl font-bold mb-2 ${textColorClass}`}>
                  {performanceComparison > 0 ? `+${performanceComparison.toFixed(2)}` : performanceComparison.toFixed(2)}
                </span>
                <span className="ml-2">{iconComponent}</span>
              </div>
            </div>
          </div>
          <div className="w-full flex-3 ml-4">
            <Line data={lineChartData} options={lineChartOptions} />
          </div>
        </div>
        <div className="algo-info shadow-2xl mt-5 flex justify-between space-x-5">
          <p className="text-lg text-gray-800">
            Total Naive Cost: <span className="font-bold">${naiveCosts.toFixed(2)}</span>
          </p>
          <p className="text-lg text-gray-800">
            Total Optimal Cost: <span className="font-bold">${optimalCosts.toFixed(2)}</span>
          </p>
          <p className="text-lg text-gray-800">
            Total Optimal Cost combined with Storage Sales: <span className="font-bold">${storageCosts.toFixed(2)}</span>
          </p>
        </div>
        <p className="italic text-sm items-center mt-5">
          "A positive cost is the amount paid by the user, while a negative cost indicates a profit that is accounted for the user."
        </p>
      </div>
    </div>
  );
};

export default TickAlgo;
