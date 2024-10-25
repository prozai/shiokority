// src/components/TopNotificationBar.jsx
import React, { useState } from 'react';

const TopNotificationBar = ({ initialAlerts }) => {
  const [alerts, setAlerts] = useState(initialAlerts);

  const handleDismiss = (index) => {
    // Filter out the alert at the clicked index
    setAlerts((prevAlerts) => prevAlerts.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4 mb-8">
      {alerts.map((alert, index) => (
        <Alert
          key={index}
          color={alert.color}
          message={alert.message}
          onDismiss={() => handleDismiss(index)}
        />
      ))}
    </div>
  );
};

const Alert = ({ color, message, onDismiss }) => (
  <div className={`${color} text-white p-4 rounded-lg flex justify-between items-center`}>
    <span>{message}</span>
    <button className="text-white font-bold" onClick={onDismiss}>×</button>
  </div>
);

export default TopNotificationBar;
