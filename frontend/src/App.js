import './App.css';

import InputForm from './components/InputForm';
import React, { useEffect, useState } from 'react';

function App() {

  // variables
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState( {started: false, pc:0} );
  const [msg, setMsg] = useState(null);


  const handleFormSubmit = (inputValue) => {
    // submit a post request to backend
  };

  function handleUpload(){
    if (!file) {
      setMsg("No file selected");
      return;
    }

    // submit a post request to backend and send files 
}

  

  return (
    <div className="App">

      <h1>Second Brain for Students</h1>
      <hr/>

      <InputForm onSubmit={handleFormSubmit} />
      <p>Response from user: put the backend response in here somewhere</p>


      <input onChange={ (e) => { setFile(e.target.files[0]) }} type = "file"/>
      <button onClick = { handleUpload}>Upload</button>

      
      <hr/>

      <h2>Files:</h2>
      <p>
        Im not sure exactly how this is going to work yet but im expecting that we will list the file names here
        <br/>file 2
        <br/>file 3
        <br/>etc.
      </p>

    </div>
  );
}

export default App;
