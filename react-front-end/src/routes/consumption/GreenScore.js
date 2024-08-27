import React from 'react';

const getColorForScore = (score) => {
  if (score === 'N/A') return 'white'; // Handle the case for no data

  // Define lighter pastel color segments
  const colors = [
    { score: 0, color: [255, 75, 75] },    // (Lighter Pastel Red)
    { score: 25, color: [255, 150, 50] },   // (Lighter Pastel Orange)
    { score: 50, color: [255, 255, 75] },   // (Lighter Pastel Yellow)
    { score: 75, color: [180, 255, 100] },   // (Lighter Pastel Light Green)
    { score: 100, color: [0, 204, 102] },  // (Lighter Pastel Dark Green)
  ];

  // Find the two colors to interpolate between
  let lower, upper;
  for (let i = 0; i < colors.length - 1; i++) {
    if (score >= colors[i].score && score <= colors[i + 1].score) {
      lower = colors[i];
      upper = colors[i + 1];
      break;
    }
  }

  // Interpolate between the two colors
  const range = upper.score - lower.score;
  const rangeRatio = (score - lower.score) / range;
  const color = lower.color.map((start, index) => {
    const end = upper.color[index];
    return Math.round(start + rangeRatio * (end - start));
  });

  return `rgb(${color.join(',')})`;
};

const GreenScore = ({ score }) => {
  const scoreColor = getColorForScore(score);

  return (
    <div className="w-7/8 text-white ml-10 flex flex-row items-center justify-start">
      <div className="flex flex-col items-center justify-start mr-8">
        {/* <h2 className="text-2xl mb-2 font-semibold">Score:</h2> */}
        <h2 className="text-6xl font-bold" style={{ color: scoreColor }}>
          {score}
        </h2>
      </div>
      <div className="text-left ml-12">
        <h2 className="text-xl font-semibold mb-2 italic">What is the Green Score?</h2>
        <p className="italic text-sm">
          "The Green Score is a ranking system from 0 to 100 that evaluates your energy efficiency based on your daily energy usage.
          It compares your current day's energy consumption with the data from previous days. A score of 100 indicates the most
          efficient energy usage day, while a score of 0 reflects the highest energy consumption. This helps you understand your
          energy usage patterns and encourages more efficient energy habits."
        </p>
      </div>
    </div>
  );
};

export default GreenScore;
