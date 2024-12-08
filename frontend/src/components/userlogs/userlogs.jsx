import React, { useState, useEffect } from "react";
import axios from "axios";

const UserLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const userId = localStorage.getItem("userId");

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await axios.get(`http://localhost:5001/user-logs/${userId}`);
        setLogs(response.data);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching user logs:", err);
        setError("Failed to fetch user logs. Please try again later.");
        setLoading(false);
      }
    };

    fetchLogs();
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="user-logs">
      <h2>User Logs</h2>
      {logs.length > 0 ? (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ border: "1px solid #ddd", padding: "8px" }}>Audit ID</th>
              <th style={{ border: "1px solid #ddd", padding: "8px" }}>User ID</th>
              <th style={{ border: "1px solid #ddd", padding: "8px" }}>Action</th>
              <th style={{ border: "1px solid #ddd", padding: "8px" }}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.AuditId}>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{log.AuditId}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{log.UserId}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{log.Action}</td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>{log.Timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No logs found for this user.</p>
      )}
    </div>
  );
};

export default UserLogs;