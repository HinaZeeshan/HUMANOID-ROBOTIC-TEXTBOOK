import React from 'react';
import { FaPaperPlane } from 'react-icons/fa';
import clsx from 'clsx';
import styles from './styles.module.css';

interface MessageInputProps {
  inputValue: string;
  isLoading: boolean;
  selectedText: string | null;
  onChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

const MessageInput: React.FC<MessageInputProps> = ({
  inputValue,
  isLoading,
  selectedText,
  onChange,
  onSubmit
}) => {
  return (
    <form className={styles.inputArea} onSubmit={onSubmit}>
      <input
        type="text"
        className={styles.input}
        value={inputValue}
        onChange={(e) => onChange(e.target.value)}
        placeholder={selectedText ? "Ask about selected text..." : "Ask a question..."}
        disabled={isLoading}
      />
      <button
        type="submit"
        className={styles.sendButton}
        disabled={isLoading || !inputValue.trim()}
      >
        <FaPaperPlane size={16} />
      </button>
    </form>
  );
};

export default MessageInput;