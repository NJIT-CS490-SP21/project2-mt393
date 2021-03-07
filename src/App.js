import logo from './logo.svg';
import './App.css';
import { Board } from './board.js';
import React from "react";
import { useRef, useState, useEffect } from "react";
import io from 'socket.io-client';

export const socket = io();

function App() {
  const [showLogin, setShowLogin] = useState(true);
  
  function closeLogin() {
    let newName = document.getElementById("name_input");
    setShowLogin(false);
    socket.emit("nameSubmit", {name: newName.value});
  }
  
  return (
    <div>
      {showLogin === true ? (
        <form onSubmit={() => closeLogin()}>
          <input id="name_input" maxLength="20" placeholder="Make a name!"></input>
          <button>Submit</button>
        </form>
      ) : (
        <div>
          <Board />
        </div>
      )}
    </div>
  );
}

export default App;
