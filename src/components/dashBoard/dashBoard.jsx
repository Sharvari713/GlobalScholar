import React from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  // Get username from localStorage (this simulates a logged-in user)
  const username = localStorage.getItem("username");

  const handleLogout = () => {
    // Remove username from localStorage and redirect to login page
    localStorage.removeItem("username");
    navigate("/login");
  };

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <p>Welcome, {username ? username : "Guest"}!</p>

    </div>
  );
};

export default Dashboard;
