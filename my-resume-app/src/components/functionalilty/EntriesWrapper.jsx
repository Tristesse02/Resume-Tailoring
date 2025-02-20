/**
 * @typedef {import('../types/EntriesWrapper.js').ResumeData} ResumeData
 * @typedef {import('../types/EntriesWrapper.js').ResumeEntry} ResumeEntry
 * @typedef {import('../types/EntriesWrapper.js').ResumeRequest} ResumeRequest
 */
import AddEntry from "./AddEntry.jsx";
import styles from "./index.module.css";
import ResumeForm from "./ResumeForm.jsx";
import SubmitButton from "./SubmitButton.jsx";

import { useState, useEffect } from "react";
import { useJobDescription } from "../../useContext/JobDescriptionContext.jsx";

const LOCAL_STORAGE_KEY = "resume_entries";

const EntriesWrapper = () => {
  const { jobDescription } = useJobDescription(); // use context instead of passing props
  const [entries, setEntries] = useState([]);

  useEffect(() => {
    const savedEntries = localStorage.getItem(LOCAL_STORAGE_KEY);

    if (savedEntries) {
      setEntries(JSON.parse(savedEntries));
    } else {
      setEntries([
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
      ]);
    }
  }, []);

  useEffect(() => {
    if (entries.length > 0) {
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(entries));
    }
  }, [entries]);

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

  // /** @type {ResumeEntry} */
  const submitAllForms = () => {
    // Retrieve profile data from local storage
    const storedProfileData = localStorage.getItem("profileData");
    const profileData = storedProfileData ? JSON.parse(storedProfileData) : {};

    // Process experiences and projects
    /** @type {ResumeData} */
    let resumeData = entries.reduce((acc, cur) => {
      const category =
        cur.formData.type === "Project"
          ? "personal_projects"
          : "work_experiences";
      if (!acc[category]) acc[category] = [];
      acc[category].push({
        title: cur.formData.name,
        type: cur.formData.type,
        techStack: cur.formData.techStack.split(",").map((e) => e.trim()), // Convert to array of strings of tech stacks
        description: cur.formData.description,
        quantifiableMetrics: cur.formData.numbers,
        bulletPoints: cur.formData.bulletPoints,
      });

      return acc;
    }, {});

    /** @type {ResumeRequest} */
    let requestedBody = {
      profile_data: profileData,
      resume_data: resumeData,
      job_description: jobDescription,
    };

    console.log(requestedBody); // TODO: testing purposes

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
          console.log("Resume tailored successfully:", data.data);
          downloadPDF(); // Trigger PDF download after success
        } else {
          console.error("Error:", data.error);
        }
      })
      .catch((error) => console.error("Error:", error));
  };

  // Function to download PDF from backend
  const downloadPDF = () => {
    fetch("http://localhost:5000/download-pdf")
      .then((response) => response.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "generated_resume.pdf"; // Name of the downloaded file
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      })
      .catch((error) => console.error("Failed to download PDF:", error));
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
      <div className={styles.buttonContainer}>
        <AddEntry onClick={addNewEntry} />
        <SubmitButton submitAllForms={submitAllForms} />
      </div>
    </div>
  );
};

export default EntriesWrapper;
