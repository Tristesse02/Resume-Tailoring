import "./index.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Header from "./components/functionalilty/Header.jsx";
import EntriesWrapper from "./components/functionalilty/EntriesWrapper.jsx";
import PageContainer from "./components/functionalilty/PageContainer.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <PageContainer>
      <Header />
      <EntriesWrapper />
    </PageContainer>
  </StrictMode>
);
