import React from 'react';
import logo from '../assets/renewable-energy.png';
import { Link, NavLink } from 'react-router-dom';
import { ResetLocation } from '../helpers/reset-location.js';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBell } from '@fortawesome/free-regular-svg-icons';
import './navbar.css';

const Navbar = () => {
  return (
    <header>
      <nav className="navbar h-20 w-full text-white flex items-center px-4">
        <NavLink
          onClick={(event) => {
            // event.preventDefault(); // Prevent default navigation behavior
            ResetLocation();
            const logoElement = document.querySelector('.logo');
            logoElement.classList.add('spin-once-animation');
            setTimeout(() => {
              logoElement.classList.remove('spin-once-animation');
            }, 1000); // Adjust the timeout to match the animation duration

          }}
          to="/"
          className="flex items-center space-x-3"
        >
          <img
            width="50"
            height="50"
            className="logo"
            src={logo}
            alt="Sun Logo"
          />
          <h1 className="text-xl font-bold hover:text-gray-300">
            <span>Smart Grid</span>
          </h1>
        </NavLink>

        <ul className="flex space-x-6 ml-auto">
          <li>
            <Link to="/" className="text-lg font-semibold hover:text-gray-300">
              Home
            </Link>
          </li>
          <li>
            <Link to="/finances" className="text-lg font-semibold hover:text-gray-300">
              Finances
            </Link>
          </li>
          <li>
            <Link to="/consumption" className="text-lg font-semibold hover:text-gray-300">
              Consumption
            </Link>
          </li>
          <li>
            <Link to="/about" className="text-lg font-semibold hover:text-gray-300">
              About
            </Link>
          </li>
          <li>
            <Link to="/alert">
              <FontAwesomeIcon icon={faBell} className="bell-icon" />
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;
