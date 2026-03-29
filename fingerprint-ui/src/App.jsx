import { useState } from "react";
import axios from "axios";
import "./App.css";

import { useEffect } from "react";



function App() {

  const [targets, setTargets] = useState([""]);
  const [results, setResults] = useState([]);

  useEffect(() => {
  const interval = setInterval(async () => {
    try {
      const res = await axios.get("http://10.1.0.30:5000/results");
      setResults(res.data);
    } catch (err) {
      console.log("Polling error:", err);
    }
  }, 2000);

  return () => clearInterval(interval);
}, []);
  const handleChange = (index, value) => {
    const updated = [...targets];
    updated[index] = value;
    setTargets(updated);
  };

  const addInput = () => {
    setTargets([...targets, ""]);
  };

  const scan = async () => {
    const filtered = targets.filter(t => t.trim() !== "");
    //
   try {
    const res = await axios.post("http://10.1.0.30:5000/scan", {
      targets: filtered
    });

    setResults(res.data);
  } catch (err) {
    console.log("Scan error:", err);
  }
};

  return (
    <div className="page">

      <div className="dashboard">

        {/* LEFT PANEL */}
        <div className="panel inputPanel">

          <h2>Web Server Fingerprinting Tool</h2>

          <div className="inputs">

            {targets.map((target, index) => (
              <input
                key={index}
                type="text"
                placeholder="Enter domain or IP"
                value={target}
                onChange={(e) => handleChange(index, e.target.value)}
              />
            ))}

          </div>

          <div className="buttons">

            <button className="addBtn" onClick={addInput}>
              + Add Website
            </button>

            <button className="scanBtn" onClick={scan}>
              Scan Targets
            </button>

          </div>

        </div>

        {/* RIGHT PANEL */}
        <div className="panel resultsPanel">

          <h2>Scan Results History</h2>

          <table>

            <thead>
              <tr>
                <th>Target</th>
                <th>Protocol</th>
                <th>Server</th>
                <th>Version</th>
              </tr>
            </thead>

            <tbody>

              {results.map((r,i)=>(
                <tr key={i}>
                  <td>{r.target}</td>
                  <td>{r.protocol}</td>
                  <td>{r.server}</td>
                  <td>{r.version}</td>
                </tr>
              ))}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default App;