import { useState } from "react";
import styles from "./index.module.css";

export default function ResumeForm({ id, formData, updateFormData }) {
  const [form, setForm] = useState(
    formData || {
      name: "",
      type: "",
      techStack: "",
      description: "",
      numbers: "",
    }
  );

  const handleChange = (e) => {
    const newFormData = { ...form, [e.target.name]: e.target.value };
    setForm(newFormData);
    updateFormData(id, newFormData);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Experience {id}</h1>

      <div className={styles.formGroup}>
        <input
          name="name"
          className={styles.input}
          placeholder="Job/Project Name 🤔"
          value={form.name}
          onChange={handleChange}
        />
        <input
          name="type"
          className={styles.input}
          placeholder="Type 💜(Intern, Job, Project) (you must choose from any of the three ☹️)"
          value={form.type}
          onChange={handleChange}
        />
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
      </div>
    </div>
  );
}
