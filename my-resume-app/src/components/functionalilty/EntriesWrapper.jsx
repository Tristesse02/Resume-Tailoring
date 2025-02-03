import { useState } from "react";
import AddEntry from "./AddEntry.jsx";
import styles from "./index.module.css";
import ResumeForm from "./ResumeForm.jsx";
import SubmitButton from "./SubmitButton.jsx";

const EntriesWrapper = () => {
  const [entries, setEntries] = useState([
    {
      id: 1,
      formData: {
        name: "",
        type: "",
        techStack: "",
        description: "",
        numbers: "",
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
    // TODO: modify the content in the form to match a kind of json format
    // then send this json to a backend that we will build now
    let obj = entries.reduce((acc, cur) => {
      if (cur.formData.type === "Project") {
        console.log("you read");
        if (!acc.hasOwnProperty("Personal Projects")) {
          acc["Personal Projects"] = [];
        }
        acc["Personal Projects"].push({
          title: cur.formData.name,
          description:
            cur.formData.type +
            "\n" +
            cur.formData.techStack +
            "\n" +
            cur.formData.description +
            "\n" +
            cur.formData.numbers,
        });
      } else {
        console.log("bro come one");
        if (!acc.hasOwnProperty("Work Experience")) {
          acc["Work Experience"] = [];
          console.log("ye?");
        }
        acc["Work Experience"].push({
          title: cur.formData.name,
          description:
            cur.formData.type +
            "\n" +
            cur.formData.techStack +
            "\n" +
            cur.formData.description +
            "\n" +
            cur.formData.numbers,
        });
      }
      return acc;
    }, {});

    console.log(obj);

    console.log("Submitted Forms: ", JSON.stringify(obj)); // successfully formatting to json and ready to send to backend
  };

  return (
    <div className={styles.containerWrapper}>
      {entries.map((entry) => (
        <ResumeForm
          key={entry.id}
          id={entry.id}
          formData={entry.formData}
          updateFormData={updateFormData}
        /> // Pass unique ID
      ))}
      <AddEntry onClick={addNewEntry} />
      <SubmitButton submitAllForms={submitAllForms} />
    </div>
  );
};

export default EntriesWrapper;
