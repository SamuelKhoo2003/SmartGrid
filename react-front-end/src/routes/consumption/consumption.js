import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UsageChart from './UsageChart';
import ProductionChart from './ProductionChart';
import GreenScore from './GreenScore';
import FilterButtons from '../../helpers/FilterButtons';
import './consumption.css';

const Consumption = () => {
  const [usageData, setUsageData] = useState(null);
  const [productionData, setProductionData] = useState(null);
  const [daysFilter, setDaysFilter] = useState(90);
  const [greenScore, setGreenScore] = useState('N/A');

  const fetchUsageData = async () => {
    try {
      const response = await axios.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessEnergyLog');
      const data = response.data;

      // Sort data by day in ascending order
      const sortedData = data.sort((a, b) => new Date(a.dayID) - new Date(b.dayID));

      const days = sortedData.map(entry => entry.dayID);
      const energyUsed = sortedData.map(entry => entry.energyUsed);

      setUsageData({
        labels: days,
        datasets: [
          {
            label: 'Energy Used',
            data: energyUsed,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
          },
        ],
      });

      // Calculate GreenScore
      if (energyUsed.length > 0) {
        const maxEnergyUsed = Math.max(...energyUsed);
        const minEnergyUsed = Math.min(...energyUsed);
        const mostRecentEnergyUsed = energyUsed[energyUsed.length - 1];
        const score = (1 - (mostRecentEnergyUsed - minEnergyUsed) / (maxEnergyUsed - minEnergyUsed)) * 100;
        setGreenScore(Math.round(score));
      }
    } catch (error) {
      console.error('Error fetching usage data', error);
    }
  };

  const fetchProductionData = async () => {
    try {
      const response = await axios.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessEnergyLog');
      const data = response.data;

      // Sort data by day in ascending order
      const sortedData = data.sort((a, b) => new Date(a.dayID) - new Date(b.dayID));

      const days = sortedData.map(entry => entry.dayID);
      const energyProduced = sortedData.map(entry => entry.energyProduced);

      setProductionData({
        labels: days,
        datasets: [
          {
            label: 'Energy Produced',
            data: energyProduced,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
          },
        ],
      });
    } catch (error) {
      console.error('Error fetching production data', error);
    }
  };

  useEffect(() => {
    document.title = 'Consumption | Smart Grid';
    fetchUsageData();
    fetchProductionData();
  }, []);

  const filterData = (data, days) => {
    const endIndex = data.labels.length;
    const startIndex = Math.max(0, endIndex - days);
    return {
      ...data,
      labels: data.labels.slice(startIndex, endIndex),
      datasets: data.datasets.map(dataset => ({
        ...dataset,
        data: dataset.data.slice(startIndex, endIndex),
      })),
    };
  };

  const handleDaysFilterChange = (days) => {
    setDaysFilter(days);
  };

  const filteredUsageData = usageData ? filterData(usageData, daysFilter) : null;
  const filteredProductionData = productionData ? filterData(productionData, daysFilter) : null;

  return (
    <div className="consumption-container">
      <div className="w-11/12 flex justify-between items-center px-6">
        <div className="text-2xl font-semibold -mt-4">Your Consumption History</div>
        <div>
          <FilterButtons daysFilter={daysFilter} handleDaysFilterChange={handleDaysFilterChange} />
        </div>
      </div>
      <div className="w-11/12 md:w-8/10 flex flex-col items-center">
        <div className="w-full flex">
          <div className="graph-bubble bg-gray-500 bg-opacity-50 shadow-lg">
            {filteredUsageData ? (
              <UsageChart data={filteredUsageData} />
            ) : (
              <p className="text-white">Loading usage data...</p>
            )}
          </div>
          <div className="w-4"></div>
          <div className="graph-bubble bg-gray-500 bg-opacity-50 shadow-lg">
            {filteredProductionData ? (
              <ProductionChart data={filteredProductionData} />
            ) : (
              <p className="text-white">Loading production data...</p>
            )}
          </div>
        </div>
        <div className="score-bubble bg-gray-500 bg-opacity-50 shadow-lg">
          <GreenScore score={greenScore} />
        </div>
      </div>
    </div>
  );
};

export default Consumption;
