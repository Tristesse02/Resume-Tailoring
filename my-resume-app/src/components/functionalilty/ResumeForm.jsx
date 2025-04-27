import { useState } from "react";
import styles from "./index.module.css";
import { LucideX, Pencil, Sparkles } from "lucide-react";

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

  const [isOn, setIsOn] = useState(formData?.isBulletDescription ?? true);

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

  const handleChangeTailor = () => {
    const newValue = !isOn;
    setIsOn(newValue);
    handleOnToggle(newValue);
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
    <div className={styles.profileContainer} style={{ position: "relative" }}>
      <div className={styles.profileHeaderContainer}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            justifyContent: "flex-start",
            marginBottom: "12px",
          }}
        >
          <button
            onClick={handleChangeTailor}
            className={
              isOn ? styles.toggleTailorStar : styles.toggleTailorPencil
            }
          >
            {isOn ? (
              <Sparkles
                className={styles.sparkles}
                style={{
                  height: "20px",
                  width: "20px",
                }}
              />
            ) : (
              <Pencil
                className={styles.pencil}
                style={{ height: "20px", width: "20px" }}
              />
            )}
          </button>
          <h3 className={styles.profileHeaderHeader}>
            Experience {indexEntry}
          </h3>
          <button
            className={styles.removeButton}
            onClick={() => id && removeEntry(id)}
          >
            <LucideX className={styles.deleteExperienceEntry} />
          </button>
        </div>
      </div>

      <div className={styles.experienceEntryFormGrid}>
        <div className={styles.widthSpan3}>
          <label>Name</label>
          <input
            name="name"
            className={styles.profileInput}
            placeholder="Job/Project Name"
            value={form.name}
            onChange={handleChange}
          />
        </div>

        <div className={styles.widthSpan3}>
          <label>Type</label>
          <select
            name="type"
            className={styles.profileInput}
            value={form.type}
            onChange={handleChange}
          >
            <option value="">Select Type 💜</option>
            <option value="Job">Job</option>
            <option value="Project">Project</option>
          </select>
        </div>

        {form.type !== "Project" && (
          <>
            <div className={styles.widthSpan2}>
              <label>Duration</label>
              <input
                name="duration"
                className={styles.profileInput}
                placeholder="Jun 2024 -- Aug 2024"
                value={form.duration}
                onChange={handleChange}
              />
            </div>

            <div className={styles.widthSpan2}>
              <label>Position</label>
              <input
                name="position"
                className={styles.profileInput}
                placeholder="Software Engineer Intern"
                value={form.position}
                onChange={handleChange}
              />
            </div>

            <div className={styles.widthSpan2}>
              <label>Location</label>
              <input
                name="location"
                className={styles.profileInput}
                placeholder="Remote, US"
                value={form.location}
                onChange={handleChange}
              />
            </div>
          </>
        )}

        {(form.type === "Project" ||
          form.type.includes("Select Type") ||
          isOn) && (
          <div className={styles.widthSpanFull}>
            <label>Tech Stack</label>
            <input
              name="techStack"
              className={styles.profileInput}
              placeholder="React, Node.js, AWS, etc."
              value={form.techStack}
              onChange={handleChange}
            />
          </div>
        )}

        {isOn ? (
          <>
            <div className={styles.widthSpanFull}>
              <label>Description</label>
              <textarea
                name="description"
                className={styles.profileTextarea}
                placeholder="Describe your experience in detail"
                value={form.description}
                onChange={handleChange}
              />
            </div>
            <div className={styles.widthSpanFull}>
              <label>Quantifiable Results</label>
              <input
                name="numbers"
                className={styles.profileInput}
                placeholder="Increased performance by 40%"
                value={form.numbers}
                onChange={handleChange}
              />
            </div>
            <div className={styles.widthSpanFull}>
              <label>Bullet Points</label>
              <input
                name="bulletPoints"
                className={styles.profileInput}
                placeholder="Number of bullet points (3-5)"
                value={form.bulletPoints}
                onChange={handleChange}
              />
            </div>
          </>
        ) : (
          <div className={styles.widthSpanFull}>
            <label>Description</label>
            <textarea
              name="bulletDescription"
              className={styles.profileTextarea}
              placeholder="• Developed a web application using React.js"
              value={form.bulletDescription}
              onBlur={handleOnBlur}
              onFocus={handleOnFocus}
              onKeyDown={handleOnKeyDown}
              onChange={handleChange}
            />
          </div>
        )}
      </div>
    </div>
  );
}
