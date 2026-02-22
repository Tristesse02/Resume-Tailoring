import styles from "./index.module.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, ArrowRight, GraduationCap } from "lucide-react";

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
          gpa: "",
          graduate: "",
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
    <div className={styles.profileContainer}>
      <div className={styles.profileHeaderContainer}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            justifyContent: "flex-start",
          }}
        >
          <GraduationCap style={{ height: "20px", width: "20px" }} />
          <h3 className={styles.profileHeaderHeader}>Education Information</h3>
        </div>
        <p className={styles.profileHeaderTitle}>
          Enter your educational background to include in your resume
        </p>
      </div>
      <form className={styles.form}>
        <div className={styles.educationFormGrid}>
          <div className={styles.fullWidthSpan3}>
            <label>University</label>
            <input
              className={styles.profileInput}
              type="text"
              name="university"
              placeholder="Stanford University"
              value={formData.university}
              onChange={handleChange}
              required
            />
          </div>
          <div className={styles.fullWidthSpan3}>
            <label>Degree</label>
            <input
              className={styles.profileInput}
              type="text"
              name="degree"
              placeholder="B.S. Computer Science"
              value={formData.degree}
              onChange={handleChange}
              required
            />
          </div>
          <div className={styles.fullWidthSpan2}>
            <label>GPA</label>
            <input
              className={styles.profileInput}
              type="text"
              name="gpa"
              placeholder="3.8"
              value={formData.gpa}
              onChange={handleChange}
              required
            />
          </div>
          <div className={styles.fullWidthSpan2}>
            <label>Graduation Year</label>
            <input
              className={styles.profileInput}
              type="text"
              name="graduate"
              placeholder="2025"
              value={formData.graduate}
              onChange={handleChange}
              required
            />
          </div>
          <div className={styles.fullWidthSpan2}>
            <label>Location</label>
            <input
              className={styles.profileInput}
              type="text"
              name="location"
              placeholder="Stanford, CA"
              value={formData.location}
              onChange={handleChange}
            />
          </div>
          <div className={styles.fullWidthSpan6}>
            <label>Relevant Courses</label>
            <textarea
              className={styles.profileTextarea}
              type="text"
              name="courses"
              placeholder="Data Structures, Algorithms, Machine Learning, etc."
              value={formData.courses}
              onChange={handleChange}
            />
          </div>
        </div>
      </form>
      <div className={styles.buttonContainer}>
        <button onClick={handlePreviousPage} className={styles.buttonLeft}>
          <ArrowLeft className={styles.buttonArrowLeft} />
          Back
        </button>
        <button onClick={handleNextPage} className={styles.buttonRight}>
          Next
          <ArrowRight className={styles.buttonArrowRight} />
        </button>
      </div>
    </div>
  );
};

export default UniversityInfo;
