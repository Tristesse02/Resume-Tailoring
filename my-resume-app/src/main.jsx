import "./index.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import MainPage from "./components/pages/MainPage";
import ResumeTailor from "./components/pages/ResumeTailor";
import Profile from "./components/pages/Profile";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/resume-tailor" element={<ResumeTailor />} />
      </Routes>
    </Router>
  </StrictMode>
);
