"""
board_validation.py - Fixed version with proper test class structure
"""

from origins_env import OriginsEnv

class TestBoardInitialization:
    """Test suite for board initialization validation"""
    
    def setup_method(self):
        """Initialize fresh environment before each test"""
        self.env = OriginsEnv()  # Create new instance for each test
    
    def test_board_dimensions(self):
        """Validate board has correct 8x10 dimensions"""
        assert len(self.env.board) == 8, "Board must have exactly 8 rows"
        assert all(len(row) == 10 for row in self.env.board), "All rows must have 10 columns"
        print("✓ Board dimensions validated")

    def test_initial_piece_placement(self):
        """Validate correct placement of key pieces"""
        assert self.env.board[0][0] == "Creationist_Earth", "Top-left should be Creationist Earth"
        assert self.env.board[7][9] == "Evolutionist_Earth", "Bottom-right should be Evolutionist Earth"
        print("✓ Initial pieces validated")

    def test_starting_positions(self):
        """Validate human character positions"""
        assert hasattr(self.env, 'creationist_male_pos'), "Missing creationist_male_pos"
        assert self.env.creationist_male_pos == (0, 5), "Wrong Creationist male position"
        
        assert hasattr(self.env, 'evolutionist_female_pos'), "Missing evolutionist_female_pos"
        assert self.env.evolutionist_female_pos == (7, 4), "Wrong Evolutionist female position"
        print("✓ Starting positions validated")

    def test_board_consistency(self):
        """Validate all cells contain valid pieces"""
        valid_pieces = {
            "Creationist_Earth", "Creationist_Water",
            "Evolutionist_Fire", "Evolutionist_Air",
            "Neutral"
        }
        
        for r, row in enumerate(self.env.board):
            for c, piece in enumerate(row):
                assert piece in valid_pieces, f"Invalid piece '{piece}' at ({r},{c})"
        print("✓ Board consistency validated")

def run_tests():
    """Alternative test runner if not using pytest"""
    print("\n=== Running Board Validation ===")
    tester = TestBoardInitialization()
    
    tests = [
        tester.test_board_dimensions,
        tester.test_initial_piece_placement,
        tester.test_starting_positions,
        tester.test_board_consistency
    ]
    
    failures = 0
    for test in tests:
        tester.setup_method()  # Reset env before each test
        try:
            test()
        except AssertionError as e:
            failures += 1
            print(f"❌ {test.__name__} failed: {e}")
        except Exception as e:
            failures += 1
            print(f"💥 {test.__name__} crashed: {e}")
    
    print(f"\n{'✅' if failures == 0 else '❌'} {len(tests)-failures}/{len(tests)} tests passed")

if __name__ == "__main__":
    run_tests()