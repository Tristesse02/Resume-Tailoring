import { useState } from "react";
import styles from "./index.module.css";
import ToggleButton from "../ui/toggleButton";

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
      duration: "",
      position: "",
      location: "",
    }
  );

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newFormData = { ...form, [name]: value };

    // If the type is not project, then clear the project related fields
    if (name === "type") {
      newFormData.duration = value !== "Project" ? form.duration : "";
      newFormData.position = value !== "Project" ? form.position : "";
      newFormData.location = value !== "Project" ? form.location : "";
    }

    setForm(newFormData);
    updateFormData(id, newFormData);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <ToggleButton />
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

        {form.type !== "Project" && (
          <>
            <input
              name="duration"
              className={styles.input}
              placeholder="Duration (Jun 2024 -- Aug 2024)"
              value={form.duration}
              onChange={handleChange}
            />
            <input
              name="position"
              className={styles.input}
              placeholder="Position (e.g. Software Engineer Intern)"
              value={form.position}
              onChange={handleChange}
            />
            <input
              name="location"
              className={styles.input}
              placeholder="Location (e.g. Remote, US)"
              value={form.location}
              onChange={handleChange}
            />
          </>
        )}

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
