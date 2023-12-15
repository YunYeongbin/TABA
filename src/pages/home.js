import React, { useEffect, useState } from "react";
import axios from "axios";
import Header from "../components/header.js";
import "../style/home.css";

function Home() {
  const [repositories, setRepositories] = useState([]);

  useEffect(() => {
    const queryParams = new URLSearchParams(window.location.search);
    const accessToken = queryParams.get('accessToken');

    if (accessToken) {
      console.log('Access Token:', accessToken);
      fetchRepositories(accessToken);
    } else {
      const code = queryParams.get('code');
      if (code) {
        fetchAccessToken(code);
      }
    }
  }, []);

  const fetchAccessToken = async (code) => {
    try {
      const response = await axios.get(`http://15.164.171.29:8080/oauth?code=${code}`);
      const accessToken = response.data.access_token;
      console.log('Fetched Access Token:', accessToken);
      fetchRepositories(accessToken);
    } catch (error) {
      console.error('Access token error', error);
    }
  };

  const fetchRepositories = async (accessToken) => {
    try {
      // 백엔드 서버에 액세스 토큰을 사용하여 리포지토리 정보를 요청합니다.
      const response = await axios.get('http://15.164.171.29:8080/api/repositories', {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });
      setRepositories(response.data);
      console.log('Repositories:', response.data);
    } catch (error) {
      console.error('Error fetching repositories', error);
    }
  };

    return(
      <div className="Main">
          <Header />
          <div className="MainIntro1">
            <div className="TrendIntro1">
              <p className="TrendtextWrapper1">“개발자인 당신에게<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;채용 트렌드를 찍어주다”</p>
            </div>
            <div className="TrendIntro2">
              <p className="TrendtextWrapper2">반기 마다 직무별 기술 스택 트렌드 및<br/>직무별 자격증 트렌드 제공</p>
            </div>
          </div>
          <div className="MainIntro2">
            <div className="AiIntro1">
              <img className="IconBrain"/>
              <div className="AitextWrapper1" >AI 모델 학습을 기반으로<br/>포트폴리오에서 면접 예상 질문 추출</div>
            </div>
            <div className="AiIntro2">
              <div className="AitextWrapper2">“채찍만의 독보적인 서비스,<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;포트폴리오로 면접 질문 예측하기”</div>
            </div>
          </div>
      </div>
    )
}

export default Home;