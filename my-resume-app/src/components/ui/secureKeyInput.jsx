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
    <div>
      <input
        type="password"
        className={styles.input}
        value={apiKey}
        disabled={locked}
        onChange={(e) => setApiKey(e.target.value)}
        onPaste={(e) => locked && e.preventDefault()}
        onCopy={(e) => locked && e.preventDefault()}
        placeholder="Enter your OpenAI API key"
      />
      {!locked && <button onClick={handleConfirm}>Confirm</button>}
      {locked && <p>🔒 Key locked for this session</p>}
      {/* <div>
        <p>Security Reminder</p>
        <p>
          Your API key is stored <strong>only in memory</strong> and will be
          lose when you refresh or close the page. For your safety:
        </p>
        <ul className="list-disc list-inside text-sm mt-2 space-y-1">
          <li>Don’t use this site on a public or shared computer</li>
          <li>Don’t leave this tab open unattended</li>
          <li>Close the tab when you're done</li>
        </ul>
      </div> */}
    </div>
  );
};

export default SecureKeyInput;
