import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MatchingUniversities = () => {
  const [matchingUniversities, setMatchingUniversities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const userId = localStorage.getItem("userId");

  useEffect(() => {
    const fetchMatchingUniversities = async () => {
      try {
        const response = await axios.get(`http://localhost:5001/matching-universities/${userId}`);
        setMatchingUniversities(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching matching universities:", error);
        setError("Failed to fetch matching universities. Please try again later.");
        setLoading(false);
      }
    };

    fetchMatchingUniversities();
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="matching-universities">
      <h2>Matching Universities</h2>
      <table>
        <thead>
          <tr>
            <th>University Name</th>
            <th>In-State Tuition Fees</th>
            <th>Room and Board Cost</th>
          </tr>
        </thead>
        <tbody>
          {matchingUniversities.map((university, index) => (
            <tr key={index}>
              <td>{university.UniversityName}</td>
              <td>${university.InStateTuitionFees}</td>
              <td>${university.RoomAndBoardCost}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MatchingUniversities;