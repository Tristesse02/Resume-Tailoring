import "./index.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Profile from "./components/pages/Profile";
import MainPage from "./components/pages/MainPage";
import ApikeyPage from "./components/pages/ApikeyPage";
import ResumeTailor from "./components/pages/ResumeTailor";
import UniversityInfo from "./components/pages/UniversityInfo";

import { ApiKeyProvider } from "./useContext/ApiKeyProvider";
import PageRequireNav from "./components/utils/PageRequireNav";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <ApiKeyProvider>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/apikey" element={<ApikeyPage />} />
          <Route
            path="/profile"
            element={<PageRequireNav Component={Profile} />}
          />
          <Route
            path="/university-info"
            element={<PageRequireNav Component={UniversityInfo} />}
          />
          <Route
            path="/resume-tailor"
            element={<PageRequireNav Component={ResumeTailor} />}
          />
        </Routes>
      </ApiKeyProvider>
    </Router>
  </StrictMode>
);
