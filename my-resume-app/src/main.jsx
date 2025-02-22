import "./index.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Profile from "./components/pages/Profile";
import MainPage from "./components/pages/MainPage";
import ResumeTailor from "./components/pages/ResumeTailor";
import UniversityInfo from "./components/pages/UniversityInfo";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/university-info" element={<UniversityInfo />} />
        <Route path="/resume-tailor" element={<ResumeTailor />} />
      </Routes>
    </Router>
  </StrictMode>
);
