import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: { title: string; module: string; chapter: string }[];
}

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  return (
    <div
      className={clsx(styles.message, message.role === 'user' ? styles.userMessage : styles.botMessage)}
    >
      <div>{message.content}</div>
      {message.sources && message.sources.length > 0 && (
        <div className={styles.sources}>
          {message.sources.slice(0, 3).map((source, idx) => (
            <span key={idx} className={styles.sourceItem}>
              📚 <strong>{source.module}</strong>: {source.title}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

export default MessageBubble;