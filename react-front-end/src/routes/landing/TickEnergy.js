import React from 'react';
import { Scatter } from 'react-chartjs-2';
import Speedometer from 'react-d3-speedometer';


const TickEnergy = ({ energyUsage, energyProduced, chartData }) => {
  return (
    <div className="w-full flex justify-center mt-10">
      <div className="bg-gray-500 bg-opacity-50 p-7 rounded-lg shadow-lg w-11/12 flex items-center">
        <div className="flex flex-col items-center mr-8">
          <div className="flex flex-col items-center mb-20">
            <Speedometer
              value={energyUsage}
              minValue={0}
              maxValue={20}
              needleColor="white"
              startColor="pink"
              segments={10}
              endColor="purple"
              width={300}
              height={200}
              textColor="transparent"
              labelFontSize='0'
            />
            <p className="text-lg">Current Energy Usage: <strong>{energyUsage} J</strong></p>
          </div>
          <div className="flex flex-col items-center">
            <Speedometer
              value={energyProduced}
              minValue={0}
              maxValue={5}
              needleColor="white"
              startColor="#3498db"
              segments={10}
              endColor="#2ecc71"
              width={300}
              height={200}
              textColor="transparent"
              labelFontSize='0'
            />
            <p className="text-lg">Current Energy Produced: <strong>{energyProduced} J</strong></p>
          </div>
        </div>
        <div className="w-full">
          <Scatter
            data={chartData}
            options={{
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
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default TickEnergy;
