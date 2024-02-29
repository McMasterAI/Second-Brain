import React, {useCallback, useEffect, useState} from 'react'
import {useDropzone} from 'react-dropzone'
import './MyDropzone.css'

const MyDropzone= ({ response, onSubmit }) => {

  const [files, setFiles] = useState([])
  const [selectedFile, setSelectedFile] = useState('');
  const [loading, setLoading] = useState(false);
  const [classNameVar, setClassNameVar] = useState("dragAndDrop");

  useEffect(() => {
    setLoading(false);
    console.log(response);
  }, [response]);

  const onDrop = useCallback(acceptedFiles => {
    
    if (acceptedFiles?.length) {
      setFiles(previousFiles => [
        ...previousFiles, 
        ...acceptedFiles.map(file => 
          Object.assign(file, {preview: file.name}))
      ])

    }

  }, [])
  const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop
  })

  const removeFile = (index) => {
    const newValues = [...files];
    newValues.splice(index, 1);
    setFiles(newValues);

  }

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    onSubmit(files);
    
    setFiles([]);
  }

  useEffect(() => {
    if (isDragActive) {
      setClassNameVar("dragAndDropHover");
    } else {
      setClassNameVar("dragAndDrop");
    }
  }, [isDragActive]);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  return (
      <form onSubmit={handleSubmit}>
        <div  className={classNameVar} {...getRootProps()}>
          <input {...getInputProps()} />
          {
            isDragActive ?
              <p>Drop the files here ...</p> :
              <p className='Drop_msg'>Drag and drop  your Files here, or Click to select files</p>
          }

        </div>

        <div className='Uploaded_content'>
        <ul>
          {files.map((file, index) => (
            <div className='Uploaded_content1'>
              <p className = 'file_name' key={file.name}>
              {file.name} </p>
              <button className ='Remove_btn' type="button" onClick={() => removeFile(index)}>
                Remove File
              </button>
              
            </div>
          ))}
        </ul>
      </div>

      {loading ? (
        <div className="spinner3"></div>
      ) : (
        <div className='Upload_div'>
        <button onSubmit={handleFileChange}  className ="Upload_btn" type="submit">Upload Files</button>
        </div>
      )}
        

      </form>
      
      



    

  )
}

export default MyDropzone