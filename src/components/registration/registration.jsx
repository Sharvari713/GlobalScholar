import React, { useState, useEffect } from "react";
import Select from "react-select";
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import './registration.css';

const Register = () => {
  const navigate = useNavigate();
  const [universityOptions, setUniversityOptions] = useState([]);
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    reEnterPassword: "",
    tuitionFeeBudget: "",
    accommodationFeeBudget: "",
    selectedColleges: [],
  });

  // Fetch university names from backend
  useEffect(() => {
    const fetchUniversities = async () => {
      try {
        const response = await axios.get("http://localhost:5001/universities");
        setUniversityOptions(
          response.data.map((univ) => ({
            value: univ,
            label: univ,
          }))
        );
      } catch (error) {
        console.error("Error fetching university names:", error);
      }
    };
    fetchUniversities();
  }, []);

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

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.reEnterPassword) {
      alert("Passwords do not match!");
      return;
    }

    const selectedColleges = formData.selectedColleges.map((college) => college.value);

    const payload = {
      FirstName: formData.firstName,
      LastName: formData.lastName,
      EmailId: formData.email,
      Password: formData.password,
      TuitionFeeBudget: parseInt(formData.tuitionFeeBudget, 10),
      AccommodationBudget: parseInt(formData.accommodationFeeBudget, 10),
      SelectedColleges: selectedColleges,
    };

    try {
      const response = await axios.post("http://localhost:5001/register", payload);
      if (response.status === 201) {
        alert("Registration successful!");
        navigate("/dashboard");
      } else {
        alert(response.data.error || "Registration failed!");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred during registration.");
    }
  };

  return (
    <div className="register">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>First Name:</label>
          <input type="text" name="firstName" value={formData.firstName} onChange={handleChange} required />
        </div>
        <div>
          <label>Last Name:</label>
          <input type="text" name="lastName" value={formData.lastName} onChange={handleChange} required />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </div>
        <div>
          <label>Re-enter Password:</label>
          <input type="password" name="reEnterPassword" value={formData.reEnterPassword} onChange={handleChange} required />
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
        <div>
          <label>University Names:</label>
          <Select
            options={universityOptions}
            isMulti
            value={formData.selectedColleges}
            onChange={handleDropdownChange}
            placeholder="Select Universities"
          />
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
