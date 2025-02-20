import Header from "../functionalilty/Header";
import BackButton from "../functionalilty/BackButton";
import PageContainer from "../functionalilty/PageContainer";
import EntriesWrapper from "../functionalilty/EntriesWrapper";
import JobDescriptionInput from "../functionalilty/JobDescriptionInput";

const ResumeTailor = () => {
  return (
    <PageContainer>
      <BackButton />
      <Header />
      <JobDescriptionInput />
      <EntriesWrapper />
    </PageContainer>
  );
};

export default ResumeTailor;
