import { useNavigate } from "react-router-dom";
import styles from "./index.module.css";

const MainPage = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Welcome to Resume Tailor 🦙</h1>
      <p className={styles.description}>
        This tool helps you tailor your resume to match job descriptions
        effortlessly. Paste the job description, add your experiences, and get
        optimized suggestions!
      </p>
      <button
        onClick={() => navigate("/profile")}
        className={styles.buttonRight}
      >
        Next ➡
      </button>
    </div>
  );
};

export default MainPage;
