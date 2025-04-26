import { Sparkles } from "lucide-react";
import styles from "./index.module.css";

const Header = () => {
  return (
    <>
      <div className={styles.resTailHeaderContainer}>
        <h1 style={{ fontSize: "30px", margin: "0" }}>Resume Tailor</h1>
        <Sparkles className={styles.sparkles} />
      </div>
      <p className={styles.resTailHeaderDescription}>
        Let us optimize your resume for job applications with AI-powered
        tailoring
      </p>
    </>
  );
};

export default Header;
