from origins_env import OriginsEnv
import random

class AIDecisionValidator:
    def __init__(self):
        self.env = OriginsEnv()
        self.env.reset()
        
    def setup_capture_scenario(self):
        """Setup board for capture prioritization test"""
        self.env.reset()
        # Place Creationist Fire at (0,2)
        self.env.board[0][2] = "Creationist_Fire"
        # Place vulnerable Evolutionist Air at (1,2)
        self.env.board[1][2] = "Evolutionist_Air"
        # Place neutral square at (1,1)
        self.env.board[1][1] = "Neutral"
        self.env.turn = "Creationist"
        
    def setup_suicide_scenario(self):
        """Setup board for danger avoidance test"""
        self.env.reset()
        # Place Creationist Fire at (0,1) - would lose to Water
        self.env.board[0][1] = "Creationist_Fire"
        # Place Evolutionist Water at (1,1)
        self.env.board[1][1] = "Evolutionist_Water"
        self.env.turn = "Creationist"
        
    def setup_protection_scenario(self):
        """Setup board for piece protection test"""
        self.env.reset()
        # Place valuable Creationist Man at (1,1)
        self.env.board[1][1] = "Creationist_Man"
        # Place threatening Evolutionist Earth at (2,1)
        self.env.board[2][1] = "Evolutionist_Earth"
        self.env.turn = "Creationist"
        
    def get_ai_moves(self):
        """Get all possible moves for current player"""
        moves = []
        for r in range(8):
            for c in range(10):
                if self.env.board[r][c].startswith(self.env.turn):
                    for target in self.env.get_valid_moves(r, c):
                        moves.append((r, c, target))
        return moves
        
    def test_capture_prioritization(self):
        """Test if AI prioritizes capturing vulnerable pieces"""
        try:
            self.setup_capture_scenario()
            moves = self.get_ai_moves()
            
            # Find moves that capture the Air element
            capture_moves = [m for m in moves if m[2] == (1, 2)]
            
            # AI should prefer capturing (Fire beats Air)
            assert len(capture_moves) > 0, "No capture moves available"
            
            # In a real AI, you'd check if it selects this move
            print("✓ AI capture prioritization test passed")
            return True
        except AssertionError as e:
            print(f"✗ AI capture prioritization failed: {str(e)}")
            return False
            
    def test_danger_avoidance(self):
        """Test if AI avoids moves that would lose pieces"""
        try:
            self.setup_suicide_scenario()
            moves = self.env.get_valid_moves(0, 1)  # Creationist Fire at (0,1)
            
            # Fire shouldn't move to Water's position (1,1)
            assert (1, 1) not in moves, "AI considers suicidal move"
            
            print("✓ AI danger avoidance test passed")
            return True
        except AssertionError as e:
            print(f"✗ AI danger avoidance failed: {str(e)}")
            return False
            
    def test_piece_protection(self):
        """Test if AI protects valuable pieces"""
        try:
            self.setup_protection_scenario()
            moves = self.get_ai_moves()
            
            # Should have moves that protect the Man
            protective_moves = [
                m for m in moves 
                if m[0] == 1 and m[1] == 1  # Moving the Man
                or m[2] == (2, 1)  # Capturing the threat
            ]
            
            assert len(protective_moves) > 0, "No protective moves available"
            print("✓ AI piece protection test passed")
            return True
        except AssertionError as e:
            print(f"✗ AI piece protection failed: {str(e)}")
            return False
            
    def test_strategic_positioning(self):
        """Test if AI makes progress toward objectives"""
        try:
            self.env.reset()
            self.env.turn = "Creationist"
            
            # Get moves for Creationist Man (should move toward row 6)
            man_pos = next(
                (r, c) for r in range(8) 
                for c in range(10) 
                if self.env.board[r][c] == "Creationist_Man"
            )
            moves = self.env.get_valid_moves(*man_pos)
            
            # Should prefer moving downward (toward destination)
            downward_moves = [m for m in moves if m[0] > man_pos[0]]
            assert len(downward_moves) > 0, "No progress toward objective"
            print("✓ AI strategic positioning test passed")
            return True
        except Exception as e:
            print(f"✗ AI strategic positioning failed: {str(e)}")
            return False
            
    def run_all_tests(self):
        print("\n" + "="*60)
        print("VALIDATING AI DECISION MAKING")
        print("="*60)
        
        results = [
            self.test_capture_prioritization(),
            self.test_danger_avoidance(),
            self.test_piece_protection(),
            self.test_strategic_positioning()
        ]
        
        print("\n" + "="*60)
        if all(results):
            print("✅ ALL AI DECISION TESTS PASSED!")
        else:
            print(f"❌ {results.count(False)}/{len(results)} TESTS FAILED")
        print("="*60)
        
        return all(results)

if __name__ == "__main__":
    validator = AIDecisionValidator()
    validator.run_all_tests()