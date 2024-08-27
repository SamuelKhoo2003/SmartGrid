
// EXPERIMENT WITH MAKING IT LINE INSTEAD OF SCATTER

import React, { useEffect, useState } from 'react';
import EnergySavingTip from './EnergySavingTip';
import TickEnergy from './TickEnergy';
import TickBuySell from './TickBuySell';
import TickStorage from './TickStorage';
import TickAlgo from './TickAlgo';
import ExternalInfo from '../../assets/ExternalInfo.json';
import './landing.css';

const Home = () => {
  const [energyUsage, setEnergyUsage] = useState(0);
  const [energyProduced, setEnergyProduced] = useState(0);

  const [chartData, setChartData] = useState({
    labels: Array.from({ length: 60 }, (_, i) => i),
    datasets: [
      {
        label: 'Energy Usage (J)',
        data: Array.from({ length: 60 }, (_, i) => ({ x: i, y: null })),
        borderColor: 'rgba(255, 51, 153, 1)',
        backgroundColor: 'rgba(255, 51, 153, 0.2)',
        pointBackgroundColor: 'rgba(255, 51, 153, 0.8)',
        pointBorderColor: 'rgba(255, 51, 153, 0.6)',
      },
      {
        label: 'Energy Usage Without Deferrables (J)',
        data: Array.from({ length: 60 }, (_, i) => ({ x: i, y: null })),
        borderColor: 'rgba(51, 255, 51, 1)',
        backgroundColor: 'rgba(51, 255, 51, 0.2)',
        pointBackgroundColor: 'rgba(51, 255, 51, 0.8)',
        pointBorderColor: 'rgba(51, 255, 51, 0.6)',
      },
      {
        label: 'Energy Produced (J)',
        data: Array.from({ length: 60 }, (_, i) => ({ x: i, y: null })),
        borderColor: 'rgba(51, 153, 255, 1)',
        backgroundColor: 'rgba(51, 153, 255, 0.2)',
        pointBackgroundColor: 'rgba(51, 153, 255, 0.8)',
        pointBorderColor: 'rgba(51, 153, 255, 0.6)',
      }
    ],
  }); 

  const [currentAction, setCurrentAction] = useState('BUY');
  const [actionLog, setActionLog] = useState([]);
  const [currentStorage, setCurrentStorage] = useState(0);
  const [storageChange, setStorageChange] = useState(0);
  const [historicalStorage, setHistoricalStorage] = useState(Array.from({ length: 60 }, () => 0));

  const [naiveCosts, setNaiveCosts] = useState(0);
  const [optimalCosts, setOptimalCosts] = useState(0);
  const [storageCosts, setStorageCosts] = useState(0);
  const [currNaiveCosts, setCurrNaiveCosts] = useState(0);
  const [currOptimalCosts, setCurrOptimalCosts] = useState(0);
  const [naiveCostPerTick, setNaiveCostPerTick] = useState(Array.from({ length: 60 }, () => 0));
  const [optimalCostPerTick, setOptimalCostPerTick] = useState(Array.from({ length: 60 }, () => 0));
  const [storageCostPerTick, setStorageCostPerTick] = useState(Array.from({ length: 60 }, () => 0));

  const [totalBought, setTotalBought] = useState(0);
  const [totalSold, setTotalSold] = useState(0);

  useEffect(() => {
    document.title = 'Home | Energy Dashboard';
    const fetchData = async () => {
      const data = ExternalInfo;

      // initial assignments
      let newUsageData = Array.from({ length: 60 }, (_, i) => ({ x: i, y: null }));
      let newEnergyUsageWithoutDef = Array.from({ length: 60 }, (_, i) => ({ x: i, y: null }));
      let newProducedData = Array.from({ length: 60 }, (_, i) => ({ x: i, y: null }));
      let newHistoricalStorage = Array.from({ length: 60 }, () => 0);

      let naiveCostSum = 0;
      let optimalCostSum = 0;
      let storageCostSum = 0;
      let newNaiveCostPerTick = Array.from({ length: 60 }, () => 0);
      let newOptimalCostPerTick = Array.from({ length: 60 }, () => 0);
      let newStorageCostPerTick = Array.from({ length: 60 }, () => 0);

      let newActionLog = [];
      let totalBought = 0;
      let totalSold = 0;

      let latestTick = 0;

      Object.keys(data).forEach(key => {
        if (data[key].length > 0) {
          const tickData = data[key][0];
          newUsageData[key] = { x: key, y: tickData.energyUsed };
          newEnergyUsageWithoutDef[key] = { x: key, y: tickData.noDefEnergyUsed };
          newProducedData[key] = { x: key, y: tickData.energyIn };
          newHistoricalStorage[key] = tickData.storage;

          naiveCostSum += tickData.naiveProfit;
          optimalCostSum += tickData.optProfit;
          storageCostSum += tickData.storageProfit;
          newNaiveCostPerTick[key] = naiveCostSum;
          newOptimalCostPerTick[key] = optimalCostSum;
          newStorageCostPerTick[key] = storageCostSum;

          let action = tickData.energyTransaction > 0 ? 'BUY' : tickData.energyTransaction < 0 ? 'SELL' : 'N/A';
          newActionLog.push({
            tick: key,
            action: action,
            value: Math.abs(tickData.energyTransaction)
          });

          if (action === 'BUY') {
            totalBought += Math.abs(tickData.energyTransaction);
          } else if (action === 'SELL') {
            totalSold += Math.abs(tickData.energyTransaction);
          }

          latestTick = Math.max(latestTick, key);
        }
      });
  
      setEnergyUsage(newUsageData[latestTick]?.y ?? 0);
      setEnergyProduced(newProducedData[latestTick]?.y ?? 0);
      setChartData(prevData => ({
        ...prevData,
        datasets: [
          {
            ...prevData.datasets[0],
            data: newUsageData,
          },
          {
            ...prevData.datasets[1],
            data: newEnergyUsageWithoutDef,
          },
          {
            ...prevData.datasets[2],
            data: newProducedData,
          }
        ],
      }));

      setCurrentStorage(data[latestTick]?.[0]?.storage ?? 0);
      setStorageChange(newHistoricalStorage[latestTick] - newHistoricalStorage[latestTick - 1] ?? 0);
      setHistoricalStorage(newHistoricalStorage);


      setNaiveCosts(naiveCostSum);
      setOptimalCosts(optimalCostSum);
      setStorageCosts(storageCostSum);
      setCurrNaiveCosts(data[latestTick]?.[0]?.naiveProfit.toFixed(2) ?? 0);
      setCurrOptimalCosts(data[latestTick]?.[0]?.optProfit.toFixed(2) ?? 0);
      setNaiveCostPerTick(newNaiveCostPerTick);
      setOptimalCostPerTick(newOptimalCostPerTick);
      setStorageCostPerTick(newStorageCostPerTick);

      // console.log(newActionLog[newActionLog.length - 1]?.action)
      // SO MUCH DEBUGGING OVER THIS AS ARRAY LENGTH NON MATCH

      setActionLog(newActionLog);
      setCurrentAction(newActionLog[newActionLog.length - 1]?.action);

      setTotalBought(totalBought);
      setTotalSold(totalSold);
    };
    fetchData();
  }, []);
  

  const scrollToContent = () => {
    const contentSection = document.getElementById('content-section');
    contentSection.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="w-full min-h-screen flex flex-col items-center justify-center">
        <h1 className="text-5xl text-white">Welcome To Your Dashboard</h1>
        <EnergySavingTip />
        <div className="flex flex-col items-center">
          <button onClick={scrollToContent} className="text-white text-xl focus:outline-none hover:scale-110">
            <svg className="w-10 h-10 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </button>
        </div>
      </div>
      <div id="content-section" className="w-full flex flex-col items-center justify-center py-10">
        <div className="w-full mt-8">
          <TickEnergy energyUsage={energyUsage.toFixed(2)} energyProduced={energyProduced.toFixed(2)} chartData={chartData} />
        </div>
        <div className="w-full mt-8">
            <TickStorage currentStorage={currentStorage} storageChange={storageChange} historicalStorage={historicalStorage} />
        </div>
        <div className="w-full mt-8">
            <TickBuySell currentAction={currentAction} actionLog={actionLog} totalBought={totalBought} totalSold={totalSold} />
        </div>
        <div className="w-full mt-8">
          <TickAlgo
          currNaiveCosts={currNaiveCosts}
          currOptimalCosts={currOptimalCosts}
          naiveCosts={naiveCosts}
          optimalCosts={optimalCosts}
          storageCosts={storageCosts}
          naiveCostPerTick={naiveCostPerTick}
          optimalCostPerTick={optimalCostPerTick}
          storageCostPerTick={storageCostPerTick}/>
        </div>
      </div>
    </div>
  );
};

export default Home;
