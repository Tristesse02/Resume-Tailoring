import React, { useState } from "react";
import styles from "./index.module.css";

const SecureKeyInput = ({ onConfirm }) => {
  const [apiKey, setApiKey] = useState("");
  const [locked, setLocked] = useState(false);

  const handleConfirm = () => {
    if (apiKey.trim().startsWith("sk-")) {
      setLocked(true);
      onConfirm(apiKey); // Pass to parent component
    } else {
      alert("Invalid key format.");
    }
  };

  return (
    <div className={styles.form}>
      <div className={styles.formGrid}>
        <div style={{ gridColumn: "span 5" }}>
          <label>API Key</label>
          <input
            type="password"
            className={styles.profileInput}
            value={apiKey}
            disabled={locked}
            onChange={(e) => setApiKey(e.target.value)}
            onPaste={(e) => locked && e.preventDefault()}
            onCopy={(e) => locked && e.preventDefault()}
            placeholder="Enter your OpenAI API key"
          />
        </div>
        <div
          style={{
            gridColumn: "span 1",
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "flex-start",
          }}
        >
          <label></label>
          {!locked && (
            <button onClick={handleConfirm} className={styles.confirmButton}>
              Confirm
            </button>
          )}
        </div>
        <div
          style={{
            gridColumn: "span 6",
          }}
        >
          {locked && (
            <p style={{ margin: "0" }}>🔒 Key locked for this session</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default SecureKeyInput;
