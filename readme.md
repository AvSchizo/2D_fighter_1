### to set up:
After downloading the source code, you will need to create a python virtual environment.
You do this by entering the below line into a Comand-Line Interface like the Linux terminal, or Window's powershell.

> python3 -m venv .venv

<em>You can actually use any name instead of </em>.venv<em> but to avoid confusion, I recommend using </em>.venv<em></em>

Whenever you want to start the game or continue the setup, you need to activate the virtual environment.

##### on Linux or Apple:

> source .venv/bin/activate

##### on Windows:

> ###### with Command Prompt:
> .\\.venv\Scripts\activate.bat

> ###### with Powershell:
> .\\.venv\Scripts\Activate.ps1

> ###### with Git Bash / WSL:
> source .venv/Scripts/activate

To continue the setup, you will need to type the line below to install pygame.

##### on Windows with Python version 3.12- (most likely):

> pip install pygame-ce

##### otherwise:

> pip install pygame

The game is now completely set up, to play the game, have the virtual environment be active, and enter the line below.

> python3 main-window.py

Once you're done playing, type the line below and you're done.

> deactivate

## Preferences

You may notice there is no preferences.json to start.
Fear not, this is intentional and it will appear with the default preferences upon first starting up the game.