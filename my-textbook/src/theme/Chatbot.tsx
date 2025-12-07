 import React, { JSX, useState } from 'react';
     
     // Define the type for a single message
     interface Message {
       text: string;
       sender: 'user' | 'bot';
     }
     
     function Chatbot(): JSX.Element {
       const [messages, setMessages] = useState<Message[]>([]);
       const [input, setInput] = useState<string>('');
       const [isLoading, setIsLoading] = useState<boolean>(false);
       const [error, setError] = useState<string | null>(null); // To handle Task T031 later
     
       const handleSendMessage = async (): Promise<void> => {
         if (input.trim() === '') return;
     
         const newMessage: Message = { text: input, sender: 'user' };
         setMessages((prevMessages) => [...prevMessages, newMessage]);
         setInput('');
         setIsLoading(true);
         setError(null);
     
         try {
           // Placeholder for API call (will be implemented in T024)
           // For now, simulate a response
           await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate loading
           const botResponse: Message = {
             text: "This is a placeholder response from the chatbot. Backend integration is coming soon!",
             sender: 'bot'
           };
           setMessages((prevMessages) => [...prevMessages, botResponse]);
         } catch (err) {
           console.error("Chatbot API error:", err);
           setError("Oops! The chatbot is currently unavailable. Please try again later or browse the textbook manually.");       // Error handling for T031
           setMessages((prevMessages) => [...prevMessages, { text: "Error: Could not get a response.", sender: 'bot' }]);  
         } finally {
           setIsLoading(false);
         }
       };
     
       return (
         <div style={{
           border: '1px solid #ccc',
           borderRadius: '8px',
           padding: '10px',
           maxWidth: '400px',
           margin: '20px auto',
           display: 'flex',
           flexDirection: 'column',
           height: '500px',
           boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
         }}>
           <h3 style={{ textAlign: 'center', marginBottom: '10px' }}>AI Chatbot Assistant</h3>
           <div style={{ flexGrow: 1, overflowY: 'auto', marginBottom: '10px', paddingRight: '5px' }}>
             {messages.map((msg, index) => (
               <div key={index} style={{
                 textAlign: msg.sender === 'user' ? 'right' : 'left',
                 marginBottom: '5px'
               }}>
                 <span style={{
                   display: 'inline-block',
                   padding: '8px 12px',
               borderRadius: '15px',
                   background: msg.sender === 'user' ? '#007bff' : '#f0f0f0',
                   color: msg.sender === 'user' ? 'white' : '#333',
                   maxWidth: '80%'
                 }}>
                   {msg.text}
                 </span>
               </div>
             ))}
             {isLoading && (
               <div style={{ textAlign: 'left', marginBottom: '5px' }}>
                 <span style={{
                   display: 'inline-block',
                   padding: '8px 12px',
                   borderRadius: '15px',
                   background: '#e0e0e0',
                   color: '#555',
                   maxWidth: '80%'
                 }}>
                   Thinking...
                 </span>
               </div>
             )}
             {error && <p style={{color: 'red', fontSize: '0.8em', textAlign: 'center'}}>{error}</p>}
           </div>
           <div style={{ display: 'flex' }}>
             <input
               type="text"
               value={input}
               onChange={(e) => setInput(e.target.value)}
               onKeyPress={(e) => { if (e.key === 'Enter' && !isLoading) handleSendMessage(); }}
               placeholder="Ask a question about the textbook..."
               style={{ flexGrow: 1, padding: '8px', borderRadius: '5px', border: '1px solid #ccc', marginRight: '5px' }}  
               disabled={isLoading}
             />
             <button
              onClick={handleSendMessage}
              style={{ padding: '8px 15px', borderRadius: '5px', border: 'none', background: '#007bff', color: 'white',   
       cursor: 'pointer' }}
              disabled={isLoading}
            >
              Send
            </button>
          </div>
        </div>
      );
    }
    
    export default Chatbot;