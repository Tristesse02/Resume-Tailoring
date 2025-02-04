import { createContext, useContext, useState } from "react";

// 1. Create the context
const JobDescriptionContext = createContext();

// 2. Create a provider component
export function JobDescriptionProvider({ children }) {
  const [jobDescription, setJobDescription] = useState("");

  return (
    <JobDescriptionContext.Provider
      value={{ jobDescription, setJobDescription }}
    >
      {children}
    </JobDescriptionContext.Provider>
  );
}

// 3. Create a custom hook to use the context
export function useJobDescription() {
  const context = useContext(JobDescriptionContext);
  if (!context) {
    throw new Error(
      "useJobDescription must be used within a JobDescriptionProvider"
    );
  }
  return context;
}
