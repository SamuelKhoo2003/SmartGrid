import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar.js';
import Home from './routes/landing/landing';
import Finances from './routes/finances/finances.js';
import Consumption from './routes/consumption/consumption.js';
import NotFound from './routes/not-found/not-found.js';
import About from './routes/about/about.js';
import './core-ui/App.css';
import StayTuned from './routes/alert/stayTuned.js';
import 'chart.js/auto';

const App = () => {
  return (
    <div className="app flex flex-col min-h-screen">
      <Navbar />
      <div className="flex-grow text-white"> {/* Change the background color */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/finances" element={<Finances />} />
          <Route path="/consumption" element={<Consumption />} />
          <Route path="/about" element={<About />} />
          <Route path="/alert" element={<StayTuned />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;
