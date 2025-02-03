const PageContainer = ({ children }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "flex-start",
        width: "100%",
        height: "100vh",
        padding: "2rem 0",  // Prevents content from touching the top
      }}
    >
      {children}
    </div>
  );
};

export default PageContainer;
