import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from '@docusaurus/router';
import { FiSend, FiX, FiMessageSquare, FiInfo, FiBook, FiZap, FiGlobe } from 'react-icons/fi';
import { API_BASE_URL } from '../config';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: Array<{
    title: string;
    module: string;
    chapter: string;
    relevance_score: number;
  }>;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [showSources, setShowSources] = useState(false);
  const [selectedModule, setSelectedModule] = useState<string>('all');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const location = useLocation();

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize chat session
  useEffect(() => {
    if (!sessionId) {
      // Generate a simple session ID
      const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      setSessionId(newSessionId);

      // Add welcome message
      setMessages([
        {
          id: `msg_${Date.now()}`,
          role: 'assistant',
          content: "Welcome to the Advanced Robotics Textbook Assistant! I can help you with complex queries spanning multiple modules. Ask about specific workflows like voice-to-navigation, sensor fusion, or integrated robot systems.",
          timestamp: new Date()
        }
      ]);
    }
  }, [sessionId]);

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
      // Determine if this is a cross-module query
      const isCrossModuleQuery = inputValue.toLowerCase().includes('from') &&
        (inputValue.toLowerCase().includes('to') ||
          inputValue.toLowerCase().includes('then')) &&
        (inputValue.toLowerCase().includes('voice') ||
          inputValue.toLowerCase().includes('navigate') ||
          inputValue.toLowerCase().includes('perceive') ||
          inputValue.toLowerCase().includes('plan') ||
          inputValue.toLowerCase().includes('execute'));

      // Call the backend API with cross-module support
      const response = await fetch(`${API_BASE_URL}/api/v1/rag/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          context_filter: selectedModule !== 'all' ? selectedModule : null,
          cross_module: isCrossModuleQuery,
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add assistant message with sources
      const assistantMessage: Message = {
        id: `msg_${Date.now()}_assistant`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        sources: data.sources || []
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

  const clearChat = () => {
    setMessages([
      {
        id: `msg_${Date.now()}`,
        role: 'assistant',
        content: "Chat history cleared. How can I help you with the robotics textbook content?",
        timestamp: new Date()
      }
    ]);
  };

  const toggleSources = () => {
    setShowSources(!showSources);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="bg-blue-500 p-3 rounded-lg">
                  <FiMessageSquare size={24} />
                </div>
                <div>
                  <h1 className="text-2xl font-bold">Advanced Robotics Assistant</h1>
                  <p className="text-blue-100">Cross-module queries and complex workflows</p>
                </div>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={toggleSources}
                  className="bg-blue-500 hover:bg-blue-400 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
                >
                  <FiInfo size={16} />
                  <span>{showSources ? 'Hide' : 'Show'} Sources</span>
                </button>
                <button
                  onClick={clearChat}
                  className="bg-white text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg font-medium transition-colors"
                >
                  Clear Chat
                </button>
              </div>
            </div>
          </div>

          {/* Module Selector */}
          <div className="bg-gray-50 p-4 border-b">
            <div className="flex flex-wrap items-center gap-4">
              <span className="text-gray-700 font-medium">Filter by module:</span>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setSelectedModule('all')}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${selectedModule === 'all'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                >
                  <FiGlobe className="inline mr-1" /> All
                </button>
                <button
                  onClick={() => setSelectedModule('module-1')}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors flex items-center ${selectedModule === 'module-1'
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                >
                  <FiBook className="inline mr-1" /> ROS 2
                </button>
                <button
                  onClick={() => setSelectedModule('module-2')}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors flex items-center ${selectedModule === 'module-2'
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                >
                  <FiZap className="inline mr-1" /> Sim
                </button>
                <button
                  onClick={() => setSelectedModule('module-3')}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors flex items-center ${selectedModule === 'module-3'
                    ? 'bg-yellow-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                >
                  <FiZap className="inline mr-1" /> AI Brain
                </button>
                <button
                  onClick={() => setSelectedModule('module-4')}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors flex items-center ${selectedModule === 'module-4'
                    ? 'bg-red-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                >
                  <FiZap className="inline mr-1" /> VLA
                </button>
              </div>
            </div>
          </div>

          {/* Chat Container */}
          <div className="flex flex-col md:flex-row h-[600px]">
            {/* Messages Area */}
            <div className="flex-1 flex flex-col">
              <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`mb-6 flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[85%] rounded-2xl p-4 ${message.role === 'user'
                        ? 'bg-blue-500 text-white rounded-br-none'
                        : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none shadow-sm'
                        }`}
                    >
                      <div className="font-medium mb-1">
                        {message.role === 'user' ? 'You' : 'Robotics Assistant'}
                      </div>
                      <div className="whitespace-pre-wrap">{message.content}</div>

                      {/* Sources display if available */}
                      {showSources && message.sources && message.sources.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-gray-200">
                          <div className="text-xs font-semibold text-gray-600 mb-2">Sources:</div>
                          <div className="space-y-1">
                            {message.sources.slice(0, 3).map((source, index) => (
                              <div key={index} className="text-xs text-gray-500 bg-gray-100 p-2 rounded">
                                <div className="font-medium">{source.title}</div>
                                <div className="flex justify-between">
                                  <span>{source.module}</span>
                                  <span>{source.chapter}</span>
                                  <span>Score: {source.relevance_score.toFixed(2)}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="mb-6 flex justify-start">
                    <div className="bg-white text-gray-800 border border-gray-200 rounded-2xl rounded-bl-none p-4 max-w-[85%] shadow-sm">
                      <div className="font-medium mb-1">Robotics Assistant</div>
                      <div className="flex items-center">
                        <div className="animate-pulse">Thinking</div>
                        <div className="ml-2 flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="border-t border-gray-200 p-4 bg-white">
                <div className="flex flex-col space-y-3">
                  <div className="flex">
                    <input
                      type="text"
                      value={inputValue}
                      onChange={handleInputChange}
                      onKeyDown={handleKeyDown}
                      placeholder="Ask about complex robotics workflows, cross-module integration, or specific concepts..."
                      className="flex-1 border border-gray-300 rounded-l-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      disabled={isLoading}
                    />
                    <button
                      onClick={handleSendMessage}
                      disabled={isLoading || !inputValue.trim()}
                      className={`bg-blue-600 text-white px-6 py-3 rounded-r-lg flex items-center ${isLoading || !inputValue.trim() ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'
                        }`}
                    >
                      <FiSend className="mr-2" />
                      Send
                    </button>
                  </div>

                  {/* Quick suggestions */}
                  <div className="flex flex-wrap gap-2">
                    <span className="text-sm text-gray-500">Try:</span>
                    <button
                      onClick={() => setInputValue("How does voice command flow to robot navigation?")}
                      className="text-xs bg-blue-100 text-blue-800 hover:bg-blue-200 px-3 py-1 rounded-full transition-colors"
                    >
                      Voice → Nav
                    </button>
                    <button
                      onClick={() => setInputValue("How do I integrate ROS 2 with Gazebo simulation?")}
                      className="text-xs bg-purple-100 text-purple-800 hover:bg-purple-200 px-3 py-1 rounded-full transition-colors"
                    >
                      ROS 2 + Gazebo
                    </button>
                    <button
                      onClick={() => setInputValue("Explain the VSLAM process in NVIDIA Isaac")}
                      className="text-xs bg-yellow-100 text-yellow-800 hover:bg-yellow-200 px-3 py-1 rounded-full transition-colors"
                    >
                      VSLAM
                    </button>
                    <button
                      onClick={() => setInputValue("How to implement perception-action loop?")}
                      className="text-xs bg-red-100 text-red-800 hover:bg-red-200 px-3 py-1 rounded-full transition-colors"
                    >
                      Perception-Action
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Information Panel */}
            <div className="w-full md:w-80 bg-gray-800 text-white p-4 overflow-y-auto">
              <h3 className="font-bold text-lg mb-4 flex items-center">
                <FiInfo className="mr-2" /> Capstone Knowledge
              </h3>
              <div className="space-y-4 text-sm">
                <div>
                  <h4 className="font-semibold text-blue-300 mb-2">Cross-Module Workflows</h4>
                  <ul className="space-y-1">
                    <li className="flex items-start">
                      <span className="text-green-400 mr-2">•</span>
                      Voice → Plan → Navigate → Perceive → Manipulate
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-400 mr-2">•</span>
                      Sensor fusion across modules
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-400 mr-2">•</span>
                      Integrated AI decision making
                    </li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold text-blue-300 mb-2">Module Integration</h4>
                  <ul className="space-y-1">
                    <li className="flex items-start">
                      <span className="text-yellow-400 mr-2">•</span>
                      ROS 2 nodes with simulation bridge
                    </li>
                    <li className="flex items-start">
                      <span className="text-yellow-400 mr-2">•</span>
                      Perception pipeline with Nav2
                    </li>
                    <li className="flex items-start">
                      <span className="text-yellow-400 mr-2">•</span>
                      VLA system coordination
                    </li>
                  </ul>
                </div>

                <div className="bg-gray-700 p-3 rounded-lg">
                  <h4 className="font-semibold text-cyan-300 mb-2">Pro Tips</h4>
                  <ul className="space-y-1 text-xs">
                    <li>• Ask about specific workflows to get integrated answers</li>
                    <li>• Use the module filter to focus on specific topics</li>
                    <li>• Toggle sources to see where answers come from</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;