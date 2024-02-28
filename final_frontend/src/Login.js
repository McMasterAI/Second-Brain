import React, { useState, useEffect } from 'react';
import './Login.css';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faLock, faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import secondbrainlogo from './images/a.png';
import { BsEyeFill } from "react-icons/bs";

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

  const [title, setTitle] = useState("Log In");
  const [signupDisabled, setSignupDisabled] = useState(true);
  const [signinDisabled, setSigninDisabled] = useState(false);

  const [text1, setText1] = useState("New to Second Brain?");
  const [text2, setText2] = useState("Click Register Now!");




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
      //alert('Click Login');
    }
    else{  
    setNameFieldMaxHeight("0");
    setTitle("Log In");
    setSignupDisabled(true);
    setSigninDisabled(false);
    setLoginMsg('');
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
      //alert('Click Register');
    } else {
      // Otherwise, proceed with sign-up functionality
      setNameFieldMaxHeight("60px");
      setTitle("Register New User");
      setSignupDisabled(false);
      setSigninDisabled(true);
      setLoginMsg('');
      setIsRegistered(!isRegistered);
      setUsername('');
      setPassword('');
      setConfirmPassword('');
      setPassCheck('');
      setRegisterMsg('');
    }
  };

 

  const handleRegistration = async (event) => {

    event.preventDefault();

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
                handleSigninClick();
                setPassCheck('');
                setConfirmPassword('');
                setText1("Account Created Successfully!");
                setText2("Welcome to Second Brain, " + username + "!");
          }
            
          } catch (error) {
            console.error('Error submitting input:', error);
          }
        setLoading(false);
    }
    else {
        setPassCheck('Confirm password does not equal password');
        console.log("Password check failed");
    }
  };

  const [passwordVisible1, setPasswordVisible1] = useState(false);
  const [passwordVisible2, setPasswordVisible2] = useState(false);

  const handleVisibility1 = () => {
    setPasswordVisible1(!passwordVisible1);
  };
  const handleVisibility2 = () => {
    setPasswordVisible2(!passwordVisible2);
  };

  return (
    <body>
      <div className="container"></div>
      <div className="form-box">
        <img className="login_logo" alt= "logo" src={secondbrainlogo}/>
        <h1 id="title">{title}</h1>
        <form>
          <div className="input-group">
            <div className="input-field">
              <FontAwesomeIcon className="i" icon={faUser} />
              <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
            </div>
            <div className="input-field">
            
              <FontAwesomeIcon className="i" icon={faLock} />
              <input type={passwordVisible1 ? "text" : "password"} placeholder="Password" id="password1" value={password} onChange={e => setPassword(e.target.value)} />
              <FontAwesomeIcon className="i2" icon={passwordVisible1 ? faEye: faEyeSlash} id="eyeicon1" onClick={handleVisibility1}/>
            </div>
  
            <div className="input-field" id="nameField" style={{ maxHeight: nameFieldMaxHeight }}>
              <FontAwesomeIcon className="i" icon={faLock} />
              <input type={passwordVisible2 ? "text" : "password"} id="password2" placeholder="Confirm Password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
              <FontAwesomeIcon className="i2" id="eyeicon2" icon={passwordVisible2 ? faEye: faEyeSlash} onClick={handleVisibility2}/>
            </div>
  
            {(signupDisabled && !loading1) && (
              <>
                {loginMsg && <p className="message_styling">{loginMsg}</p>}
                
                <button className='main_btn' onClick={handleLogin}>Login</button>

                <h2 className='text'>{text1}</h2>
                <h2 className='text'>{text2}</h2>
                
              </>
            )}
            {loading1 && (
              <div className="spinner2"></div>
            )}
  
            {(signinDisabled && !loading) && (
              <>
                {passCheck && <p className="message_styling">{passCheck}</p>}
                {registerMsg && <p className="message_styling">{registerMsg}</p>}
                <button className='main_btn' onClick={handleRegistration}>Register</button>

              </>
            )}
            {loading && (
              <div className="spinner2"></div>
            )}
          </div>
          <div className="btn-field">
            <button type="button" id="signupbtn" className={signupDisabled ? "disabled" : ""} onClick={registrationButton}>
              Register Now!
            </button>
            <button type="button" id="signinbtn" className={signinDisabled ? "disabled" : ""} onClick={handleSigninClick}>
              Back to Login Page
            </button>
          </div>
        </form>
      </div>
    </body>
  );
  
}

export default Login;



