import styles from "./index.module.css";
import { useJobDescription } from "../../useContext/JobDescriptionContext.jsx";

const JobDescriptionInput = () => {
  const { setJobDescription } = useJobDescription(); // use context instead of passing props

  return (
    <div className={styles.jobDescriptionContainer}>
      <h2 className={styles.jobDescriptionTitle}>Job Description</h2>
      <textarea
        className={styles.textarea}
        placeholder="Just paste it here bro ima handle it for u 😭🙏"
        onChange={(e) => setJobDescription(e.target.value)}
      ></textarea>
    </div>
  );
};

export default JobDescriptionInput;
