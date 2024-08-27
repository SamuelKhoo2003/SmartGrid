import React from 'react';
import { Bar } from 'react-chartjs-2';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowUp, faArrowDown, faEquals } from '@fortawesome/free-solid-svg-icons';
import './landing.css';

const TickStorage = ({ currentStorage, storageChange, historicalStorage }) => {
  const barChartData = {
    labels: Array.from({ length: 60 }, (_, i) => i),
    datasets: [
      {
        label: 'Energy Stored (J)',
        data: historicalStorage,
        backgroundColor: 'rgba(119, 221, 119, 0.6)', // Medium pastel green with some transparency
        borderColor: 'rgba(119, 221, 119, 1)', // Medium pastel green solid
        borderWidth: 1,
      },
    ],
  };

  const energyChartOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text: 'Ticks',
          color: 'white',
          font: {
            weight: 'bold',
          },
        },
        type: 'linear',
        position: 'bottom',
        min: 0,
        max: 59,
        ticks: {
          stepSize: 1,
          color: 'white',
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Energy (J)',
          color: 'white',
          font: {
            weight: 'bold',
          },
        },
        type: 'linear',
        position: 'left',
        min: 0,
        max: 50,
        ticks: {
          color: 'white',
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
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

  const currentChargePercent = (currentStorage / 50) * 100;

  const renderTrendIcon = (trend) => {
    if (trend === 'increase') {
      return <FontAwesomeIcon icon={faArrowUp} className="increase-icon" />;
    } else if (trend === 'decrease') {
      return <FontAwesomeIcon icon={faArrowDown} className="decrease-icon" />;
    } else if (trend === 'equal') {
      return <FontAwesomeIcon icon={faEquals} className="equal-icon" />;
    }
    return null;
  };

  const trend = storageChange > 0 ? 'increase' : storageChange < 0 ? 'decrease' : 'equal';

  return (
    <div className="w-full flex justify-center mt-10">
      <div className="bg-gray-500 bg-opacity-50 p-7 rounded-lg shadow-lg w-11/12 flex items-center">
        <div className="w-full flex-2 flex-col items-center">
          <Bar data={barChartData} options={energyChartOptions} />
        </div>
        <div className="w-full mb-8 flex-1 flex-col items-center ml-6">
          <h2 className="storage-title font-semibold mb-7">Storage Insight</h2>
          <div className="circular-progress-container mb-8" style={{ width: 300, height: 300 }}>
          <CircularProgressbar
            value={currentStorage}
            maxValue={50}
            text={`${currentStorage.toFixed(2)} J`}
            styles={buildStyles({
              textSize: '12px',
              pathColor: `rgba(57, 255, 20, ${currentStorage / 50})`, // Neon green color
              textColor: '#fff',
              fontWeight: 'bold', // Make the text bold
              trailColor: '#333', // Darker grey trail color
            })}
          />
          </div>
          <div className="storage-info shadow-2xl">
            <p className="text-lg text-gray-800">
              Current Charge: <span className="font-bold">{currentChargePercent.toFixed(1)}%</span>
            </p>
            <p className="text-lg text-gray-800">
              Tick Changes: <span className={`${storageChange > 0 ? 'text-green-500' : storageChange < 0 ? 'text-red-500' : 'text-gray-600'} font-bold`}>
                {storageChange.toFixed(2)} J {renderTrendIcon(trend)}
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TickStorage;
