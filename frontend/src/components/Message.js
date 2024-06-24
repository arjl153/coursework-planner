import React from "react";

const Message = ({ role, content }) => {
  const formatContent = (text) => {
    if (role === "assistant") {
      return text.split("\n").map((str, index) => (
        <p key={index} style={{ margin: 0 }}>
          {str}
        </p>
      ));
    }
    return text;
  };

  return (
    <div className={`message ${role}`}>
      {formatContent(content)}
    </div>
  );
};

export default Message;
