import SecureKeyInput from "../ui/secureKeyInput";
import { useApiKey } from "../../useContext/ApiKeyProvider";

import styles from "./index.module.css";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, ArrowRight, KeyRound } from "lucide-react";

const ApikeyPage = () => {
  const navigate = useNavigate();

  const { setApiKey } = useApiKey();

  const handlePreviousPage = () => navigate("/");

  const handleNextPage = () => navigate("/profile");

  const handleConfirm = (key) => {
    setApiKey(key);
  };

  return (
    <div className={styles.profileContainer}>
      <div className={styles.profileHeaderContainer}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            justifyContent: "flex-start",
          }}
        >
          <KeyRound style={{ height: "20px", width: "20px" }} />
          <h3 className={styles.profileHeaderHeader}>API Key Configuration</h3>
        </div>
        <p className={styles.profileHeaderTitle}>
          Enter your OpenAI API key to unlock the full potential of this
          application.
        </p>
      </div>
      <SecureKeyInput onConfirm={handleConfirm} />
      <div className={styles.buttonContainer}>
        <button onClick={handlePreviousPage} className={styles.buttonLeft}>
          <ArrowLeft className={styles.buttonArrowLeft} />
          Back
        </button>
        <button onClick={handleNextPage} className={styles.buttonRight}>
          Next
          <ArrowRight className={styles.buttonArrowRight} />
        </button>
      </div>
    </div>
  );
};

export default ApikeyPage;
// TODO: Update the EntryWrapper page and see if it do update!
