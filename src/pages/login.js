import React, {useEffect} from "react";
import "../style/login.css"
import imageLogo from "../image/chaezzic-logo 1.png"
import { useNavigate } from "react-router-dom";
import { Axios } from "axios";

const CLIENT_ID = "3f893a5c7be2f5a01b4b"
const redirectURL="http://15.164.171.29:8080/oauth"
const GITHUB_AUTH_SERVER = `https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${redirectURL}`;


function handleLoginClick(){
  window.location.href = GITHUB_AUTH_SERVER;
}

function Login(){
  const navigate = useNavigate();

  const navigatetoHome=()=>{
    navigate("/");
  };

    return(
        <div className="Loginbody">
            <div className="Logobody">
                <nav className="LoginLogoMenuNav">
                  <div className="LoginLogo" onClick={navigatetoHome}>
                    <img src={imageLogo} alt="logoImg" />
                    <div className="LogintitleWrapper">채찍</div>
                  </div>
                  <div className="loginWrapper">로그인</div>
                </nav>
            </div>
            <div className="LoginTypoFrame">
              <div className="LoginTypo">
                <div className="LoginMainTypo">간편하게 가입하고<br/>채찍의 서비스 이용하기</div>
                <div className="LoginSloganTypo">채용 트렌드를 찍어주다, 채찍</div>
              </div>
              <button className="NavLoginButton" onClick={handleLoginClick}>
                <div className="LoginButtonTypo">깃허브 계정으로 계속하기</div>
              </button>
            </div>
        </div>
    )
}

export default Login;