import styles from "./index.module.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, ArrowRight, User } from "lucide-react";

const ProfilePage = () => {
  const navigate = useNavigate();
  // Load saved profile data from localStorage
  const [formData, setFormData] = useState(() => {
    const savedData = localStorage.getItem("profileData");
    return savedData
      ? JSON.parse(savedData)
      : {
          name: "",
          email: "",
          phone: "",
          linkedin: "",
          github: "",
          languages: "",
          frameworks: "",
        };
  });

  // Update localStorage when formData changes
  useEffect(() => {
    localStorage.setItem("profileData", JSON.stringify(formData));
  }, [formData]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleNextPage = () => {
    // Store data (could be stored in localStorage or context)
    localStorage.setItem("profileData", JSON.stringify(formData));
    navigate("/university-info"); // Move to next page
  };

  const handlePreviousPage = () => {
    navigate("/apikey"); // Move to previous page
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
          <User style={{ height: "20px", width: "20px" }} />
          <h3 className={styles.profileHeaderHeader}>Personal Information</h3>
        </div>
        <p className={styles.profileHeaderTitle}>
          Enter your personal details to include in your resume
        </p>
      </div>
      <form className={styles.form}>
        <div className={styles.formGrid}>
          <div className={styles.fullWidth}>
            <label>Full Name</label>
            <input
              className={styles.profileInput}
              type="text"
              name="name"
              placeholder="John Doe"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Email</label>
            <input
              className={styles.profileInput}
              type="email"
              name="email"
              placeholder="john.doe@example.com"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Phone</label>
            <input
              className={styles.profileInput}
              type="text"
              name="phone"
              placeholder="+1 (555) 123-4567"
              value={formData.phone}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>LinkedIn</label>
            <input
              className={styles.profileInput}
              type="url"
              name="linkedin"
              placeholder="linkedin.com/in/johndoe"
              value={formData.linkedin}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Github</label>
            <input
              className={styles.profileInput}
              type="url"
              name="github"
              placeholder="github.com/johndoe"
              value={formData.github}
              onChange={handleChange}
            />
          </div>
          <div className={styles.fullWidth}>
            <label>Technical Skills</label>
            <textarea
              className={styles.profileTextarea}
              type="text"
              name="languages"
              placeholder="JavaScript, Python, Java, etc."
              value={formData.languages}
              onChange={handleChange}
            />
          </div>
          <div className={styles.fullWidth}>
            <label>Libraries & Frameworks</label>
            <textarea
              className={styles.profileTextarea}
              type="text"
              name="frameworks"
              placeholder="React, Node.js, Express, etc."
              value={formData.frameworks}
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

export default ProfilePage;
