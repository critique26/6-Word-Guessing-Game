Python Quest: Word Guessing Game
Python Quest is an interactive, pastel galaxy-themed arcade word puzzle built entirely with Pygame. Test and sharpen your Python programming and Computer Science knowledge by solving technical clues across various CS domains before running out of lives!

Features
Custom Player Profiling: Input your handle at launch to track performance across sessions.

Dynamic Question Deck: Randomly shuffles a master question bank into an active pool for unique playthroughs.

Real-Time Character History: Live on-screen tracking of used keystrokes to prevent repeated mistakes.

Life & Scoring System:

Gain +10 Points for every correct word guessed.

Lose 1 Life (out of 5) for incorrect word submissions.

Persistent Leaderboard: Ranks player scores in descending order.

Match History Log: Displays past word outcomes, attempt counts, and round statuses.

Pastel Galaxy Aesthetic: Custom UI panels, high-contrast text, and a dynamic starfield background.

Tech Stack & Data Structures
Language: Python 3

Graphics & Loop Engine: Pygame

Core Data Structures: Heavy reliance on Python lists, including:

Nested Lists: Storing [Hint, Answer, Category] records and [Player, Score] high scores.

List Operations: Deck management via pop(), append(), list slicing, and lambda key sorting.

Installation & Setup
1. Clone the Repository

Bash
git clone https://github.com/your-username/python-quest-word-guessing-game.git
cd python-quest-word-guessing-game

2. Install Dependencies
Make sure you have pygame installed:

Bash
pip install pygame

3. Run the Game

Bash
python main.py


How to Play & Controls

Game State	Controls

Name Input	Type player name + ENTER

Instructions	Press ENTER to begin

Gameplay	Type word guess + ENTER to submit

Feedback Screens	Press ENTER to continue

End Game / Victory	R (Replay), L (Leaderboard), H (History)

Leaderboard / History	R (Replay), L (Leaderboard), H (History)

Global Controls	ESC (Quit Game)


This project is open-source and available under the MIT License.
