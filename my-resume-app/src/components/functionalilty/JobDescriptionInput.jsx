import styles from "./index.module.css";
import { useJobDescription } from "../../useContext/JobDescriptionContext.jsx";
import { Briefcase } from "lucide-react";

const JobDescriptionInput = () => {
  const { setJobDescription } = useJobDescription(); // use context instead of passing props

  return (
    <div className={styles.profileContainer}>
      <div className={styles.profileHeaderContainer}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            justifyContent: "flex-start",
            marginBottom: "12px",
          }}
        >
          <Briefcase style={{ height: "20px", width: "20px" }} />
          <h3 className={styles.profileHeaderHeader}>Job Description</h3>
        </div>
        <textarea
          className={styles.profileTextarea}
          placeholder="Paste the job description here to optimize your resume"
          onChange={(e) => setJobDescription(e.target.value)}
        />
      </div>
    </div>
  );
};

{
  /* <div className={styles.profileContainer}>
  <div className={styles.profileHeaderContainer}>
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: "8px",
        justifyContent: "flex-start",
      }}
    >
      <User style={{ height: "20px", width: "20px" }} />
      <h3 className={styles.profileHeaderHeader}>Personal Information</h3>
    </div>
    <p className={styles.profileHeaderTitle}>
      Enter your personal details to include in your resume
    </p>
  </div>
</div>; */
}

export default JobDescriptionInput;
