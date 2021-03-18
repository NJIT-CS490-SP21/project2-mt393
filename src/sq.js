import "./board.css";
import React from "react";
import PropTypes from 'prop-types';
import { socket } from "./socket";

export function Square(props) {
  function clicked() {
    socket.emit("move", { square: props.num });
  }

  return (
    <td>
      {props.turn === true && props.team === "" ? (
        <button type="button" onClick={() => clicked()}>{props.team}</button>
      ) : (
        <div>{props.team}</div>
      )}
    </td>
  );
}
Square.propTypes = {
  turn: PropTypes.bool,
  num: PropTypes.number,
  team: PropTypes.string
};

export default Square;
