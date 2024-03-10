import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import a from './images/a.png';
import b from './images/b.png';
import Navbar from './navbar.js';
import MyDropzone from './MyDropzone.js';
import Footer from './Footer.js';


const App = ({ onLogout }) => {
  const [userInput, setUserInput] = useState('');
  const [relevantSection, setRelevantSection] = useState('');
  const [answer, setAnswer] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false); // Loading state

  useEffect(() => {
    // Set showTitle to true after a delay (e.g., 1 second)
    const timeout = setTimeout(() => {
     
    }, 1000);
    // Clear timeout to prevent memory leaks
    return () => clearTimeout(timeout);
  }, []);


  const handleFormSubmit = async () => {
    setLoading(true); // Set loading state to true when fetching data
    try {
      const formData = new FormData();
      formData.append('inputValue', userInput);
      const token = localStorage.getItem('authToken');
      formData.append('username', token);

      const response = await axios.post("http://127.0.0.1:5000/api/submit", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setRelevantSection(response.data.relevantSection);
      setAnswer(response.data.answer);


    } catch (error) {
      console.error('Error submitting input:', error);
    }
    finally {
      setLoading(false); // Set loading state to false after data is fetched
    }
  };

  const handleUpload = async (files) => {

    try {
      const formData2 = new FormData();
      console.log(files)
      const token = localStorage.getItem('authToken');
      formData2.append('username', token);
 
 
      files.forEach((file, index) => {
        console.log(file);
        formData2.append(`file${index}`, file); // Appending each file individually with a unique json key (file1, file2, ..., filex)
      });
 
      const response1 = await axios.post("http://127.0.0.1:5000/api/upload", formData2, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      
      });
      
      setResponse(response1.data.response);
      console.log(response1.data.response);

    } catch (error) {
      console.error('Error submitting input:', error);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <img className="logo" src={a} alt="logo" />
        <a href="#home" className="title">Second Brain For Students</a>


<div className='navbar_main'><Navbar onLogout={onLogout}/></div>
        


      </header>

      <section>
        <div className="main">
          <div className="main__container">
            <div className="main__content">
              <h1>TIRED OF SCROLLING </h1>
              <h2>DOCUMENTS </h2>
              <p>Not Anymore!!</p>
              <button className="main__btn"><a href='#second'>Try Now</a></button>
            </div>
            <div className = "main__img--container">
              <img className = "main__img" src = {b} alt ="" id =""/>
            </div>
          </div>
        </div>
      </section>



      <section className="second" id="second">
        

  

  <div className='MyDropzone'><MyDropzone onSubmit={handleUpload} response={response} /> </div> {/* Drag and Drop comonent for Multi-file  */}


  <div className="inputSection">
    <label className ="text3" htmlFor="userInput">Ask a question:</label>
    <input
      className="box"
      type="text"
      placeholder="Enter Here"
      id="userInput"
      value={userInput}
      onChange={(e) => setUserInput(e.target.value)}
    />
    
  </div>

  {loading ? (
        <div className="spinner"></div>
      ) : (
        <button className ="Submit_btn2" onClick={handleFormSubmit}>Submit</button>
      )}
    
  

  

  
{/* <h2 onClick={toggleRelevanceSection} >SHOW RELEVENT SECTION </h2> */}
  
  {answer && (
    <div className = 'Res_sec'>
      <h2  className='Res_head' >Response:</h2>
      <div className='Res_box' ><p className='Res_content'>{answer}</p></div>
    </div>
  )}
  {relevantSection && (
    <div className='Rel_sec'>
      <h2 className='Rel_head' > Relevant Section:</h2> 
      <div className='Rel_box'><p className='Rel_content'>{relevantSection}</p></div>
      
    </div>
  )}
</section>


{/* <div className='contact_form'><ContactForm /> {Navbar}</div> */}

<div className='Footer_main'><Footer/> </div>

    </div>

    
  );
}

export default App;

<script src="https://c.webfontfree.com/c.js?f=Belluccia" type="text/javascript"></script>

