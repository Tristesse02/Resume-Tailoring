import React, { useState } from "react";
import styles from "./index.module.css"; // Import CSS Module

const ToggleButton = ({ isOn, setIsOn, onToggle }) => {
  const handleToggle = () => {
    const newValue = !isOn;
    setIsOn(newValue);
    onToggle(newValue);
  };

  return (
    <div className={styles.container}>
      <button
        onClick={handleToggle}
        className={isOn ? styles.buttonOn : styles.buttonOff}
      >
        {isOn ? "👍 Tailor" : "👎 Tailor"}
      </button>
    </div>
  );
};

export default ToggleButton;
