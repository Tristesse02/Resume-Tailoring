import { LucideCirclePlus } from "lucide-react";
import styles from "./index.module.css";

const AddEntry = ({ onClick }) => {
  return (
    <button className={styles.addMoreExperienceButton} onClick={onClick}>
      <LucideCirclePlus style={{width: "16px", height: "16px"}}/>
      Add More Experience
    </button>
  );
};

export default AddEntry;
