"""
elemental_validation.py - Advanced validation for special movement mechanics
Validates fire spread, water blocking, and air jumping with edge case testing.
"""

from origins_env import OriginsEnv
import pytest

class TestElementalMechanics:
    """Validation suite for elemental movement rules"""
    
    def setup_method(self):
        """Initialize a fresh environment for each test"""
        self.env = OriginsEnv()
        # Ensure clean starting state
        for r in range(8):
            for c in range(10):
                if r > 1 and r < 6:  # Clear center board
                    self.env.board[r][c] = "Neutral"
    
    def validate_fire_spread(self):
        """Test fire propagation to adjacent neutral tiles"""
        # Setup
        self.env.board[1][1] = "Neutral"
        self.env.board[0][2] = "Creationist_Fire"
        
        # Execute
        self.env.move_piece((0, 2), (1, 1))
        
        # Verify spread pattern (at least one adjacent)
        spread_targets = [(1,0), (1,2), (0,1), (2,1)]
        spread_occurred = any(
            self.env.board[r][c] == "Creationist_Fire" 
            for r, c in spread_targets
            if 0 <= r < 8 and 0 <= c < 10
        )
        
        assert spread_occurred, (
            f"Fire should spread to at least one adjacent neutral tile\n"
            f"Board state:\n{self._format_board()}"
        )
        
        # Verify original fire position cleared
        assert self.env.board[0][2] == "Neutral", "Original fire position should clear"
        
        print("✓ Fire spread validated: Flames propagate correctly")

    def validate_water_blocking(self):
        """Test water-earth interaction rules"""
        # Setup obstacles
        self.env.board[1][1] = "Evolutionist_Water"
        self.env.board[2][2] = "Creationist_Earth"
        self.env.board[2][0] = "Neutral"  # Valid move target
        
        # Get valid moves
        water_moves = self.env.get_valid_moves(1, 1)
        
        # Earth should block
        assert (2, 2) not in water_moves, (
            f"Water should be blocked by Earth\n"
            f"Invalid moves present: {water_moves}"
        )
        
        # Water should flow to neutral
        assert (2, 0) in water_moves, "Water should flow to neutral tiles"
        
        print("✓ Water blocking validated: Earth creates dam effect")

    def validate_air_jumping(self):
        """Test air's ability to traverse obstacles"""
        # Setup obstacle course
        self.env.board[1][1] = "Creationist_Air"
        self.env.board[2][2] = "Evolutionist_Fire"  # Obstacle
        self.env.board[3][3] = "Neutral"  # Landing zone
        
        # Get valid moves
        air_moves = self.env.get_valid_moves(1, 1)
        
        # Verify jump capability
        assert (3, 3) in air_moves, (
            f"Air should jump over Fire to (3,3)\n"
            f"Actual moves: {air_moves}"
        )
        
        # Verify can't land on obstacle
        assert (2, 2) not in air_moves, "Air shouldn't land directly on Fire"
        
        print("✓ Air jump validated: Can traverse obstacles")

    def validate_elemental_interactions(self):
        """Test combined elemental effects"""
        # Complex setup
        self.env.board[1][1] = "Creationist_Fire"
        self.env.board[2][2] = "Evolutionist_Water"
        self.env.board[3][3] = "Creationist_Earth"
        
        # Fire spreads should respect water
        spread_targets = self.env._get_adjacent(1, 1)
        for r, c in spread_targets:
            if self.env.board[r][c] == "Neutral":
                self.env.board[r][c] = "Creationist_Fire"
        
        # Water shouldn't move toward earth
        water_moves = self.env.get_valid_moves(2, 2)
        assert (3, 3) not in water_moves, "Water should avoid Earth despite fire spread"
        
        print("✓ Elemental interaction network validated")

    def _format_board(self):
        """Helper for visual board output"""
        return "\n".join(" ".join(f"{cell:<15}" for cell in row) 
                        for row in self.env.board)

def run_validation():
    """Execute all validation tests with detailed reporting"""
    print("\n=== Elemental Mechanics Validation Suite ===")
    tester = TestElementalMechanics()
    
    tests = [
        tester.validate_fire_spread,
        tester.validate_water_blocking,
        tester.validate_air_jumping,
        tester.validate_elemental_interactions
    ]
    
    failures = 0
    for test in tests:
        tester.setup_method()
        try:
            test()
        except AssertionError as e:
            failures += 1
            print(f"\n❌ {test.__name__} FAILED")
            print(f"   Error: {str(e)}")
            if hasattr(tester, '_format_board'):
                print(f"\nBoard State:\n{tester._format_board()}")
        except Exception as e:
            failures += 1
            print(f"\n💥 {test.__name__} CRASHED")
            print(f"   Exception: {str(e)}")
    
    # Summary
    if failures == 0:
        print("\n✅ All elemental mechanics validated successfully!")
    else:
        print(f"\n🔴 Validation issues: {failures}/{len(tests)} tests failed")
    
    return failures == 0

if __name__ == "__main__":
    run_validation()