import { useState } from "react";
import styles from "./ResumeForm.module.css";

export default function ResumeForm() {
  const [entries, setEntries] = useState([]);
  const [form, setForm] = useState({
    type: "",
    techStack: "",
    description: "",
    numbers: "",
  });

  const addEntry = () => {
    console.log("Add Entry Clicked!"); // Debugging log
    if (form.type && form.techStack && form.description && form.numbers) {
      setEntries([...entries, form]);
      console.log("New Entries:", [...entries, form]); // Debugging log
      setForm({ type: "", techStack: "", description: "", numbers: "" });
    } else {
      console.log("Missing Fields:", form); // Debugging log
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Resume Entry Form</h1>

      <div className={styles.formGroup}>
        <input
          className={styles.input}
          placeholder="Type (Intern, Job, Personal Project)"
          value={form.type}
          onChange={(e) => setForm({ ...form, type: e.target.value })}
        />
        <input
          className={styles.input}
          placeholder="Tech Stack (e.g. React, Node.js, AWS, etc.)"
          value={form.techStack}
          onChange={(e) => setForm({ ...form, techStack: e.target.value })}
        />
        <textarea
          className={styles.textarea}
          placeholder="Description (just describe by words, as detailed as possible)"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <input
          className={styles.input}
          placeholder="Numbers (Quantifiable Result)"
          value={form.numbers}
          onChange={(e) => setForm({ ...form, numbers: e.target.value })}
        />
        <button className={styles.button} onClick={addEntry}>
          Add Entry
        </button>
      </div>

      <div className={styles.entryList}>
        {entries.map((entry, index) => (
          <div key={index} className={styles.entryCard}>
            <p>
              <strong>Type:</strong> {entry.type}
            </p>
            <p>
              <strong>Tech Stack:</strong> {entry.techStack}
            </p>
            <p>
              <strong>Description:</strong> {entry.description}
            </p>
            <p>
              <strong>Numbers:</strong> {entry.numbers}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
