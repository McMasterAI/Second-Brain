import React, { useState, useEffect } from 'react';
import './navbar.css';

function Navbar() {


  const [activeSection, setActiveSection] = useState(null);

  useEffect(() => {
    const handleScroll = () => {
      const sections = document.querySelectorAll('section');
      const navLinks = document.querySelectorAll('header nav a');

      sections.forEach(sec => {
        const top = window.scrollY;
        const offset = sec.offsetTop - 150;
        const height = sec.offsetHeight;
        const id = sec.getAttribute('id');

        if (top >= offset && top < offset + height) {
          setActiveSection(id);
        }
      });

      navLinks.forEach(link => {
        const linkId = link.getAttribute('href').substring(1); // Remove leading '#'
        if (linkId === activeSection) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    };

    const menuIcon = document.getElementById('menu-icon');
    const navbar = document.querySelector('header nav');

    menuIcon.onclick = () => {
      menuIcon.classList.toggle('bx-x');
      navbar.classList.toggle('active');
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [activeSection]);

  return (
    <div>
      <i className='bx bx-menu' id = "menu-icon"></i>
    <nav className="navbar">
      <a href="#home" className = "active">Home</a>
      <a href="#about" >About</a>
      <a href="#skills" >Contact Us</a>
      <a href="#projects" >Legal</a>
      <a href="#contact" >Etc</a>
    </nav>
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'/>
    </div>
  );
}

export default Navbar;