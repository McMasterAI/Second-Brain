import React, { useState } from 'react';
import styled from 'styled-components';
import SBlogo from './assets/SBLogo.png'; // Adjust the path based on your project structure

const Container = styled.div`
  max-width: 100vw;
  height: 100vh;
  margin: auto; /* Center the container horizontally */
  background-color: #26a97a;
  padding: 0px;
  display: flex;
  flex-direction: column;
  align-items: center; /* Align content at the start (top) */
  justify-content: flex-start; /* Align content at the start (top) */
`;

const Header = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
`;

const Logo = styled.img`
  width: 7vw; // Adjust the size as needed
  height: 7vw; // Adjust the size as needed
  margin-right: 10px;

  &:hover {
    transform: scaleX(-1);
  }
`;

const Title = styled.h1`
  font-size: 6vw;
  color: rgb(255,75,220);
  margin: 0;
  text-shadow: 0 0 30px white;
  &:hover {
    color: rgb(60, 95, 255);
  }
`;

const InputContainer = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 10px;
`;

const TextBox = styled.input`
  min-width: 35vw; /* Adjust the minimum width as needed */
  padding: 3vh 1.5vw;
  color: black;
  border-radius: 15px;
  border: 3px solid black;
  font-size: 1.5vw;
  text-align: left;
  box-sizing: border-box; /* Include padding and border in the width calculation */


  &:focus {
    outline: none;
  }
`;

const SubmitButton = styled.button`
  padding: 3vh 3vw; /* Adjust the values as needed */
  background-color: rgb(255, 75, 220);
  color: white;
  cursor: pointer;
  border-radius: 15px;
  border-style:none;
  border: 3px solid black;
  font-size: 1.5vw;
  transition: ease background-color 250ms, ease transform 250ms;

  &:hover {
    background-color: rgb(210,50,175);
    transform: scale(1.03);
  }
`;

const ChooseFileButton = styled.label`
  padding: 3vh 3vw; /* Adjust the values as needed */
  background-color: rgb(60, 95, 255);
  color: white;
  cursor: pointer;
  border-radius: 15px;
  border-style: none;
  border: 3px solid black;
  font-size: 1.3vw;
  transition: ease background-color 250ms, ease transform 250ms;
  white-space: nowrap; /* Prevent text from wrapping */
  &:hover {
    background-color: rgb(50, 75, 210);
    transform: scale(1.03);
  }
`;

const FilesSection = styled.div`
  margin-top: 20px;
  background-color: white; /* Adjust the background color as needed */
  padding: 1vw; /* Adjust padding as needed */
  border-radius: 15px;
  width: 58vw;
  border: 3px solid black;

`;

const FileList = styled.ul`
  list-style-type: none;
  padding: 0;
`;

const FileItem = styled.li`
  margin-bottom: 5px;
`;

const App = () => {
  const [inputValue, setInputValue] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setUploadedFiles([...uploadedFiles, ...files]);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    // Add your logic for handling the form submission here
    // You can use the inputValue and uploadedFiles as needed
  };

  return (
    <Container>
      <Header>
        <Logo src={SBlogo} alt="Second Brain Logo" />
        <Title>Second Brain</Title>
      </Header>
      <form onSubmit={handleFormSubmit}>
        <InputContainer>
          <TextBox
            className="custom-textbox"
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Type a question..."
          />
          <SubmitButton type="submit">Submit</SubmitButton>
          <ChooseFileButton>
            Choose File
            <input type="file" style={{ display: 'none' }} onChange={handleFileChange} />
          </ChooseFileButton>
        </InputContainer>
      </form>
      <FilesSection>
        <h2>Files:</h2>
        <FileList>
          {uploadedFiles.map((file, index) => (
            <FileItem key={index}>{file.name}</FileItem>
          ))}
        </FileList>
      </FilesSection>
    </Container>
  );
};

export default App;
