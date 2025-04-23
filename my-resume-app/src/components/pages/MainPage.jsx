import { useNavigate } from "react-router-dom";
import styles from "./index.module.css";

import CardContent, { Card } from "./../ui/card.jsx";
import { Button } from "../ui/button.jsx";

const MainPage = () => {
  const navigate = useNavigate();

  console.log("minh dz");

  return (
    <div className={styles.container}>
      <div className={styles.titleWrapper}>
        <h1 className={styles.title}>Resume Tailor</h1>
        <p className={styles.description}>
          Create a perfectly tailored resume for every job application
        </p>
      </div>

      <Card className="mainPage__CardStyle">
        <div className={styles.cardHeader}>
          <div className={styles.cardTitle}>How it works</div>
          <div className={styles.cardDescription}>
            Our AI-powered tool helps you customize your resume to match job
            descriptions
          </div>
        </div>
        <CardContent className="mainPage__CardContent">
          <div className={styles.cardsWrapper}>
            <div className={styles.stepCard}>
              <div className={styles.stepCircle}>
                <span className={styles.stepNumber}>1</span>
              </div>
              <h3 className={styles.stepTitle}>Enter your details</h3>
              <p className={styles.stepDescription}>
                Fill in your profile and education information
              </p>
            </div>

            <div className={styles.stepCard}>
              <div className={styles.stepCircle}>
                <span className={styles.stepNumber}>2</span>
              </div>
              <h3 className={styles.stepTitle}>Add experiences</h3>
              <p className={styles.stepDescription}>
                Input your work history and projects
              </p>
            </div>

            <div className={styles.stepCard}>
              <div className={styles.stepCircle}>
                <span className={styles.stepNumber}>3</span>
              </div>
              <h3 className={styles.stepTitle}>Get your resume</h3>
              <p className={styles.stepDescription}>
                Receive a tailored resume optimized for your target job
              </p>
            </div>
          </div>

          <Button
            onClick={() => navigate("/apikey")}
            className={styles.mainPage__Button}
          >
            Get Started
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default MainPage;
