import { useState } from "react";
import AddEntry from "./AddEntry.jsx";
import styles from "./index.module.css";
import ResumeForm from "./ResumeForm.jsx";
import SubmitButton from "./SubmitButton.jsx";
import { useJobDescription } from "../../useContext/JobDescriptionContext.jsx";

const EntriesWrapper = () => {
  const { jobDescription } = useJobDescription(); // use context instead of passing props
  const [entries, setEntries] = useState([
    {
      id: 1,
      formData: {
        name: "",
        type: "",
        techStack: "",
        description: "",
        numbers: "",
        bulletPoints: "",
      },
    },
  ]); // Start with one form

  const addNewEntry = () => {
    setEntries([
      ...entries,
      {
        id: entries.length + 1,
        formData: {
          name: "",
          type: "",
          techStack: "",
          description: "",
          numbers: "",
          bulletPoints: "",
        },
      },
    ]); // Create unique ID
  };

  const updateFormData = (id, newFormData) => {
    setEntries((prevEntries) =>
      prevEntries.map((entry) =>
        entry.id === id ? { ...entry, formData: newFormData } : entry
      )
    );
  };

  const submitAllForms = () => {
    let resumeData = entries.reduce((acc, cur) => {
      const category =
        cur.formData.type === "Project"
          ? "Personal Projects"
          : "Work Experience";
      if (!acc[category]) acc[category] = [];

      acc[category].push({
        title: cur.formData.name,
        description: `${cur.formData.type}\nTech-stack:${cur.formData.techStack}\nDescription:${cur.formData.description}\nQuantifiable Metrics:${cur.formData.numbers}Number of Bullet Points:${cur.formData.bulletPoints}`,
      });

      return acc;
    }, {});

    // TODO: Replace data mock with real job description
    let requestedBody = {
      resume_data: resumeData,
      job_description: jobDescription,
    };

    fetch("http://localhost:5000/tailor-resume", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestedBody),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.data) {
          console.log("Generated Resume:", data.data);
        } else {
          console.error("Error:", data.error);
        }
      })
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className={styles.containerWrapper}>
      {entries.map((entry) => (
        <ResumeForm
          key={entry.id}
          id={entry.id}
          formData={entry.formData}
          updateFormData={updateFormData}
        /> // Pass unique I FD
      ))}
      <AddEntry onClick={addNewEntry} />
      <SubmitButton submitAllForms={submitAllForms} />
    </div>
  );
};

export default EntriesWrapper;
