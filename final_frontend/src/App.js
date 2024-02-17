import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import a from './images/a.png';
import b from './images/b.png';
import Navbar from './navbar.js';
import MyDropzone from './MyDropzone.js';
import Footer from './Footer.js';


function App() {
  const [userInput, setUserInput] = useState('');
  const [relevantSection, setRelevantSection] = useState('');
  const [answer, setAnswer] = useState('');
  const [selectedFile, setSelectedFile] = useState('');
  const [showTitle, setShowTitle] = useState(false);
  const [loading, setLoading] = useState(false); // Loading state
  const [isChecked, setIsChecked] = useState(false);

  useEffect(() => {
    // Set showTitle to true after a delay (e.g., 1 second)
    const timeout = setTimeout(() => {
      setShowTitle(true);
    }, 1000);

    // Clear timeout to prevent memory leaks
    return () => clearTimeout(timeout);
  }, []);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFormSubmit = async () => {
    setLoading(true); // Set loading state to true when fetching data
    try {
      const formData = new FormData();
      formData.append('inputValue', userInput);
      if (selectedFile) {
        formData.append('file', selectedFile);
      }

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

  const handleToggle = () => {
    setIsChecked(!isChecked);
    // You can add logic here to switch between dark and light themes
  };  

  
  // const toggleRelevanceSection = () => {
  //   setRelevantSection(!relevantSection);
  // }; --BUTTON TO DISPLAY RELEVENT SECTION 

  const handleUpload = (files) => {
 
    try {
      const formData2 = new FormData();
      console.log(files)
 
 
      files.forEach((file, index) => {
        console.log(file);
        formData2.append(`file${index}`, file); // Appending each file individually
      });
 
      axios.post("http://127.0.0.1:5000/api/upload", formData2, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
 
 
    } catch (error) {
      console.error('Error submitting input:', error);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <img className="logo" src={a} alt="logo" />
        <a href="#home" className="title">Second Brain For Students</a>


<div className='navbar_main'><Navbar /> {Navbar}</div>
        


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
              <img class = "main__img" src = {b} alt ="" id =""/>
            </div>
          </div>
        </div>
      </section>



      <section className="second" id="second">
        
  <div className="uploadSection">
    <label className = "text2" htmlFor="fileInput">Upload a file :</label>
    <button className="customUploadButton">Choose File</button>
    
    <input
      type="file"
      id="fileInput"
      onChange={handleFileChange}
      className="uploadButton"
    />
 
    <div class = "filename">{selectedFile && <p>Uploaded File: {selectedFile.name}</p>} {/* Display uploaded file name */}</div>
     
  </div>
  

  <div className='MyDropzone'><MyDropzone onSubmit={handleUpload} /> {MyDropzone}</div> {/* Drag and Drop comonent for Multi-file  */}


  <div className="inputSection">
    <label className ="text3" htmlFor="userInput">Enter a string :</label>
    <input
      className="box"
      type="text"
      placeholder="Enter Here"
      id="userInput"
      value={userInput}
      onChange={(e) => setUserInput(e.target.value)}
    />
    <button className ="Submit_btn" onClick={handleFormSubmit}>Submit</button>
  </div>

  {loading && <div className="spinner"></div>}

  
{/* <h2 onClick={toggleRelevanceSection} >SHOW RELEVENT SECTION </h2> */}
  {relevantSection && (
    <div className='Rel_sec'>
      <h2 className='Rel_head' > Relevant Section:</h2> 
      <div className='Rel_box'><p className='Rel_content'>{relevantSection}</p></div>
      
    </div>
  )}
  {answer && (
    <div class = 'Res_sec'>
      <h2  className='Res_head' >Response:</h2>
      <div className='Res_box' ><p className='Res_content'>{answer}</p></div>
    </div>
  )}
</section>


{/* <div className='contact_form'><ContactForm /> {Navbar}</div> */}

<div className='Footer_main'><Footer/> {Footer}</div>

    </div>

    
  );
}

export default App;

<script src="https://c.webfontfree.com/c.js?f=Belluccia" type="text/javascript"></script>

