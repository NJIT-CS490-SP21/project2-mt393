import React, { useState, useEffect } from "react";
import { Square } from "./sq";
import "./board.css";
import { socket } from "./socket";

export function Board() {
  const [useTeam, setTeam] = useState(["", "", "", "", "", "", "", "", ""]);
  const [myTurn, setMyTurn] = useState(false);
  const [winner, setWinner] = useState("");

  function restart() {
    socket.emit("restart", {});
  }

  useEffect(() => {
    socket.on("newgame", () => {
      setWinner("");
    });
  });

  useEffect(() => {
    socket.on("boardUpdate", (data) => {
      setTeam(data.updatedBoard);
    });
  });

  useEffect(() => {
    socket.on("gameWon", (data) => {
      setWinner(data.winner);
    });
  });

  useEffect(() => {
    socket.on("whosTurn", (data) => {
      setMyTurn(data.turn);
    });
  });

  return (
    <div>
      <table>
        <tbody>
          <tr>
            <Square num={1} team={useTeam[0]} turn={myTurn} />
            <Square num={2} team={useTeam[1]} turn={myTurn} />
            <Square num={3} team={useTeam[2]} turn={myTurn} />
          </tr>
          <tr>
            <Square num={4} team={useTeam[3]} turn={myTurn} />
            <Square num={5} team={useTeam[4]} turn={myTurn} />
            <Square num={6} team={useTeam[5]} turn={myTurn} />
          </tr>
          <tr>
            <Square num={7} team={useTeam[6]} turn={myTurn} />
            <Square num={8} team={useTeam[7]} turn={myTurn} />
            <Square num={9} team={useTeam[8]} turn={myTurn} />
          </tr>
        </tbody>
      </table>
      {myTurn || winner ? (
        <button type="button" onClick={() => restart()}>Restart</button>
      ) : (
        <button type="button">Restart</button>
      )}
      {winner ? <h1>The winner is {winner}!</h1> : null}
    </div>
  );
}
export { Board as default };
