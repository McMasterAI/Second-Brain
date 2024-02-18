import React, {useCallback, useState} from 'react'
import {useDropzone} from 'react-dropzone'
import './MyDropzone.css'

const MyDropzone= ({ onSubmit }) => {

  const [files, setFiles] = useState([])
  const [selectedFile, setSelectedFile] = useState('');

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
    onSubmit(files);
    setFiles([])
  }

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  return (
      <form onSubmit={handleSubmit}>
        <div  className="dragAndDrop" {...getRootProps()}>
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

        <div className='Upload_div'>
        <button onSubmit={handleFileChange}  className ="Upload_btn" type="submit">Upload Files</button>
        </div>

      </form>
      
      



    

  )
}

export default MyDropzone