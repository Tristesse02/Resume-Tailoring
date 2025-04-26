import { ArrowLeft } from "lucide-react";
import styles from "./index.module.css";
import { useNavigate } from "react-router-dom";

const BackButton = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.backButtonContainer}>
      <button
        onClick={() => navigate("/university-info")}
        className={styles.buttonLeft}
      >
        <ArrowLeft className={styles.buttonArrowLeft} />
        Back to Education
      </button>
    </div>
  );
};

export default BackButton;
