import React, { useState } from 'react';

const InputForm = ({ onSubmit }) => {
    const [inputValue, setInputValue] = useState('');

    const handleChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(inputValue)
        setInputValue('');
    };


    return (
        <form onSubmit={handleSubmit}>
            <label>
                Input:
                <input type="text" value={inputValue} onChange={handleChange} />
            </label>
            <button  type="submit">Submit</button>
        </form>
    );
};

export default InputForm;