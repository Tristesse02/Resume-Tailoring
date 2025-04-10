import SecureKeyInput from "../ui/secureKeyInput";
import { useApiKey } from "../../useContext/ApiKeyProvider";

import styles from "./index.module.css";
import { useNavigate } from "react-router-dom";

const ApikeyPage = () => {
  const navigate = useNavigate();

  const { setApiKey } = useApiKey();

  const handleConfirm = (key) => {
    setApiKey(key);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>API Key Page</h1>
      <p className={styles.description}>
        Enter your OpenAI API key to unlock the full potential of this
        application.
      </p>
      <SecureKeyInput onConfirm={handleConfirm} />
      <div className={styles.buttonContainer}>
        <button onClick={() => navigate("/")} className={styles.buttonRight}>
          Back ⬅
        </button>
        <button
          onClick={() => navigate("/profile")}
          className={styles.buttonRight}
        >
          Next ➡
        </button>
      </div>
    </div>
  );
};

export default ApikeyPage;
// TODO: Update the EntryWrapper page and see if it do update!
