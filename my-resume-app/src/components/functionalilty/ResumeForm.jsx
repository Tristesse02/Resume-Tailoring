import { useState } from "react";
import styles from "./index.module.css";

export default function ResumeForm({
  id,
  formData,
  updateFormData,
  removeEntry,
}) {
  const [form, setForm] = useState(
    formData || {
      name: "",
      type: "",
      techStack: "",
      description: "",
      numbers: "",
      bulletPoints: "",
    }
  );

  const handleChange = (e) => {
    const newFormData = { ...form, [e.target.name]: e.target.value };
    setForm(newFormData);
    updateFormData(id, newFormData);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Experience {id}</h1>
        <button className={styles.removeButton} onClick={() => removeEntry(id)}>
          ❌
        </button>
      </div>

      <div className={styles.formGroup}>
        <input
          name="name"
          className={styles.input}
          placeholder="Job/Project Name 🤔"
          value={form.name}
          onChange={handleChange}
        />
        <select
          name="type"
          className={styles.input}
          value={form.type}
          onChange={handleChange}
        >
          <option value="">Select Type 💜</option>
          <option value="Job">Job</option>
          <option value="Project">Project</option>
        </select>
        <input
          name="techStack"
          className={styles.input}
          placeholder="Tech Stack ⚙️🛠️(e.g. React, Node.js, AWS, etc.)"
          value={form.techStack}
          onChange={handleChange}
        />
        <textarea
          name="description"
          className={styles.textarea}
          placeholder="Description 📃(just describe by words, as detailed as possible)"
          value={form.description}
          onChange={handleChange}
        />
        <input
          name="numbers"
          className={styles.input}
          placeholder="Numbers 🔢(Quantifiable Result)"
          value={form.numbers}
          onChange={handleChange}
        />
        <input
          name="bulletPoints"
          className={styles.input}
          placeholder="How many bullet points do you want to add? (From 👆to🤚)"
          value={form.bulletPoints}
          onChange={handleChange}
        />
      </div>
    </div>
  );
}
