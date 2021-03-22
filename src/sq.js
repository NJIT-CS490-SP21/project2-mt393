import "./board.css";
import React from "react";
import PropTypes from 'prop-types';
import { socket } from "./socket";

export function Square({num, turn, team}) {
  function clicked() {
    socket.emit("move", { square: num });
  }

  return (
    <td>
      {turn === true && team === "" ? (
        <button type="button" onClick={() => clicked()}>{team}</button>
      ) : (
        <div>{team}</div>
      )}
    </td>
  );
}
Square.propTypes = {
  turn: PropTypes.bool,
  num: PropTypes.number,
  team: PropTypes.string
};
Square.defaultProps = {
  turn: true,
  num: 1,
  team: ""
};


export default Square;
