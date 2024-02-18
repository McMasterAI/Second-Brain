import React from 'react';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      
      <ul className="list">
        <li>
          <a href="#">FAQ</a>
        </li>
        <li>
          <a href="#">Services</a>
        </li>
        <li>
          <a href="#about">About Us</a>
        </li>
        <li>
          <a href="#contact">Contact Us</a>
        </li>
        <li>
          <a href="#">Privacy Policy</a>
        </li>
      </ul>
      <p className="copyright">
        © Second Brain For Students | All Rights Reserved
      </p>
    </footer>
  );
}

export default Footer;
