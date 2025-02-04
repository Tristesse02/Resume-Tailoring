import React from "react";
import styles from "./index.module.css";
import { JobDescriptionProvider } from "../../useContext/JobDescriptionContext.jsx";

const PageContainer = ({ children }) => {
  return (
    <JobDescriptionProvider>
      <div className={styles.pageContainer}>{children}</div>
    </JobDescriptionProvider>
  );
};

export default PageContainer;
