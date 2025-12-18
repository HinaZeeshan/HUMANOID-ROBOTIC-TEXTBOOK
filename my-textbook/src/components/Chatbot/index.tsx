import React, { useState, useEffect, useRef } from 'react';
import { FaRobot, FaTimes, FaBookOpen } from 'react-icons/fa';
import { useLocation } from '@docusaurus/router';
import MessageBubble from './MessageBubble';
import MessageInput from './MessageInput';
import LoadingIndicator from './LoadingIndicator';
import styles from './styles.module.css';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    sources?: { title: string; module: string; chapter: string }[];
}

export default function Chatbot() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            role: 'assistant',
            content: 'Hi! I\'m your AI assistant for the Humanoid Robotics Textbook. Ask me anything about the content!',
        },
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [selectedText, setSelectedText] = useState<string | null>(null);
    const location = useLocation(); // Get current location
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Monitor text selection
    useEffect(() => {
        const handleSelection = () => {
            const selection = window.getSelection();
            if (selection && selection.toString().trim().length > 0) {
                setSelectedText(selection.toString().trim());
            } else {
                setSelectedText(null);
            }
        };

        document.addEventListener('mouseup', handleSelection);
        return () => document.removeEventListener('mouseup', handleSelection);
    }, []);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!inputValue.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: inputValue,
        };

        setMessages((prev) => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            // Determine context based on current page
            const currentPageContext = location.pathname;
            let contextFilter = null;
            let isCrossModuleSearch = true; // Default to cross-module if not specific

            // Logic from previous implementation
            const isCrossModuleQuery = inputValue.toLowerCase().includes('from') &&
                (inputValue.toLowerCase().includes('to') ||
                    inputValue.toLowerCase().includes('then')) &&
                (inputValue.toLowerCase().includes('voice') ||
                    inputValue.toLowerCase().includes('navigate') ||
                    inputValue.toLowerCase().includes('perceive') ||
                    inputValue.toLowerCase().includes('plan') ||
                    inputValue.toLowerCase().includes('execute'));

            if (!isCrossModuleQuery && !currentPageContext.includes('capstone') && !currentPageContext.includes('05')) {
                if (currentPageContext.includes('ros2') || currentPageContext.includes('01')) {
                    contextFilter = 'module-1';
                    isCrossModuleSearch = false;
                } else if (currentPageContext.includes('digital') || currentPageContext.includes('02')) {
                    contextFilter = 'module-2';
                    isCrossModuleSearch = false;
                } else if (currentPageContext.includes('ai') || currentPageContext.includes('03')) {
                    contextFilter = 'module-3';
                    isCrossModuleSearch = false;
                } else if (currentPageContext.includes('vla') || currentPageContext.includes('04')) {
                    contextFilter = 'module-4';
                    isCrossModuleSearch = false;
                }
            }

            const response = await fetch('http://localhost:8000/api/v1/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: userMessage.content,
                    selected_text: selectedText,
                    query_type: selectedText ? "selected_text_only" : "full_book",
                }),
            });

            if (!response.ok) throw new Error('Failed to fetch response');

            const data = await response.json();

            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: data.answer,
                sources: data.source_citations.map((cit: any) => ({
                    title: cit.title,
                    module: cit.location,
                    chapter: cit.section_id
                })),
            };

            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            console.error('Chat error:', error);
            setMessages((prev) => [
                ...prev,
                {
                    id: Date.now().toString(),
                    role: 'assistant',
                    content: 'Sorry, I encountered an error. Please ensure the backend server is running.',
                },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={styles.chatbotContainer}>
            {!isOpen && (
                <button
                    className={styles.toggleButton}
                    onClick={() => setIsOpen(true)}
                    aria-label="Open Chat"
                >
                    <FaRobot size={24} color="#000" />
                </button>
            )}

            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.header}>
                        <h3 className={styles.title}>AI Assistant {selectedText && '(Context Active)'}</h3>
                        <button
                            className={styles.closeButton}
                            onClick={() => setIsOpen(false)}
                            aria-label="Close Chat"
                        >
                            <FaTimes size={20} />
                        </button>
                    </div>

                    {selectedText && (
                        <div className={styles.contextIndicator}>
                            <FaBookOpen />
                            Using selected text as context
                        </div>
                    )}

                    <div className={styles.messagesContainer}>
                        {messages.map((msg) => (
                            <MessageBubble key={msg.id} message={msg} />
                        ))}
                        <LoadingIndicator show={isLoading} />
                        <div ref={messagesEndRef} />
                    </div>

                    <MessageInput
                        inputValue={inputValue}
                        isLoading={isLoading}
                        selectedText={selectedText}
                        onChange={setInputValue}
                        onSubmit={handleSubmit}
                    />
                </div>
            )}
        </div>
    );
}
