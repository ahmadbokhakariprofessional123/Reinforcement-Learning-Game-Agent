Reinforcement Learning Agent for Strategy Game

This project implements a reinforcement learning agent trained to make strategic decisions in a turn-based game environment. The objective is to evaluate how effectively a policy-based reinforcement learning algorithm can learn optimal behaviour through interaction with the environment.

Problem Statement
Designing intelligent agents for strategy-based games is challenging due to delayed rewards, large state spaces, and the need for long-term planning. Traditional rule-based systems lack adaptability, whereas reinforcement learning enables agents to learn strategies through trial and error.

This project investigates whether a reinforcement learning agent can learn effective decision-making strategies in a custom-designed game environment.

Objective

Design a custom environment suitable for reinforcement learning

Train an agent to maximise long-term reward

Evaluate training stability and learning behaviour

Analyse challenges such as reward shaping and convergence

Approach
A custom game environment was designed with defined states, actions, and rewards. A policy-based reinforcement learning algorithm was used to train the agent through repeated interactions with the environment. Learning progress was monitored using reward trends and behavioural evaluation.

Key design considerations included state representation, action space definition, reward shaping, and training stability.

Reinforcement Learning Method
Algorithm: Proximal Policy Optimisation (PPO)
Learning type: Model-free, on-policy reinforcement learning
Training strategy: Episodic training with reward feedback
Evaluation: Average reward per episode and behavioural consistency

PPO was selected due to its training stability and effectiveness in complex environments.

Results
The agent demonstrated improved performance over training episodes. Reward trends showed gradual convergence, and strategic behaviour emerged through repeated training. Early training instability highlighted the importance of reward design and hyperparameter tuning.

Key Insights
Reward shaping had a significant impact on learning speed and agent behaviour. Reinforcement learning requires extensive experimentation and tuning. PPO provided more stable learning compared to simpler reinforcement learning approaches. Environment design proved to be as important as algorithm selection.

Tech Stack
Python
PyTorch
NumPy
Reinforcement Learning (PPO)
Custom environment logic

How to Run
Install dependencies using the requirements file and run the training script.

Future Improvements
Improve reward shaping for more advanced strategic behaviour
Introduce curriculum learning
Benchmark performance against heuristic agents
Add clearer visualisation of agent behaviour
Deploy the agent in an interactive interface
