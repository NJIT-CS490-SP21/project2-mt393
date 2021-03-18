import React, { useState, useEffect } from "react";
import { socket } from "./socket";

export function LB() {
  const [leaders, setLeaders] = useState([]);
  const [scores, setScores] = useState([]);
  const [shown, setShown] = useState(false);

  function toggleLB() {
    setShown((prevShown) => !prevShown);
  }

  useEffect(() => {
    socket.on("updateLB", (data) => {
      setLeaders(data.leaders);
      setScores(data.scores);
    });
  });

  return (
    <div>
      <button type="button" onClick={() => toggleLB()}>Leaderboard</button>
      {shown ? (
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Username</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {leaders.map((leader, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{leader}</td>
                <td>{scores[index]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </div>
  );
}
export { LB as default };
