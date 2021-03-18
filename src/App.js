import "./App.css";
import React, { useState } from "react";
import { socket } from "./socket";
import { Board } from "./board";
import { LB } from "./LB";

function App() {
  const [showLogin, setShowLogin] = useState(true);

  function closeLogin() {
    const newName = document.getElementById("name_input");
    setShowLogin(false);
    socket.emit("nameSubmit", { name: newName.value });
  }

  return (
    <div>
      {showLogin === true ? (
        <form onSubmit={() => closeLogin()}>
          <input
            id="name_input"
            maxLength="20"
            placeholder="Make a name!"
           />
          <button type="submit">Submit</button>
        </form>
      ) : (
        <div>
          <Board />
          <LB />
        </div>
      )}
    </div>
  );
}

export default App;
