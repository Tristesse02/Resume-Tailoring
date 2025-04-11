import RequireApiKey from "./RequireApiKey";

const PageRequireNav = ({ Component }) => {
  return (
    <RequireApiKey>
      <Component />
    </RequireApiKey>
  );
};

export default PageRequireNav;
