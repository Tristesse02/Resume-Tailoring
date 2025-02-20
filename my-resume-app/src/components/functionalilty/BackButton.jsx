import styles from "./index.module.css";
import { useNavigate } from "react-router-dom";

const BackButton = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.backButtonContainer}>
      <button
        onClick={() => navigate("/profile")}
        className={styles.backButton}
      >
        ⬅ Back to Profile
      </button>
    </div>
  );
};

export default BackButton;
