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

## Databases setup

Note: this is the same as and was taken from this hw10 readme: https://gist.github.com/naman-njit/c6e30e65c03cd4fd564d5339bd46eced
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs` Enter yes to all prompts.
2. Initialize PSQL database: `sudo service postgresql initdb`
3. Start PSQL: `sudo service postgresql start`
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER` **If you get an error saying "could not change directory", that's okay! It worked!**
5. Make a new database: `sudo -u postgres createdb $USER` **If you get an error saying "could not change directory", that's okay! It worked!**
6. Make sure your user shows up:
- a) `psql`
- b) `\du` look for ec2-user as a user (**take a screenshot**)
- c) `\l` look for ec2-user as a database (**take a screenshot**)
7. Make a new user:
- a) `psql` (if you already quit out of psql)
- b) Type this with your username and password (DONT JUST COPY PASTE): `create user some_username_here superuser password 'some_unique_new_password_here';` e.g. `create user namanaman superuser password 'mysecretpassword123';`
- c) \q to quit out of sql
8. Save your username and password in a `sql.env` file with the format `SQL_USER=` and `SQL_PASSWORD=`.

### Known problems
 - The client doesnt emit a socket event when the game ends as the specs instruct. Personally, for apps that require coordination between multiple clients, i rather do a lot of the computation and keep a lot of information on the server
Possible solution: Only use the server to connect the clients to other clients and the database. Keep most of the information in a bunch of simple usestates and then extrapolate the data, use javascript to do most computations, and any time that you update something, just give it to the server to give to all of the other clients.

 - The app does not look aesthetically presentable
 -Possible solution: have the tic tac toe game running vertically, with x's username on top, o's on the bottom. that gives me enough room to shift it to the left half of the screen only and keep the right half with a button at the top to switch between a list of usernames and the leaderboard, both would use overflow-y in css to give them their own personal scroll bars so you dont have to scroll away from the game

### Solved problems
 - the app isnt getting the allusers table from models
Solution: The app had to be specified to only run when its the main function. By default, python files will run simply by importing them. this was done by putting locking the flask run function behind an if statement that checked if it was the main process first. I think there also mightve been a way to do this by putting the entire file in a main() function, but that wasnt the solution i used so i dont know as much about it.

