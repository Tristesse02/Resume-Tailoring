import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import EntriesWrapper from "./EntriesWrapper.jsx";
import PageContainer from "./PageContainer.jsx";
import Header from "./Header.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <PageContainer>
      <Header />
      <EntriesWrapper />
    </PageContainer>
  </StrictMode>
);
