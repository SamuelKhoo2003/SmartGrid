import React, { useEffect } from 'react';
import './not-found.css'; // Make sure to create and import this CSS file

const NotFound = () => {
  useEffect(() => {
    document.title = '404 | Smart Grid';
  }, []);
  
  return (
    <main className="not-found-container">
      <div className="not-found-content">
        <h1 className="not-found-title">404</h1>
        <p className="not-found-text">Page Not Found</p>
        <a href="/" className="home-link">Go back home</a>
      </div>
    </main>
  );
};

export default NotFound;
