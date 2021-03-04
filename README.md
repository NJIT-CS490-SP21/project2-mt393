# Tic-tac-toe app

Note: requirements, setup, and run are all the same as from the starter code here:https://github.com/NJIT-CS490-SP21/react-starter
## Requirements
1. `npm install`
2. `pip install -r requirements.txt`

## Setup
1. Run `echo "DANGEROUSLY_DISABLE_HOST_CHECK=true" > .env.development.local` in the project directory

## Run Application
1. Run command in terminal (in your project directory): `python app.py`
2. Run command in another terminal, `cd` into the project directory, and run `npm run start`
3. Preview web page in browser '/'


### Known problems
 - The app is super ugly
Possible solution: Im not great at css or html. i tried to simply present some concept of order with the html or creativity by having the flat table turn into a set of buttons on your turn the button. id like to center the board and have X's username on the left and O's on the right with a red and blue theme to each respectively
 - the turns dont work, and as a result, most of the app as well.
Possible solution: i spent quite a bit of time on this but havent figured out why they dont work. Maybe my prevTurn isnt working like i thought it would. Something isnt working like i think it is because the logic checks out.
 - the username list function isnt out yet. i know how to make a list and iterate through it, but the useState variable name that im using to hold and update the array says undefined when i try to put it in the html
Possible solution: maybe isolate it in its own file in case its interacting with something else oddly because as far as i can tell it should work. it probably deserves its own file anyway
 - heroku isnt rendering the restart button
Possible solution: i think im pushing wrong but idk what to do differently.

### Solved problems
 - the code emits the same event back to back to send it to different clients
Solution: You can create. channels of communication called "rooms." they were previously being used to emit events to individual clients, but they can be used to emit events to multiple specific clients if you initialize one to pass in to the parameters of the respective emit function. To add a session to a room you have to join it and joining the room takes a parameter that nobody tells you about, but it turns out its supposed to be a string to identify the room.

 - The onClick method for each square needs to tell every square that its not their turn and to not present the buttons
Solution: I wanted to handle this locally for speed while keeping the square function in its own file for readability and to maintain the status of whether or not the button was showing, but the button status had to be passed in as a prop to each button and i couldnt altar the useState from the board file that controlled the button status with the onclick of another js file without socket connecting to the server, at least as far as i could quickly find and learn. the default node event handler was a contender that i didnt have time to learn though.
