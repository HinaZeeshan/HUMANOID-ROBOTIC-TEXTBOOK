import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

interface LoadingIndicatorProps {
  show: boolean;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({ show }) => {
  if (!show) return null;

  return (
    <div className={clsx(styles.message, styles.botMessage)}>
      <div className={styles.loadingDots}>
        <div className={styles.dot} />
        <div className={styles.dot} />
        <div className={styles.dot} />
      </div>
    </div>
  );
};

export default LoadingIndicator;