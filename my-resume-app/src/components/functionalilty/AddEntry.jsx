import styles from "./index.module.css";

const AddEntry = ({ onClick }) => {
  return (
    <button className={styles.button} onClick={onClick}>
      Add More Experience
    </button>
  );
};

export default AddEntry;
