import { Send } from "lucide-react";
import styles from "./index.module.css";

const SubmitButton = ({ submitAllForms, disabled }) => (
  <button
    className={`${styles.submitButton} ${disabled ? styles.disabled : ""}`}
    onClick={submitAllForms}
    disabled={disabled}
  >
    <Send style={{ width: "16px", height: "16px" }} />
    Generate Tailored Resume
  </button>
);

export default SubmitButton;
