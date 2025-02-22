import styles from "./index.module.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const UniversityInfo = () => {
  const navigate = useNavigate();
  // Load saved profile data from localStorage
  const [formData, setFormData] = useState(() => {
    const savedData = localStorage.getItem("universityData");
    return savedData
      ? JSON.parse(savedData)
      : {
          university: "",
          degree: "",
          graduation: "",
          location: "",
          courses: "",
        };
  });

  // Update localStorage when formData changes
  useEffect(() => {
    localStorage.setItem("universityData", JSON.stringify(formData));
  }, [formData]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleNextPage = () => {
    // Store data (could be stored in localStorage or context)
    localStorage.setItem("universityData", JSON.stringify(formData));
    navigate("/resume-tailor"); // Move to next page
  };

  const handlePreviousPage = () => {
    navigate("/profile"); // Move to previous page
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Profile Information</h1>
      <form className={styles.form}>
        <input
          className={styles.input}
          type="text"
          name="university"
          placeholder="University"
          value={formData.university}
          onChange={handleChange}
          required
        />
        <input
          className={styles.input}
          type="text"
          name="degree"
          placeholder="Degree"
          value={formData.degree}
          onChange={handleChange}
          required
        />
        <input
          className={styles.input}
          type="text"
          name="graduation"
          placeholder="Graduation Year"
          value={formData.graduation}
          onChange={handleChange}
          required
        />
        <input
          className={styles.input}
          type="text"
          name="location"
          placeholder="University Location"
          value={formData.location}
          onChange={handleChange}
        />
        <textarea
          className={styles.textarea}
          type="text"
          name="courses"
          placeholder="Courses"
          value={formData.courses}
          onChange={handleChange}
        />
      </form>
      <div className={styles.buttonContainer}>
        <button onClick={handlePreviousPage} className={styles.buttonLeft}>
          Back ⬅
        </button>
        <button onClick={handleNextPage} className={styles.buttonRight}>
          Next ➡
        </button>
      </div>
    </div>
  );
};

export default UniversityInfo;
