import React, { useState } from "react";
import './login.css';
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    // Simulate authentication (you can replace this with actual logic)
    if (email && password) {
      localStorage.setItem("username", email); // Save the email as the username (or use a real username)
      navigate("/dashboard"); // Redirect to the dashboard
    } else {
      alert("Please enter valid credentials");
    }
  };

  return (
    <div className="login">
      <h2>Login Page</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input 
            type="email" 
            placeholder="Enter your email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Password:</label>
          <input 
            type="password" 
            placeholder="Enter your password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
