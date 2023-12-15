import React, {useState} from "react";
import Select from "react-select";
import Header from "../components/header.js"
import { useNavigate } from "react-router-dom";
import "../style/interviewai.css"
import { Octokit } from "octokit";

const joboption=[
    {value: "01", label: "프론트엔드 개발"},
    {value: "02", label: "백엔드 개발"},
    {value: "03", label: "풀스택 개발"},
    {value: "04", label: "AI 개발"},
    {value: "05", label: "게임 개발"},
];

function InterviewAi(){

  const octokit = new Octokit({
    auth: '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'
  });

  const JobcustomSelect ={
      control: (provided) =>({
        ...provided,
        width: "250px",
        paddingTop: "5px",
        paddingBottom: "5px",
        paddingLeft: "10px",
        border: '1px #DDDDDD solid',
        justifyContent: 'flex-start',
        alignItems: 'center',
        display: 'inline-flex',
        cursor: 'pointer'
      }),
      option: (provided, state) => ({
        ...provided,
        backgroundColor: state.isSelected ? "#4285F4" : state.isFocused ? "#ACCBFF": "#fff",
        color: state.isSelected ? "#fff" : "#000",
        cursor: 'pointer'
      }),
      indicatorSeparator: (provided) => ({
        ...provided,
        display: "none"
      }),
    }
  const navigate = useNavigate();
  const navigateToOutput = () => {
    navigate("/interviewai/output")
  };

  const [AiSelection, setSelectJobOption] = useState(null);
  const Jobhandler = (AiSelection) => {
    setSelectJobOption(AiSelection);
    console.log(AiSelection);
  };

  const [repos, setRepos] = useState([]);
  const [isRepoModalOpen, setIsRepoModalOpen] = useState(false);
  const [selectedRepos, setSelectedRepos] = useState([]);

  const fetchRepos = async () => {
    try{
      const response = await octokit.request('GET /user/repos');
      setRepos(response.data);
      setIsRepoModalOpen(true);
    }
    catch(error){
      console.error('Error fetching repositories:', error);
    }
  };

  const handleIncludeButtonClick = () => {
    fetchRepos();
  }

  const renderRepoModal = () => {
    if(!isRepoModalOpen) return null;

    return(
      <div className="modalOverlay">
        <div className="modalContent">
          <div className="modalHeader">
            <h2>저장소 선택</h2>
            <button onClick={() => setIsRepoModalOpen(false)}>닫기</button>
          </div>
          <div className="modalBody">
            {repos.map(repo => (
              <div key={repo.id} className="modalItem" onClick={() => selectRepo(repo)}>
                {repo.full_name}
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  const selectRepo = (repo) => {
    setSelectedRepos(prevRepos => [...prevRepos, repo]);
    console.log("Selected repo:", repo.name);
    setIsRepoModalOpen(false);
  };

  const renderPopolList = () => {
    return selectedRepos.map((repo, index) => (
      <div className="PopolItem" key={index}>
        <div className="RepositoryName">{repo.full_name}</div>
      </div>
    ));
  };

  return(
      <div className="InterviewAibody">
          <Header/>
          <div className="AiSubtitleBox">
            <div className="AiSubtitleText">포트폴리오 제출</div>
          </div>
          <div className="AiSelectFrame">
            <div className="AiJobSelectFrame">
              <div className="JobSelectTitle">직무</div>
              <Select
                  className="Selection"
                  classNamePrefix="select"
                  defaultValue={joboption[0]}
                  name="Job"
                  options={joboption}
                  isSearchable={false}
                  styles={JobcustomSelect}
                  onChange={Jobhandler}
              />
            </div>
            {renderRepoModal()}
            <div className="PopolIncludeList">
              <div className="PopolList">
                {renderPopolList()}
              </div>
              <button className="IncludeButton" onClick={handleIncludeButtonClick}>
                <div className="ButtonTypo">+ 포트폴리오 추가하기</div>
              </button>
            </div>
            <button className="OutputButton" onClick={navigateToOutput}>
              <div className="ButtonTypo">제출하기</div>
            </button>
          </div>
      </div>
  )
}

export default InterviewAi;