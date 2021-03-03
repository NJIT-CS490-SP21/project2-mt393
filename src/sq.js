import React from 'react';
import { useRef, useState, useEffect } from "react";
import './board.css';
import {socket} from './App.js';

export function Square(props) {
    function clicked() {
        socket.emit("move", {"square": props.num});
    }
    
    return (
        <td>
            { props.turn === true ? (
                <button onClick={() => clicked()}>
                    { props.team }
                </button>
            ) : (
                <div>
                    { props.team }
                </div>
            )}
        </td>
        );
}