import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();
  const username = localStorage.getItem("user");

  const handleLogout = () => {
    localStorage.removeItem("user"); 
    navigate("/login"); 
  };

  const handleAnalysis = () =>{
    navigate("/analysis");
  }

  return (
    <header className="bg-light py-3 px-4">
      <div className="container d-flex justify-content-between align-items-center">
        {/* Site Name */}
        <div className="fs-3 fw-bold text-primary">Global Scholar</div>
        {/* Conditionally render buttons or user's name */}
        <div>
          {!username ? (
            <>
              <button
                className="btn btn-outline-primary me-2"
                onClick={() => navigate("/login")}
              >
                Login
              </button>
              <button
                className="btn btn-primary"
                onClick={() => navigate("/register")}
              >
                Register
              </button>
            </>
          ) : (
            <>
              <button 
                className="btn btn-outline ms-3"
                onClick={handleAnalysis}
              >
                Analysis
              </button>
              {/* <span className="fs-5">Hi, {username}!</span> */}
              <button
                className="btn btn-danger ms-3"
                onClick={handleLogout}
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
