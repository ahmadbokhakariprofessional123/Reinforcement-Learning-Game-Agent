# Validation

## Overview
This folder contains validation scripts used to verify the correctness and reliability of the custom game environment and its core mechanics.

Validation ensures that the environment behaves exactly as intended before and during Reinforcement Learning training and evaluation.

Unlike evaluation, which measures performance, **validation focuses on correctness**.

---

## Purpose of Validation
The validation process aims to:
- Verify game rules and logic implementation
- Ensure state, action, and observation spaces are correct
- Detect logical errors and edge cases
- Confirm environment stability before training the RL agent

---

## Files in This Folder

### `validate_board_innit.py`
Validates correct initialisation of the game board, including dimensions, starting positions, and default states.

### `validate_board_dimension.py`
Checks that the board dimensions conform to the expected configuration and constraints.

### `validate_movement.py`
Validates movement rules to ensure pieces move legally and invalid moves are correctly rejected.

### `validate_special_moves.py`
Tests special movement rules and edge-case actions defined by the game logic.

### `validate_observation.py`
Ensures that observations returned to the agent correctly represent the current game state.

### `validate_ai_decision.py`
Validates that AI decisions follow allowed action constraints and do not violate game rules.

### `validate_element.py`
Tests the interaction of individual game elements to ensure consistency and correctness.

### `validate_rendering.py`
Validates rendering logic to ensure the board and elements are displayed correctly during debugging and testing.

### `validate_time_mechanics.py`
Checks timing-related rules and mechanics to ensure consistency across turns and actions.

### `origins_env.py`
The validated custom Gym environment containing the complete game logic used during training and evaluation.

---

## Validation Methodology
1. Initialise the environment
2. Run validation scripts independently
3. Test individual components in isolation
4. Check expected vs actual outcomes
5. Identify and document failed test cases

Validation scripts are designed to be modular so that failures can be traced to specific components.

---

## Validation Results
- Most validation tests passed successfully
- Core game logic functions as intended
- Some edge cases revealed logical inconsistencies that require further refinement

These findings helped stabilise the environment before agent training and evaluation.

---

## Importance of Validation in RL
In Reinforcement Learning, incorrect environment logic can:
- Mislead the agent
- Corrupt reward signals
- Produce misleading evaluation results

Thorough validation ensures the agent learns from a **reliable and consistent environment**.

---

## Limitations
- Validation scripts do not cover every possible game scenario
- Some complex edge cases require manual inspection
- Further automated testing could improve robustness

---

## Conclusion
The validation process confirms that the custom environment is logically sound and suitable for Reinforcement Learning experiments.

This step is essential for ensuring trustworthy evaluation results and reliable agent behaviour.
