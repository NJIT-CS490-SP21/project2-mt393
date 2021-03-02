import React from 'react';
import { useRef, useState } from "react";
import './board.css';

export function Square(props) {
    const [occupiedBy, setBy] = useState("")
    
    
    
    return (
        <td>
            { props.team }
        </td>
        );
}