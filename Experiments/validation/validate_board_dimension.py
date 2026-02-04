# board_validation.py

from origins_env import OriginsEnv  # Assuming your env is in origins_env.py

class TestBoardValidation:
    """Class to validate the game board dimensions."""

    def setup_method(self):
        """Initialize a fresh environment before each test."""
        self.env = OriginsEnv()  # Create a new instance for each test

    def test_board_dimensions(self):
        """Test that the game board has correct dimensions."""
        # Test row count
        assert len(self.env.board) == 8, "Board should have 8 rows"
        
        # Test column count in each row
        for row in self.env.board:
            assert len(row) == 10, "Each row should have 10 columns"
        
        print("✓ Board dimension test passed successfully!")

def run_validation_tests():
    """Run the validation tests."""
    print("\n=== Running Board Validation Tests ===")
    tester = TestBoardValidation()
    
    # Setup the environment
    tester.setup_method()
    
    # Run the test
    try:
        tester.test_board_dimensions()
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"💥 Test crashed: {e}")
    else:
        print("✅ All validation tests passed!")

if __name__ == "__main__":
    run_validation_tests()