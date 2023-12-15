import React, {useState, useEffect} from "react";
import Select from "react-select";
import axios from "axios";
import Header from "../components/header.js";
import "../style/JobTrend.css";

const customSelect ={
  control: (provided) =>({
    ...provided,
    width: "125px",
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
    backgroundColor: state.isSelected ? "#4285F4" : state.isFocused ? "#ACCBFF" : "#FFF",
    color: state.isSelected ? "#fff" : "#000",
    cursor: 'pointer'
  }),
  indicatorSeparator: (provided) => ({
    ...provided,
    display: "none"
  })
}

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

function JobTrend(){
  const [options, setOptions] = useState([]);
  const [joboptions, setJobOptions] = useState([]);
  const [yearoptions, setYearOptions] = useState([]);
  const [halfyearoptions, setHalfYearOptions] = useState([]);

  useEffect(()=>{
    const fetchJobData = async() =>{
      try{
        const response = await fetch('http://15.164.171.29:8080/job');
        const data = await response.json();

        //setOptions(data)

        const transformedOptions = data
        .filter((item, index, self) =>
          index === self.findIndex((t) => t.jobTitle === item.jobTitle))
        .map((item, index) => ({
          value: index,
          label: item.jobTitle
        }));
        setJobOptions(transformedOptions);

        const YeartransformedOptions = data
        .filter((item, index, self) => 
          index === self.findIndex((t) => t.year === item.year))
        .map((item, index) => ({
          value: index,
          label: item.year
        }));
        setYearOptions(YeartransformedOptions);

        const HalfYeartranformedOptions = data
        .filter((item, index, self) => 
          index === self.findIndex((t) => t.part === item.part))
        .map((item, index) => ({
          value: index,
          label: item.part
        }));
        setHalfYearOptions(HalfYeartranformedOptions);
      } 
      catch(error){
        console.error('Fetching data failed:', error);
      }
    };
    fetchJobData();
  }, []);

  const [JobselectedOption, setSelectedOption] = useState(null);
  const [YearselectedOption, setYearSelectedOption] = useState(null);
  const [HalfYearselectedOption, setHalfYearSelectedOption] = useState(null);
  
  const JobhandleChange = (JobselectedOption) => {
    setSelectedOption(JobselectedOption);
    console.log(JobselectedOption)
  };
  const YearhandleChange = (YearselectedOption) =>{
    setYearSelectedOption(YearselectedOption);
    console.log(YearselectedOption);
  };
  const HalfYearhandleChange = (HalfYearselectedOption) =>{
    setHalfYearSelectedOption(HalfYearselectedOption);
    console.log(HalfYearselectedOption)
  };
  
  const [statistics, setStatistics] = useState([]);
  const [totalCount, setTotalCount] = useState([]);
  const buttonHandler = async() => {
    if (!JobselectedOption){
      alert('옵션을 선택해주세요');
      return;
    }
    try{
      const response = await fetch(`http://15.164.171.29:8080/jobs/Trend/${YearselectedOption.label}/${HalfYearselectedOption.label}/${JobselectedOption.label}`);
      const data = await response.json();
      console.log(data)
      setStatistics(data.top5JobList);
      setTotalCount(data.totalCount);
      console.log("통계 : ",statistics)
    }
    catch(error){
      console.error('데이터 요청 실패', error);
    }
  };


  return(
      <div className="Trendbody">
        <Header/>
        <div className="MainBody">
          <div className="MenuSelect">
            <div className="SubTitleBox">
              <div className="SubTitletext">직무별 채용 트렌드</div>
            </div>  
            <article className="FilterList">
              <label for="Year" className="YearOption">
                <div className="LabelTypo">년도</div>
                <Select
                    className="Selection"
                    classNamePrefix="select"
                    name="Year"
                    options={yearoptions}
                    isSearchable={false}
                    styles={customSelect}
                    onChange={YearhandleChange}
                />
              </label>
              <label for="HalfYear" className="HalfYearOption">
                <div className="LabelTypo">분기</div>
                <Select
                    className="Selection"
                    classNamePrefix="select"
                    name="HalfYear"
                    options={halfyearoptions}
                    isSearchable={false}
                    styles={customSelect}
                    onChange={HalfYearhandleChange}
                />
              </label>
              <label for="Job" className="JobOption">
                <div className="LabelTypo">직무</div>
                <Select
                    className="Selection"
                    classNamePrefix="select"
                    name="Job"
                    options={joboptions}
                    isSearchable={true}
                    styles={JobcustomSelect}
                    onChange={JobhandleChange}
                />
              </label>
              <button className="ButtonStyle" onClick={buttonHandler}>
                <span className="ButtonTextWrapper">적용하기</span>
              </button>
            </article>
          </div>
          <div className="SkillTrendChart">
            <div className="ChartTitle">기술 스택 트렌드</div>
            {statistics && statistics.map((stat, index) => (
              <div className="BarItem" key={index}>
                <div className="BarTypo">{stat.skillName}</div>
                <div className="BarChart">
                  <div className="BarChartMax">
                    <div className={`Rectangle${index + 9}`}
                       style={{width: `${Math.round(stat.skillCount / totalCount * 100 * 10) / 10}%`, height: 12, background: '#4285F4'}} />
                  </div>
                  <div className="BarChartPercent">{Math.round(stat.skillCount / totalCount * 100 * 10) / 10}%</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
}

export default JobTrend;