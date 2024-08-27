import React, { useEffect } from 'react';
import './stayTuned.css'; // Make sure to create and import this CSS file

const StayTuned = () => {
  useEffect(() => {
    document.title = 'Alert | Smart Grid';
  }, []);
  
  return (
    <main className="stay-tuned-container">
      <div className="stay-tuned-content">
        <h1 className="stay-tuned-title">Stay Tuned</h1>
        <p className="stay-tuned-text">Exciting things are coming soon!</p>
        <a href="/" className="home-link">Go back home</a>
      </div>
    </main>
  );
};

export default StayTuned;
