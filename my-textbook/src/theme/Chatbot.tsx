import React, { JSX, useState } from 'react';

// Define the type for a single message
interface Message {
  text: string;
  sender: 'user' | 'bot';
}

function Chatbot(): JSX.Element {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSendMessage = async (): Promise<void> => {
    if (input.trim() === '') return;

    const newMessage: Message = { text: input, sender: 'user' };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Placeholder for API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      const botResponse: Message = {
        text: "This is a placeholder response. Backend integration is next!",
        sender: 'bot'
      };
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    } catch (err) {
      console.error("Chatbot API error:", err);
      setError("Oops! The chatbot is currently unavailable. Please try again later.");
      setMessages((prevMessages) => [...prevMessages, { text: "Error: Could not get a response.", sender: 'bot' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => setIsOpen(!isOpen);

  if (!isOpen) {
    return (
      <button
        onClick={toggleChat}
        style={{
          position: 'fixed',
          bottom: '30px',
          right: '30px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: '#007bff',
          color: 'white',
          border: 'none',
          cursor: 'pointer',
          boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
          fontSize: '24px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <span>&#128172;</span>
      </button>
    );
  }

  return (
    <div style={{
      position: 'fixed',
      bottom: '30px',
      right: '30px',
      width: '400px',
      height: '500px',
      border: '1px solid #ccc',
      borderRadius: '8px',
      background: 'white',
      display: 'flex',
      flexDirection: 'column',
      boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
      zIndex: 1000,
    }}>
      <div style={{
        padding: '10px',
        background: '#007bff',
        color: 'white',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderTopLeftRadius: '8px',
        borderTopRightRadius: '8px',
      }}>
        <h3 style={{ margin: 0, fontSize: '1.2em' }}>AI Chatbot Assistant</h3>
        <button onClick={toggleChat} style={{ background: 'none', border: 'none', color: 'white', fontSize: '20px', cursor: 'pointer' }}>&times;</button>
      </div>

      <div style={{ flexGrow: 1, overflowY: 'auto', padding: '10px' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{
            textAlign: msg.sender === 'user' ? 'right' : 'left',
            marginBottom: '10px',
          }}>
            <span style={{
              display: 'inline-block',
              padding: '10px 15px',
              borderRadius: '20px',
              background: msg.sender === 'user' ? '#007bff' : '#f1f1f1',
              color: msg.sender === 'user' ? 'white' : '#333',
              maxWidth: '85%',
              wordWrap: 'break-word',
            }}>
              {msg.text}
            </span>
          </div>
        ))}
        {isLoading && (
          <div style={{ textAlign: 'left', marginBottom: '10px' }}>
            <span style={{ display: 'inline-block', padding: '10px 15px', borderRadius: '20px', background: '#e0e0e0', color: '#555' }}>
              Thinking...
            </span>
          </div>
        )}
        {error && <p style={{ color: 'red', fontSize: '0.9em', textAlign: 'center' }}>{error}</p>}
      </div>

      <div style={{ padding: '10px', borderTop: '1px solid #ccc' }}>
        <div style={{ display: 'flex' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => { if (e.key === 'Enter' && !isLoading) handleSendMessage(); }}
            placeholder="Ask a question..."
            style={{ flexGrow: 1, padding: '10px', borderRadius: '20px', border: '1px solid #ccc', marginRight: '10px' }}
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            style={{ padding: '10px 20px', borderRadius: '20px', border: 'none', background: '#007bff', color: 'white', cursor: 'pointer' }}
            disabled={isLoading}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chatbot;