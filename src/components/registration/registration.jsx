import React, { useState } from "react";
import Select from "react-select"; // Import React Select
import './registration.css';

const Register = () => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    reEnterPassword: "",
    tuitionFeeBudget: "",
    accommodationFeeBudget: "",
    selectedColleges: [], // Store selected college options
  });

  // Options for the college dropdown
  const collegeOptions = [
    { value: "harvard", label: "Harvard University" },
    { value: "stanford", label: "Stanford University" },
    { value: "mit", label: "MIT" },
    { value: "uiuc", label: "University of Illinois Urbana-Champaign" },
    { value: "berkeley", label: "UC Berkeley" },
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleDropdownChange = (selectedOptions) => {
    setFormData((prevState) => ({
      ...prevState,
      selectedColleges: selectedOptions,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.password !== formData.reEnterPassword) {
      alert("Passwords do not match!");
      return;
    }
    console.log("Form submitted:", formData);
  };

  return (
    <div className="register">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>First Name:</label>
          <input
            type="text"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Last Name:</label>
          <input
            type="text"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Re-enter Password:</label>
          <input
            type="password"
            name="reEnterPassword"
            value={formData.reEnterPassword}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>College Names:</label>
          <Select
            options={collegeOptions} 
            isMulti 
            isSearchable 
            value={formData.selectedColleges}
            onChange={handleDropdownChange} 
            placeholder="Select Colleges"
          />
        </div>
        <div>
          <label>Tuition Fee Budget:</label>
          <input
            type="number"
            name="tuitionFeeBudget"
            value={formData.tuitionFeeBudget}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Accommodation Fee Budget:</label>
          <input
            type="number"
            name="accommodationFeeBudget"
            value={formData.accommodationFeeBudget}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
