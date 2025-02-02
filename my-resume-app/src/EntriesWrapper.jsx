import { useState } from "react";
import styles from "./ResumeForm.module.css";
import ResumeForm from "./ResumeForm.jsx";
import AddEntry from "./AddEntry.jsx";

const EntriesWrapper = () => {
  const [entries, setEntries] = useState([{ id: 1 }]); // Start with one form

  const addNewEntry = () => {
    setEntries([...entries, { id: entries.length + 1 }]); // Create unique ID
  };

  return (
    <div className={styles.containerWrapper}>
      {entries.map((entry) => (
        <ResumeForm key={entry.id} id={entry.id} /> // Pass unique ID
      ))}
      <AddEntry onClick={addNewEntry} /> {/* Clicking adds another form */}
    </div>
  );
};

export default EntriesWrapper;
