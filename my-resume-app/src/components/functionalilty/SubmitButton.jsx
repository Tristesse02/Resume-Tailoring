import styles from "./index.module.css";

const SubmitButton = ({ submitAllForms, disabled }) => (
  <button
    className={`${styles.submitButton} ${disabled ? styles.disabled : ""}`}
    onClick={submitAllForms}
    disabled={disabled}
  >
    Submit All Forms
  </button>
);

export default SubmitButton;
