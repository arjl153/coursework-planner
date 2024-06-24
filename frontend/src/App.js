import { useState } from "react";
import axios from "axios";

import Message from "./components/Message";
import Input from "./components/Input";

import "./styles.css";

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSubmit = async () => {
    const prompt = {
      role: "user",
      content: input,
    };

    setMessages([...messages, prompt]);

    try {
      const response = await axios.post("http://localhost:5001/query", {
        query: input,
      });

      const res = response.data.result_with_knowledge;
      setMessages((messages) => [
        ...messages,
        {
          role: "assistant",
          content: res,
        },
      ]);
      setInput("");
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  };

  return (
    <div className="App">
      <h1>Indiana University Bloomington Chat-Bot</h1>
      <p>Ask any questions about IUB Professors and courses</p>
      <div className="chat-container">
        <div className="Column">
          <div className="Content">
            {messages.map((el, i) => (
              <Message key={i} role={el.role} content={el.content} />
            ))}
          </div>
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onClick={input ? handleSubmit : undefined}
          />
        </div>
      </div>
    </div>
  );
}
