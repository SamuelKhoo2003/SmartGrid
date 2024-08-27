import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FilterButtons from '../../helpers/FilterButtons';
import BarChart from './BarChart';
import CombinedCharts from './CombinedCharts';
import WeeklyEarnings from './WeeklyEarnings';
import WeeklyComparison from './WeeklyComparison';
import EarningsSpeedometer from './EarningsSpeedometer'; // Import the new component
import './finance.css';

const Finances = () => {
  const [topChartData, setTopChartData] = useState(null);
  const [bottomChartData, setBottomChartData] = useState(null);
  const [pieChartData, setPieChartData] = useState(null);
  const [daysFilter, setDaysFilter] = useState(90);
  const [weeklyEarnings, setWeeklyEarnings] = useState(0);
  const [weeklyComparison, setWeeklyComparison] = useState({
    energyBought: { difference: 0, trend: '' },
    energySold: { difference: 0, trend: '' },
    earnings: { difference: 0, trend: '' },
  });
  const [average7Days, setAverage7Days] = useState(0);
  const [average30Days, setAverage30Days] = useState(0);

  const fetchData = async () => {
    try {
      const response = await axios.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessTradeLog');
      const data = response.data;

      const sortedData = data.sort((a, b) => new Date(a.dayID) - new Date(b.dayID));

      const days = sortedData.map(entry => entry.dayID);
      const energyBought = sortedData.map(entry => entry.energyBought);
      const energySold = sortedData.map(entry => entry.energySold);
      const earnings = sortedData.map(entry => -1 * entry.earnings);

      setTopChartData({
        labels: days,
        datasets: [
          {
            label: 'Energy Bought',
            data: energyBought,
            backgroundColor: 'rgba(186, 143, 235, 0.4)', // Lighter shade of pastel purple
            borderColor: 'rgba(186, 143, 235, 1)', // Slightly darker shade for border
            borderWidth: 0.75,
          },
          {
            label: 'Energy Sold',
            data: energySold,
            backgroundColor: 'rgba(255, 174, 207, 0.2)', // Light pink
            borderColor: 'rgba(255, 174, 207, 1)', // Slightly darker shade for border
            borderWidth: 0.75,
          },
        ],
      });

      setBottomChartData({
        labels: days,
        datasets: [
          {
            label: 'Costs',
            data: earnings,
            backgroundColor: 'rgba(255, 204, 0, 0.8)', // Warm yellow
            borderColor: 'rgba(255, 204, 0, 1)', // Slightly darker shade for border
            borderWidth: 1,
          },
        ],
      });

      const totalEnergyBought = energyBought.slice(-7).reduce((acc, curr) => acc + curr, 0);
      const totalEnergySold = energySold.slice(-7).reduce((acc, curr) => acc + curr, 0);
      setPieChartData({
        labels: ['Energy Bought', 'Energy Sold'],
        datasets: [
          {
            // data: [totalEnergySold, totalEnergyBought],
            data: [totalEnergyBought, totalEnergySold],
            backgroundColor: ['rgba(107, 174, 214, 0.6)', 'rgba(123, 201, 134, 0.6)'],
            hoverBackgroundColor: ['rgba(107, 174, 214, 1)', 'rgba(123, 201, 134, 1)'],
            borderColor: 'rgba(64, 64, 64, 1)',
            borderWidth: 1,
          },
        ],
      });

      const recentEarnings = earnings.slice(-7).reduce((acc, curr) => acc + curr, 0);
      setWeeklyEarnings(recentEarnings);

      // Calculate averages for 7 days and 30 days
      const averageEarnings7Days = recentEarnings / 7;
      const averageEarnings30Days = earnings.slice(-30).reduce((acc, curr) => acc + curr, 0) / 30;

      setAverage7Days(averageEarnings7Days);
      setAverage30Days(averageEarnings30Days);

      // Calculate weekly comparison
      const recentEnergyBought = energyBought.slice(-7).reduce((acc, curr) => acc + curr, 0);
      const previousEnergyBought = energyBought.slice(-14, -7).reduce((acc, curr) => acc + curr, 0);
      const recentEnergySold = energySold.slice(-7).reduce((acc, curr) => acc + curr, 0);
      const previousEnergySold = energySold.slice(-14, -7).reduce((acc, curr) => acc + curr, 0);
      const previousEarnings = earnings.slice(-14, -7).reduce((acc, curr) => acc + curr, 0);

      setWeeklyComparison({
        energyBought: {
          difference: recentEnergyBought - previousEnergyBought,
          trend: recentEnergyBought > previousEnergyBought ? 'increase' : 'decrease',
        },
        energySold: {
          difference: recentEnergySold - previousEnergySold,
          trend: recentEnergySold > previousEnergySold ? 'increase' : 'decrease',
        },
        earnings: {
          difference: recentEarnings - previousEarnings,
          trend: recentEarnings > previousEarnings ? 'increase' : 'decrease',
        },
      });
    } catch (error) {
      console.error('Error fetching data', error);
    }
  };

  useEffect(() => {
    document.title = 'Finances | Smart Grid';
    fetchData();
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

  const filteredTopChartData = topChartData ? filterData(topChartData, daysFilter) : null;
  const filteredBottomChartData = bottomChartData ? filterData(bottomChartData, daysFilter) : null;

  return (
    <div className="finances-container">
      <div className="w-11/12 flex justify-between items-center px-6">
        <div className="text-2xl font-semibold -mt-4">Your Finances History</div>
        <div>
          <FilterButtons daysFilter={daysFilter} handleDaysFilterChange={handleDaysFilterChange} />
        </div>
      </div>
      <div className="w-11/12 md:w-8/10 flex flex-col items-center mb-4">
        <div className="w-full flex">
          <div className="energybs-bubble bg-gray-500 bg-opacity-50 shadow-lg">
            {filteredTopChartData && pieChartData ? (
              <CombinedCharts lineChartData={filteredTopChartData} pieChartData={pieChartData} />
            ) : (
              <p>Loading chart data...</p>
            )}
          </div>
          <div className="w-4"></div>
          <div className="costs-bubble bg-gray-500 bg-opacity-50 shadow-lg flex-2">
            <WeeklyEarnings earnings={weeklyEarnings} />
            <EarningsSpeedometer average7Days={average7Days} average30Days={average30Days} />
          </div>
        </div>
        <div className="w-full flex mt-4">
          <div className="cost-chart-bubble bg-gray-500 bg-opacity-50 shadow-lg flex-1">
            <BarChart data={filteredBottomChartData} />
          </div>
          <div className="w-4"></div>
          <div className="comparison-bubble bg-gray-500 bg-opacity-50 shadow-lg flex-1">
            <WeeklyComparison comparison={weeklyComparison} />
            <div className="flex justify-center items-center ">
              <p className="italic vertical-center">
                "This section evaluates energy transactions and financial performance 
                over the past week, contrasting trends in energy bought, energy sold, and associated costs.
                It provides insights into recent changes to aid in strategic decision-making for energy 
                management and cost optimization."
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Finances;

