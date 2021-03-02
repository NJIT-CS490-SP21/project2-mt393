import React from 'react';
import { useRef, useState, useEffect } from "react";
import { Square } from './sq.js';
import './board.css';
import io from 'socket.io-client';

const socket = io()

export function Board() {
  const[useTeam, setTeam] = useState("X")
  
  useEffect(() => {
    socket.on('move', (data) => {
      
    })
  })
  
    return (
      <div>
        <table>
          <tbody>
            <tr>
              <Square num={1} team={useTeam}/>
              <Square num={2} team={useTeam}/>
              <Square num={3} team={useTeam}/>
            </tr>
            <tr>
              <Square num={4} team={useTeam}/>
              <Square num={5} team={useTeam}/>
              <Square num={6} team={useTeam}/>
            </tr>
            <tr>
              <Square num={7} team={useTeam}/>
              <Square num={8} team={useTeam}/>
              <Square num={9} team={useTeam}/>
            </tr>
          </tbody>
        </table>
      </div>
    )
}