import React, { useState, useEffect } from 'react';
import './Login.css';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faEnvelope, faLock } from '@fortawesome/free-solid-svg-icons';

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
  const [nameFieldMaxHeight, setNameFieldMaxHeight] = useState("0");

  const [title, setTitle] = useState("Sign In");
  const [signupDisabled, setSignupDisabled] = useState(true);
  const [signinDisabled, setSigninDisabled] = useState(false);




  useEffect(() => {
    setLoading1(false);
    setLoginMsg(message);
    setMessageCounter(counter);
    const signupbtn = document.getElementById("signupbtn");
    const signinbtn = document.getElementById("signinbtn");
    const nameField = document.getElementById("nameField");

    nameField.style.maxHeight = nameFieldMaxHeight;
    setTitle(title);
    if (signupDisabled) {
      signupbtn.classList.add("disabled");
    } else {
      signupbtn.classList.remove("disabled");
    }
    if (signinDisabled) {
      signinbtn.classList.add("disabled");
    } else {
      signinbtn.classList.remove("disabled");
    }
  }, [message, counter , nameFieldMaxHeight, title, signupDisabled, signinDisabled]);

  const handleSigninClick = () => {

    if (!signinDisabled) {
      // Show alert if sign-in state is disabled
      alert('Click Login');}
    else{  
    setNameFieldMaxHeight("0");
    setTitle("Sign In");
    setSignupDisabled(true);
    setSigninDisabled(false);
  }
};



  const handleLogin = () => {

    setLoading1(true);
    setLoginMsg('');
    onLogin(username, password, messageCounter);
  };

  const registrationButton = () => {
    if (!signupDisabled) {
      // Show alert if sign-in state is disabled
      alert('Click Register');
    } else {
      // Otherwise, proceed with sign-up functionality
      setNameFieldMaxHeight("60px");
      setTitle("Sign Up");
      setSignupDisabled(false);
      setSigninDisabled(true);
      setLoginMsg('');
      setIsRegistered(!isRegistered);
      setUsername('');
      setPassword('');
    }
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
    <body>
      <div className="container"></div>
      <div className="form-box">
        <h1 id="title">{title}</h1>
        <form>
          <div className="input-group">
            <div className="input-field">
              <FontAwesomeIcon className="i" icon={faUser} />
              <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
            </div>
            <div className="input-field">
              <FontAwesomeIcon className="i" icon={faLock} />
              <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            </div>
  
            <div className="input-field" id="nameField" style={{ maxHeight: nameFieldMaxHeight }}>
              <FontAwesomeIcon className="i" icon={faLock} />
              <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
            </div>
  
            {(signupDisabled && !loading1) && (
              <>
                {loginMsg && <p>{loginMsg}</p>}
                
                <button className='main_btn' onClick={handleLogin}>Login</button>

                <h2 className='text'>New to Second Brain? </h2>
                <h2 className='text'>Click Sign Up! </h2>
                
              </>
            )}
            {loading1 && (
              <div className="spinner"></div>
            )}
  
            {(signinDisabled && !loading) && (
              <>
                {passCheck && <p>{passCheck}</p>}
                {registerMsg && <p>{registerMsg}</p>}
                <button className='main_btn' onClick={handleRegistration}>Register</button>

              </>
            )}
            {loading && (
              <div className="spinner"></div>
            )}
          </div>
          <div className="btn-field">
            <button type="button" id="signupbtn" className={signupDisabled ? "disabled" : ""} onClick={registrationButton}>
              Sign up
            </button>
            <button type="button" id="signinbtn" className={signinDisabled ? "disabled" : ""} onClick={handleSigninClick}>
              Sign in
            </button>
          </div>
        </form>
      </div>
    </body>
  );
  
}

export default Login;



