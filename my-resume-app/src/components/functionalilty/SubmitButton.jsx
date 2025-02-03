import styles from "./index.module.css";

const SubmitButton = ({ submitAllForms }) => (
  <button className={styles.submitButton} onClick={submitAllForms}>
    Submit All Forms
  </button>
);

export default SubmitButton;
