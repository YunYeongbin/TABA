import React from 'react';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";

import Home from "./pages/home.js"
import Trend from "./pages/JobTrend.js"
import Interview from "./pages/interview.js"
import InterviewOutput from "./pages/interview_output.js"
import Login from "./pages/login.js"

export default() => {
    return(
        <Router>
            <Routes>
                <Route exact path="/" element={<Home/>} />
                <Route exact path="/login" element={<Login/>} />
                <Route exact path="/jobtrend" element={<Trend/>} />
                <Route exact path="/interviewai" element={<Interview/>} />
                <Route exact path="/interviewai/output" element={<InterviewOutput/>} />
            </Routes>
        </Router>
    )
}