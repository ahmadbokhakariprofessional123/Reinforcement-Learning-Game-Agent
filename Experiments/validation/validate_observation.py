# observation_validation.py

from origins_env import OriginsEnv

class TestObservationValidation:
    """Class to validate the observation space of the game environment."""

    def setup_method(self):
        """Initialize a fresh environment before each test."""
        self.env = OriginsEnv()  # Create a new instance for each test

    def test_observation_shape(self):
        """Test that the observation space has the correct shape."""
        obs = self.env.get_observation()
        assert len(obs) == 100, "Observation space should be 100 elements"
        print("✓ Observation shape test passed")

    def test_piece_encoding(self):
        """Test that pieces are encoded correctly in the observation."""
        obs = self.env.get_observation()
        assert obs[0] == 1, "Creationist_Earth should encode as 1"
        assert obs[74] == -5, "Evolutionist_Woman should encode as -5"
        print("✓ Piece encoding test passed")

def run_observation_validation_tests():
    """Run the observation validation tests."""
    print("\n=== Running Observation Validation Tests ===")
    tester = TestObservationValidation()
    
    # Setup the environment
    tester.setup_method()
    
    # Run the tests
    try:
        tester.test_observation_shape()
        tester.test_piece_encoding()
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"💥 Test crashed: {e}")
    else:
        print("✅ All observation tests passed!")

if __name__ == "__main__":
    run_observation_validation_tests()