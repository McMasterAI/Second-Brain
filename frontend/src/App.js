import './App.css';
import axios from 'axios';
import InputForm from './components/InputForm';
import React, { useEffect, useState } from 'react';

function App() {

  // variables
  const [data, setData] = useState([{}]);
  const [file, setFile] = useState(null);

  const [filenames, setFilenames] = useState([{}]);
  const [progress, setProgress] = useState( {started: false, pc:0} );
  const [msg, setMsg] = useState(null);

  // receiving data 
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/get").then(
      res => {
        return res.json();
      }
    ).then(
      data => {
        setData(data);
        console.log(data);
      });
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/getfiles").then(
      res => {
        return res.json();
      }
    ).then(
      file => {
        setFilenames(file);
        console.log(file);
      });
  }, []);

  // sending data
  const handleFormSubmit = (inputValue) => {
    axios.post("http://127.0.0.1:5000/api/submit", { inputValue })
      .then(response => {
          console.log('Backend response:', response.data);
          window.location.reload(false)
      })
      .catch(error => {
          console.error('Error submitting input:', error);
      });
  };

  function handleUpload(){
    if (!file) {
      setMsg("No file selected");
      return;
    }

    const fd = new FormData();
      fd.append('file', file);

      setMsg("Uploading...");
      setProgress(prevState => {
        return {...prevState, started: true}
      })
      axios.post("http://127.0.0.1:5000/api/files", fd, {
        onUploadProgress: (progressEvent) => { setProgress(prevState => {
          return { ...prevState, pc: progressEvent.progress*100 }
        })},
        header: {
          "Custon-Header": "value",
        }
      })
      .then (res => {
        setMsg("Upload successful");
        window.location.reload(false)
        console.log(res.data);
      })
        
      .catch (err => console.error(err))  
}

  
  return (
    <div className="App">

      <h1>Second Brain for Students</h1>
      <hr/>

      <InputForm onSubmit={handleFormSubmit} />
      {(typeof data.response === 'undefined') ? (
           <p>Loading...</p>
        ) : (
          data.response.map((item, i) => (
            <p key={i}>{item}</p>
          ))
        )}


      <input onChange={ (e) => { setFile(e.target.files[0]) }} type = "file"/>
      <button onClick = { handleUpload}>Upload</button>
      { progress.started && <progress max="100" value={progress.pc}></progress>}
      { msg && <span>{msg}</span>}

      
      <hr/>

      <h2>Files:</h2>
      {(typeof filenames.response === 'undefined') ? (
           <p>Loading...</p>
        ) : (
          filenames.response.map((item, i) => (
            <p key={i}> {item} </p>
          ))
        )}

    </div>
  );
}

export default App;
