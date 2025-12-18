import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from '@docusaurus/router';
import { FiSend, FiX, FiMessageSquare } from 'react-icons/fi';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const location = useLocation();

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize chat session
  useEffect(() => {
    if (isOpen && !sessionId) {
      // Generate a simple session ID
      const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      setSessionId(newSessionId);

      // Add welcome message
      setMessages([
        {
          id: `msg_${Date.now()}`,
          role: 'assistant',
          content: "Hello! I'm your Humanoid Robotics textbook assistant. Ask me anything about the content you're reading!",
          timestamp: new Date()
        }
      ]);
    }
  }, [isOpen, sessionId]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: `msg_${Date.now()}_user`,
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get current page context for more relevant answers
      const currentPageContext = location.pathname;

      // Check if this is a cross-module or capstone query
      const isCrossModuleQuery = inputValue.toLowerCase().includes('from') &&
                                (inputValue.toLowerCase().includes('to') ||
                                 inputValue.toLowerCase().includes('then')) &&
                                (inputValue.toLowerCase().includes('voice') ||
                                 inputValue.toLowerCase().includes('navigate') ||
                                 inputValue.toLowerCase().includes('perceive') ||
                                 inputValue.toLowerCase().includes('plan') ||
                                 inputValue.toLowerCase().includes('execute'));

      // Enhanced context detection for different modules
      let contextFilter = null;
      let isCrossModuleSearch = false;

      if (isCrossModuleQuery || currentPageContext.includes('capstone') || currentPageContext.includes('05')) {
        // This is a cross-module query or we're on the capstone page
        isCrossModuleSearch = true;
        contextFilter = null; // Let backend handle cross-module search
      } else if (currentPageContext.includes('ros2') || currentPageContext.includes('01')) {
        contextFilter = 'module-1';
      } else if (currentPageContext.includes('digital') || currentPageContext.includes('02')) {
        contextFilter = 'module-2';
      } else if (currentPageContext.includes('ai') || currentPageContext.includes('03')) {
        contextFilter = 'module-3';
      } else if (currentPageContext.includes('vla') || currentPageContext.includes('04')) {
        contextFilter = 'module-4';
      }

      // Call the backend API
      const response = await fetch('http://localhost:8000/api/v1/rag/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          context_filter: contextFilter,
          cross_module: isCrossModuleSearch, // Indicate if this is a cross-module query
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add assistant message
      const assistantMessage: Message = {
        id: `msg_${Date.now()}_assistant`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage: Message = {
        id: `msg_${Date.now()}_error`,
        role: 'assistant',
        content: "Sorry, I'm having trouble connecting to the knowledge base. Please try again.",
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Chatbot button - shown when chat is closed */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 z-50"
          aria-label="Open chatbot"
        >
          <FiMessageSquare size={24} />
        </button>
      )}

      {/* Chatbot panel - shown when chat is open */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-full max-w-md h-2/3 max-h-96 bg-white rounded-lg shadow-xl border border-gray-200 flex flex-col z-50">
          {/* Header */}
          <div className="bg-blue-600 text-white p-3 rounded-t-lg flex justify-between items-center">
            <h3 className="font-semibold">Robotics Textbook Assistant</h3>
            <button
              onClick={closeChat}
              className="text-white hover:text-gray-200 focus:outline-none"
              aria-label="Close chat"
            >
              <FiX size={20} />
            </button>
          </div>

          {/* Messages container */}
          <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`mb-4 flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    message.role === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {message.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="mb-4 flex justify-start">
                <div className="bg-gray-200 text-gray-800 rounded-lg p-3 max-w-[80%]">
                  Thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input area */}
          <div className="border-t border-gray-200 p-3 bg-white">
            <div className="flex">
              <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                placeholder="Ask about the textbook content..."
                className="flex-1 border border-gray-300 rounded-l-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
                className={`bg-blue-600 text-white px-4 py-2 rounded-r-lg ${
                  isLoading || !inputValue.trim() ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'
                }`}
                aria-label="Send message"
              >
                <FiSend />
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-1 text-center">
              Powered by RAG - Responses based on textbook content
            </p>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;