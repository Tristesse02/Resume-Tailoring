import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./index.module.css";

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
    <div className={styles.container}>
      <h1 className={styles.title}>Profile Information</h1>
      <form className={styles.form}>
        <input
          className={styles.input}
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          className={styles.input}
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          className={styles.input}
          type="text"
          name="phone"
          placeholder="Phone"
          value={formData.phone}
          onChange={handleChange}
          required
        />
        <input
          className={styles.input}
          type="url"
          name="linkedin"
          placeholder="LinkedIn Profile Link"
          value={formData.linkedin}
          onChange={handleChange}
        />
        <input
          className={styles.input}
          type="url"
          name="github"
          placeholder="GitHub Profile Link"
          value={formData.github}
          onChange={handleChange}
        />
        <textarea
          className={styles.textarea}
          type="text"
          name="languages"
          placeholder="Technical Skills (comma-separated)"
          value={formData.languages}
          onChange={handleChange}
        />
        <textarea
          className={styles.textarea}
          type="text"
          name="frameworks"
          placeholder="Libraries/Frameworks (comma-separated)"
          value={formData.frameworks}
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

export default ProfilePage;
