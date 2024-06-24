import React from "react";

const Input = ({ value, onChange, onClick }) => {
  return (
    <div className="input-container">
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder="Type your message here..."
      />
      <button onClick={onClick}>Send</button>
    </div>
  );
};

export default Input;
