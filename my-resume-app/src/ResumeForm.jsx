import { useState } from "react";
import styles from "./ResumeForm.module.css";

export default function ResumeForm({ id }) {
  const [form, setForm] = useState({
    type: "",
    techStack: "",
    description: "",
    numbers: "",
  });

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Resume Entry Form {id}</h1>

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
      </div>
    </div>
  );
}
