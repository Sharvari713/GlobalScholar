import './App.css'
import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/login/login';
import Register from './components/registration/registration';
import Header from './components/header/header';
import Dashboard from './components/dashBoard/dashBoard';
import Analysis from './components/analysis/analysis';
import MatchingUniversities from './components/matchingUnis/MatchingUniversities';
import LivingCosts from './components/livingcosts/LivingCosts';

const App = () => {
  return (
    <Router>
      <Header/>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashBoard" element={<Dashboard/>}/>
        <Route path="/matching-universities" element={<MatchingUniversities />} />
        <Route path="/analysis" element={<Analysis/>}/>
        <Route path="/living-costs/:userId" element={<LivingCosts />} />
        <Route path="/" element={<h1>Welcome to Global Scholar!</h1>} />
        
      </Routes>
    </Router>
  );
};

export default App;
