/**
 * @typedef {import('../types/EntriesWrapper.js').ResumeData} ResumeData
 * @typedef {import('../types/EntriesWrapper.js').ResumeEntry} ResumeEntry
 * @typedef {import('../types/EntriesWrapper.js').ResumeRequest} ResumeRequest
 */
import AddEntry from "./AddEntry.jsx";
import styles from "./index.module.css";
import ResumeForm from "./ResumeForm.jsx";
import SubmitButton from "./SubmitButton.jsx";

import { v4 as uuidv4 } from "uuid";
import { useState, useEffect } from "react";

import { useApiKey } from "../../useContext/ApiKeyProvider.jsx";
import { useJobDescription } from "../../useContext/JobDescriptionContext.jsx";

const LOCAL_STORAGE_KEY = "resume_entries";

const EntriesWrapper = () => {
  const { jobDescription } = useJobDescription(); // use context instead of passing props
  const [entries, setEntries] = useState([]);
  const { apiKey } = useApiKey(); // use context instead of passing props

  useEffect(() => {
    const savedEntries = localStorage.getItem(LOCAL_STORAGE_KEY);

    if (savedEntries) {
      setEntries(JSON.parse(savedEntries));
    } else {
      setEntries([
        {
          id: id,
          formData: {
            name: "",
            type: "",
            techStack: "",
            bulletDescription: "",
            isBulletDescription: true,
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
    const uniqueId = uuidv4();

    setEntries([
      ...entries,
      {
        id: uniqueId,
        formData: {
          name: "",
          type: "",
          techStack: "",
          bulletDescription: "",
          isBulletDescription: true,
          description: "",
          numbers: "",
          bulletPoints: "",
        },
      },
    ]); // Create unique ID
  };

  const removeEntry = (id) => {
    setEntries((prevEntries) => prevEntries.filter((entry) => entry.id !== id));
  };

  const updateFormData = (id, newFormData) => {
    setEntries((prevEntries) =>
      prevEntries.map((entry) =>
        entry.id === id
          ? {
              ...entry,
              formData: {
                ...newFormData,
                // [Issue #1.3]: Do we really have to do this? Like setting it to "" when the type is not project?
                // duration:
                //   newFormData.type !== "Project" ? newFormData.duration : "",
                // position:
                //   newFormData.type !== "Project" ? newFormData.position : "",
                // location:
                //   newFormData.type !== "Project" ? newFormData.location : "",
              },
            }
          : entry
      )
    );
  };

  // /** @type {ResumeEntry} */
  const submitAllForms = () => {
    // Retrieve profile data from local storage
    const storedProfileData = localStorage.getItem("profileData");
    const profileData = storedProfileData ? JSON.parse(storedProfileData) : {};

    const storedUniversityData = localStorage.getItem("universityData");
    const universityData = storedUniversityData
      ? JSON.parse(storedUniversityData)
      : {};

    // Process experiences and projects
    /** @type {ResumeData} */
    let resumeData = entries.reduce((acc, cur, idx) => {
      const category =
        cur.formData.type === "Project"
          ? "personal_projects"
          : "work_experiences";
      if (!acc[category]) acc[category] = [];
      let entryData = {
        order: idx,
        title: cur.formData.name,
        type: cur.formData.type,
        techStack: cur.formData.techStack.split(",").map((e) => e.trim()), // Convert to array of strings of tech stacks
        description: cur.formData.description,
        bulletDescription: cur.formData.bulletDescription,
        isBulletDescription: cur.formData.isBulletDescription,
        quantifiableMetrics: cur.formData.numbers,
        bulletPoints: cur.formData.bulletPoints,
      };

      // [Issue #1.2]: Although not clearing the fields when switching types, the data
      if (cur.formData.type !== "Project") {
        entryData.duration = cur.formData.duration;
        entryData.position = cur.formData.position;
        entryData.location = cur.formData.location;
      }

      acc[category].push(entryData);

      return acc;
    }, {});

    /** @type {ResumeRequest} */
    let requestedBody = {
      profile_data: profileData,
      university_data: universityData,
      resume_data: resumeData,
      job_description: jobDescription,
    };

    console.log("dzai vlon", requestedBody); // TODO: testing purposes

    fetch("https://resume-backend-65ia.onrender.com/tailor-resume", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
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

  // Check if all forms are valid
  const isFormValid = () => {
    return entries.every((entry) => entry.formData.type);
  };

  // Function to download PDF from backend
  const downloadPDF = () => {
    fetch("https://resume-backend-65ia.onrender.com/download-pdf")
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
      {entries.map((entry, idx) => (
        <ResumeForm
          key={entry.id}
          id={entry.id}
          indexEntry={idx + 1}
          formData={entry.formData}
          updateFormData={updateFormData}
          removeEntry={removeEntry}
        /> // Pass unique I FD
      ))}
      <div className={styles.buttonContainer}>
        <AddEntry onClick={addNewEntry} />
        <SubmitButton
          submitAllForms={submitAllForms}
          disabled={!isFormValid()}
        />
      </div>
    </div>
  );
};

export default EntriesWrapper;
