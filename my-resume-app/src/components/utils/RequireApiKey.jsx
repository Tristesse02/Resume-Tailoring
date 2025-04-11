import { Navigate } from "react-router-dom";
import { useApiKey } from "../../useContext/ApiKeyProvider";

const RequireApiKey = ({ children }) => {
  const { apiKey } = useApiKey();

  if (!apiKey) {
    return <Navigate to="/apikey" replace />;
  }

  return children;
};

export default RequireApiKey;
