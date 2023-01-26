# snake_Pygame
Based on the classic game Snake, mimicking an 8-bit era graphical style.

Created with python 3.10 and pygame v2.1.4.

For the game sprites I chose to convert the .pngs into a base64 format and embed the images directly into the source code in order to reduce the number of dependencies required to run the game. After each round, the score is saved to a separate file called "highscores.txt". After the Game Over screen, the game will parse the 10 highest numbers from the file and display them as Top Scores in descending order like a classic arcade game.

--> https://docs.python.org/3.10/library/base64.html


### Instructions on how to play the game
1. First make sure you have Python 3 installed
2. Install the latest version of Pygame
--- on Windows: pip install pygame
--- on Linux: sudo apt-get install python-pygame
3. Make sure main.py and 8bit.ttf are in the same folder
4. Run main.py

### Move snake with arrow keys
## ↑ ↓ ← →
