import { useState } from "react";
import styles from "./index.module.css";
import ToggleButton from "../ui/toggleButton";

export default function ResumeForm({
  id,
  indexEntry,
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
      isBulletDescription: true,
      bulletDescription: "",
      numbers: "",
      bulletPoints: "",
      duration: "",
      position: "",
      location: "",
    }
  );

  const [isOn, setIsOn] = useState(true);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newFormData = { ...form, [name]: value };

    // [Issue #1.1]: I dont think this one should be set to empty when users reselect the type!

    // If the type is not project, then clear the project related fields
    // if (name === "type") {
    //   newFormData.duration = value !== "Project" ? form.duration : "";
    //   newFormData.position = value !== "Project" ? form.position : "";
    //   newFormData.location = value !== "Project" ? form.location : "";
    // }

    setForm(newFormData);
    updateFormData(id, newFormData);
  };

  const handleOnToggle = (value) => {
    const newForm = { ...form, isBulletDescription: value };
    setForm(newForm);
    updateFormData(id, newForm);
  };

  const handleOnFocus = (e) => {
    if (!form.bulletDescription.trim()) {
      const newForm = { ...form, bulletDescription: "• " };
      setForm(newForm);
      updateFormData(id, newForm);
    }
  };

  const handleOnBlur = (e) => {
    if (form.bulletDescription.trim() === "•") {
      const newForm = { ...form, bulletDescription: "" };
      setForm(newForm);
      updateFormData(id, newForm);
    }
  };

  const handleOnKeyDown = (e) => {
    const cursorPosition = e.target.selectionStart;
    const cursorEndPosition = e.target.selectionEnd;

    if (cursorPosition !== cursorEndPosition) {
      return;
    }
    
    const value = form.bulletDescription;

    // Prevent Backspace from deleting bullet point
    if (e.key === "Backspace") {
      // Checking if we have only 2 characters left
      if (value.length === 2) {
        e.preventDefault();
      } else {
        const helperDeleteAndMoveCursor = (e, i, j) => {
          e.preventDefault();
          const before = value.slice(cursorPosition + i);
          const after = value.slice(0, cursorPosition - j);

          const updatedValue = `${after}${before}`;
          const newForm = { ...form, bulletDescription: updatedValue };
          setForm(newForm);
          updateFormData(id, newForm);

          // Move cursor to correct position after insert
          setTimeout(() => {
            const el = e.target;
            el.selectionStart = el.selectionEnd = cursorPosition - j;
          }, 0);
        };

        const nextChar = value[cursorPosition];
        const prevChar = value[cursorPosition - 1];
        const prevChar2 = value[cursorPosition - 2];

        if (prevChar2 === "•" && prevChar === " ") {
          helperDeleteAndMoveCursor(e, 0, 3);
        } else if (prevChar === "•") {
          helperDeleteAndMoveCursor(e, 1, 2);
        } else if (nextChar === "•") {
          helperDeleteAndMoveCursor(e, 2, 1);
        }
      }
    }

    // Handle Enter key to add new bullet point
    if (e.key === "Enter") {
      e.preventDefault();
      const before = value.slice(0, cursorPosition);
      const after = value.slice(cursorPosition);

      const updateedValue = `${before}\n• ${after}`;

      const newForm = { ...form, bulletDescription: updateedValue };
      setForm(newForm);
      updateFormData(id, newForm);

      // Move cursor to correct position after insert
      setTimeout(() => {
        const el = e.target;
        el.selectionStart = el.selectionEnd = cursorPosition + 3;
      }, 0);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <ToggleButton isOn={isOn} setIsOn={setIsOn} onToggle={handleOnToggle} />
        <h1 className={styles.title}>Experience {indexEntry}</h1>
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
        {(form.type === "Project" ||
          form.type.includes("Select Type") ||
          isOn) && (
          <input
            name="techStack"
            className={styles.input}
            placeholder="Tech Stack ⚙️🛠️(e.g. React, Node.js, AWS, etc.)"
            value={form.techStack}
            onChange={handleChange}
          />
        )}

        {isOn ? (
          <>
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
          </>
        ) : (
          <textarea
            name="bulletDescription"
            className={styles.textarea}
            placeholder="Bullet points 📝(e.g. Developed a web application using React.js)"
            value={form.bulletDescription}
            onBlur={handleOnBlur}
            onFocus={handleOnFocus}
            onKeyDown={handleOnKeyDown}
            onChange={handleChange}
          />
        )}
      </div>
    </div>
  );
}
