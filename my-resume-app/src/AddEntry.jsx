import { useState } from "react";
import styles from "./ResumeForm.module.css";

const AddEntry = ({ onClick }) => {
  return (
    <button className={styles.button} onClick={onClick}>
      Add Entry
    </button>
  );
};

export default AddEntry;
