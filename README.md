# Snake AI NEAT Simulation

## Description
This project implements a Snake game AI using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve the snake's behavior over time. The simulation involves multiple generations of snake agents learning to navigate the game environment, avoid collisions, and eat apples to increase their scores.
To replicate the demo video, just follow the installation and run the code as it is, it will automatically load the latest best pickle file. 

## Features
- **Neural Network Decision Making**: Utilizes NEAT to dynamically evolve neural network architectures.
- **Gameplay**: Users can choose between classic manual play or watching the AI play the game.

## Gameplay Instructions
- **Starting the Game**: To play the game, select one of the two modes and press start.
- **Controls**: Control the snake using the classic WASD controls.
- **Performance**: Generally, the snake can reach around a score of 30-45 before it eventually gets stuck in a loop.

## Configuration
The configuration for the network is specified in the `config-feedforward.txt` file.

## Installation
To use the project:
1. Clone the repository.
2. Change directory to MAIN: `cd MAIN`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the game: `python Snake.py`

## Demo
[https://github.com/borna03/Snake_AI_NN/assets/155463174/5d7f0142-5281-4cac-b2ed-85dfea826b79](https://github.com/borna03/Snake_AI_NN/assets/155463174/9475d884-f8f2-456a-9658-7097f558db89)
