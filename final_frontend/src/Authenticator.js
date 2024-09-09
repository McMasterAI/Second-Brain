import './App.css';
import Login from './Login';
import App from './App';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Autheticator = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [message, setMessage] = useState(null);
  const [counter, setCounter] = useState(0);

  useEffect(() => {
    // Check if the authentication token exists in localStorage
    const token = localStorage.getItem('authToken');
    console.log(token);
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);


  const handleLogin = async (username, password, counter) => {

    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password)
  
        const response = await axios.post("http://127.0.0.1:5000/api/login", formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
  
        const msg = response.data.message;
        console.log(msg)
        if (msg === 'username_error'){
            setMessage("Username does not exist. If you just registered, please wait 10-20 seconds while your account is created.");
            setCounter(counter + 1);
        }
        else if (msg === 'password_error'){
            setMessage("Incorrect password");
            setCounter(counter + 1);
            
        }
        else {
            setIsLoggedIn(true);
            localStorage.setItem('authToken', username); // 
        }
        
      } catch (error) {
        console.error('Error submitting input:', error);
      }

  };

  const handleLogout = () => {
    // Clear authentication token from localStorage
    localStorage.removeItem('authToken');
    // Update authentication state to indicate user is logged out
    setIsLoggedIn(false);
  };

  return (
    <div className="App">
      {!isLoggedIn ? (
        <Login message={message} counter={counter} onLogin={handleLogin} />
      ) : (
        <App onLogout={handleLogout}/>
      )}
    </div>
  );
};

export default Autheticator;