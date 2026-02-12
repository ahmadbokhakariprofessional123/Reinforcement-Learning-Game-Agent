# Reinforcement Learning Agent for a Custom Turn-Based Board Game

## Project Overview

This project presents the design, implementation, and evaluation of a Reinforcement Learning agent trained to play a custom turn-based board game.

A custom OpenAI Gym environment was developed to simulate the game logic, and a Proximal Policy Optimization (PPO) agent was trained using Stable Baselines3.

The main objectives of this project were to design a fully functional custom environment, define appropriate state and action spaces, implement reward shaping strategies, train a stable PPO agent, and validate complex game logic through systematic testing.


## System Architecture

The project consists of three core components.

### Custom Gym Environment

A custom Gym environment called OriginsEnv was implemented. This environment defines the action space, observation space, reward logic, and termination conditions for the board game.

### Environment Registration

The environment is registered under the name Origins-v0 so that it can be instantiated using gym.make.

### PPO Training Pipeline

A PPO training pipeline was implemented using Stable Baselines3. The environment is wrapped using DummyVecEnv for compatibility with PPO, and training logs are recorded for analysis.


## Training Configuration

The PPO agent was trained with the following configuration:

- Policy: MlpPolicy  
- Learning rate: 0.0003  
- Total timesteps: 100000  
- n_steps: 2048  
- Batch size: 64  
- n_epochs: 10  
- Gamma: 0.99  
- GAE lambda: 0.95  
- Clip range: 0.2  

TensorBoard logging was enabled to monitor training performance.


## Training Performance

The agent successfully learned to generate valid actions and reduce penalties for invalid moves. Over time, accumulated reward improved as the agent adapted to the game environment.

However, the agent did not consistently achieve winning conditions, highlighting challenges such as reward sparsity, exploration versus exploitation trade-offs, and environment complexity.


## Environment Design

The custom environment subclasses gym.Env and defines:

- A discrete action space representing possible moves  
- An observation space encoding the board state  
- A reward function assigning positive rewards for valid actions and penalties for invalid moves  
- Terminal conditions for episode completion  

Special care was taken to handle edge cases and ensure rule-compliant gameplay.


## Validation and Testing

Custom validation scripts were written to verify:

- Correct state transitions  
- Proper handling of invalid actions  
- Accurate reward assignment  
- Valid terminal conditions  

Most tests passed successfully, though some edge cases revealed the complexity of implementing board game logic.


## Project Structure

- main.py – PPO training script  
- register_env.py – Environment registration  
- origins_env.py – Custom Gym environment  
- requirements.txt – Project dependencies  
- experiments – Experimental logs and files  
- README.md – Project documentation  


## How to Run the Project

1. Install dependencies  
   pip install -r requirements.txt  

2. Register the environment  
   python register_env.py  

3. Train the PPO agent  
   python main.py  

4. View training logs  
   tensorboard --logdir=ppo_origins_tensorboard  


## Key Challenges and Lessons Learned

- Reward sparsity slowed convergence  
- Invalid action penalties influenced exploration behaviour  
- Environment complexity required iterative refinement  
- Hyperparameter tuning affected stability  


## Future Improvements

- Introduce self-play training  
- Implement baseline comparison such as a random agent  
- Improve reward shaping  
- Track win-rate statistics  
- Extend to multi-agent training  


## Technologies Used

Python  
OpenAI Gym  
Stable Baselines3  
NumPy  
TensorBoard  
Git and GitHub  


## Summary

This project demonstrates the complete development cycle of a reinforcement learning system, from custom environment design and reward engineering to PPO training and validation. It highlights both the technical and experimental challenges of applying reinforcement learning to a complex custom game environment.
