# Reinforcement Learning Agent for a Custom Turn-Based Board Game

## Project Overview
This project focuses on the design and implementation of a Reinforcement Learning (RL) agent capable of playing a custom turn-based board game. A custom game environment was built using OpenAI Gym, and a Proximal Policy Optimization (PPO) agent was trained using Stable-Baselines3.

The primary objective was to explore how reinforcement learning agents interact with complex game environments, including environment design, state representation, reward shaping, and validation of game logic.

---

## My Role
I was responsible for the **design and development of the Reinforcement Learning system**, including:

- Designing the custom OpenAI Gym environment
- Defining state, action, and observation spaces
- Implementing reward functions aligned with game rules
- Training a PPO-based RL agent using Stable-Baselines3
- Writing validation scripts to test environment logic and agent behaviour
- Managing RL-related code and experiments in GitHub

---

## Technologies Used
- **Python**
- **OpenAI Gym**
- **Stable-Baselines3 (PPO)**
- **NumPy**
- **Git / GitHub**

---

## Environment Design
A custom Gym environment was implemented by subclassing `gym.Env`. The environment defines:

- A discrete **action space** representing valid moves in the game
- A structured **observation space** encoding the board state
- Clear **terminal conditions** for episode completion
- Penalties for invalid actions to ensure rule-compliant gameplay

Special attention was given to handling edge cases and invalid moves, which are common challenges in turn-based game environments.

---

## Reinforcement Learning Agent
The RL agent was trained using **Proximal Policy Optimization (PPO)** due to its stability and suitability for discrete action spaces.

Key aspects include:
- Custom reward shaping to encourage valid gameplay
- Incremental rewards and penalties based on agent actions
- Iterative experimentation with reward structure and environment parameters

While the agent successfully learned to generate valid moves, it did not consistently achieve winning conditions, highlighting the challenges of reward sparsity and environment complexity.

---

## Validation and Testing
Validation scripts were written to ensure:
- Environment logic behaves as expected
- State transitions are valid
- Invalid actions are handled correctly

Some edge-case tests revealed unresolved issues, providing valuable insight into the difficulty of implementing and validating complex game rules.

---

## Project Structure
