import React, { useState, useEffect } from 'react';
import './Login.css';
import axios from 'axios';
import './App.css';

const Login = ({ onLogin, message, counter }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isRegistered, setIsRegistered] = useState(true)
  const [passCheck, setPassCheck] = useState('');
  const [registerMsg, setRegisterMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [loading1, setLoading1] = useState(false);
  const [loginMsg, setLoginMsg] = useState('');
  const [messageCounter, setMessageCounter] = useState(0);


  useEffect(() => {
    setLoading1(false);
    setLoginMsg(message);
    setMessageCounter(counter);
  }, [message, counter]);


  const handleLogin = () => {

    setLoading1(true);
    setLoginMsg('');
    onLogin(username, password, messageCounter);
  };

  const registrationButton = () => {
    setLoginMsg('');
    setIsRegistered(!isRegistered);
    setUsername('');
    setPassword('');
  };

  const handleRegistration = async () => {
    setPassCheck('');
    setRegisterMsg('');
    if (password === confirmPassword){
        setLoading(true);
        try {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password)
      
            const response = await axios.post("http://127.0.0.1:5000/api/register", formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            });
      
            const msg = response.data.message;
            console.log(msg)
            if (msg === 'username_error'){
                setRegisterMsg("Username already exists")
            }
            else {
                console.log("Account registered")
                setIsRegistered(!isRegistered);
                setPassCheck('');
                setConfirmPassword('');
            }
            
          } catch (error) {
            console.error('Error submitting input:', error);
          }
        setLoading(false);
    }
    else {
        setPassCheck('Confirm password does not equal password')
    }
    
  };

  

  return (
    <div className="login_container">

        {isRegistered ? (
            (
                <div className="container">
            <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />

            {loading1 ? (
                <div className="spinner"></div>
            ) : (
                <button onClick={handleLogin}>Login</button>
                )}
            


            {loginMsg && <p>{loginMsg}</p>}
            <h2>New to Second Brain?</h2>
            <button onClick={registrationButton}>Register Here</button>
        </div>
            )    
        ) : (
            (
                <div className="container">
                    <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
                    <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                    <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
                    
                    {passCheck && <p>{passCheck}</p>}
                    {registerMsg && <p>{registerMsg}</p>}

                    {loading ? (
                        <div className="spinner"></div>
                    ) : (
                        <button onClick={handleRegistration}>Register</button>
                    )}

                    
                </div>
            )
        )}
    </div>
  );
};



export default Login;