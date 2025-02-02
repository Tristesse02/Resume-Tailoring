import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import ResumeForm from "./ResumeForm.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center", // This centers vertically
        height: "100vh", // Ensures it takes full height
      }}
    >
      <ResumeForm />
    </div>
  </StrictMode>
);
