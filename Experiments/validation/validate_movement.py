from origins_env import OriginsEnv
import numpy as np

def print_test_header(name):
    print(f"\n{'='*50}")
    print(f"Running {name} Tests")
    print(f"{'='*50}")

def test_initial_state():
    """Test the environment initializes correctly"""
    print_test_header("Initial State")
    env = OriginsEnv()
    env.reset()
    
    # Test initial positions
    assert env.board[0][0] == "Creationist_Earth", "Top-left should be Creationist Earth"
    assert env.board[7][9] == "Evolutionist_Earth", "Bottom-right should be Evolutionist Earth"
    assert env.turn == "Creationist", "First turn should be Creationist"
    
    # Test destination rows
    assert env.creationist_male_dest == 6, "Creationist male destination row should be 6"
    assert env.evolutionist_female_dest == 1, "Evolutionist female destination row should be 1"
    
    print("✓ All initial state tests passed")

def test_movement_rules():
    """Test movement rules for different pieces"""
    print_test_header("Movement Rules")
    env = OriginsEnv()
    env.reset()
    
    # Test Creationist Earth movement
    moves = env.get_valid_moves(0, 0)
    assert (1, 0) in moves, "Earth should move downward"
    assert (0, 1) in moves, "Earth should move right"
    
    # Test Evolutionist Man movement
    env.turn = "Evolutionist"
    moves = env.get_valid_moves(7, 5)
    assert (6, 5) in moves, "Evolutionist man should move up"
    assert (7, 6) in moves, "Evolutionist man should move right"
    
    # Test blocked movement
    env.board[1][0] = "Creationist_Water"
    assert (1, 0) not in env.get_valid_moves(0, 0), "Earth shouldn't move through same-team Water"
    
    print("✓ All movement rule tests passed")

def test_element_interactions():
    """Test element capture and conversion rules"""
    print_test_header("Element Interactions")
    env = OriginsEnv()
    env.reset()
    
    # Test Earth capturing Water
    env.board[1][0] = "Evolutionist_Water"
    env.move_piece((0, 0), (1, 0))
    assert env.board[1][0] == "Creationist_Earth", "Earth should capture Water"
    
    # Test neutral conversion
    env.reset()
    env.board[1][0] = "Neutral"
    env.move_piece((0, 0), (1, 0))
    assert env.board[1][0].startswith("Creationist_Earth"), "Should convert neutral to Earth"
    
    print("✓ All element interaction tests passed")

def test_win_conditions():
    """Test win condition detection"""
    print_test_header("Win Conditions")
    env = OriginsEnv()
    env.reset()
    
    # Test Creationist win
    env.creationist_male_arrived = True
    env.creationist_female_arrived = True
    assert env.check_game_over(), "Should detect Creationist win"
    
    # Test Evolutionist win
    env.reset()
    env.evolutionist_male_arrived = True
    env.evolutionist_female_arrived = True
    assert env.check_game_over(), "Should detect Evolutionist win"
    
    # Test draw condition
    env.reset()
    env.creationist_male_pos = None
    env.evolutionist_female_pos = None
    assert env.check_game_over(), "Should detect draw when both lose key pieces"
    
    print("✓ All win condition tests passed")

def test_observation_space():
    """Test the observation space structure"""
    print_test_header("Observation Space")
    env = OriginsEnv()
    obs = env.reset()
    
    # Test observation shape and values
    assert isinstance(obs, np.ndarray), "Observation should be numpy array"
    assert obs.shape == env.observation_space.shape, "Observation shape mismatch"
    assert obs.min() >= -1 and obs.max() <= 1, "Observation values out of bounds"
    
    print("✓ All observation space tests passed")

def test_reward_system():
    """Test basic reward functionality"""
    print_test_header("Reward System")
    env = OriginsEnv()
    env.reset()
    
    # Test reward for moving forward
    _, reward, _, _ = env.step(0)  # Try moving Creationist_Earth
    assert isinstance(reward, float), "Reward should be a float"
    
    # Test reward for reaching destination
    env.creationist_male_pos = (env.creationist_male_dest, 0)
    env.creationist_female_pos = (env.creationist_female_dest, 0)
    assert env.check_game_over()
    assert reward > 0, "Should get positive reward for winning"
    
    print("✓ All reward system tests passed")

def run_full_validation():
    """Run all validation tests"""
    try:
        test_initial_state()
        test_movement_rules()
        test_element_interactions()
        test_win_conditions()
        test_observation_space()
        test_reward_system()
        
        print("\n" + "="*50)
        print("✅ ALL VALIDATION TESTS PASSED SUCCESSFULLY!")
        print("="*50)
        return True
    except AssertionError as e:
        print("\n" + "="*50)
        print(f"❌ VALIDATION FAILED: {str(e)}")
        print("="*50)
        return False

if __name__ == "__main__":
    run_full_validation()