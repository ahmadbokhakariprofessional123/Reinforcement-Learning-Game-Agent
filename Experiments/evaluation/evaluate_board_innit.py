"""
board_evaluation.py - Comprehensive evaluation of OriginsEnv board initialization
"""

from origins_env import OriginsEnv
import pytest

class BoardEvaluator:
    """Comprehensive evaluation of board initialization"""
    
    def __init__(self):
        self.env = None
        self.valid_pieces = {
            "Creationist_Earth", "Creationist_Water",
            "Evolutionist_Earth", "Evolutionist_Fire", 
            "Evolutionist_Air", "Evolutionist_Water",
            "Neutral"
        }
        self.reset_environment()
    
    def reset_environment(self):
        """Create fresh environment instance"""
        self.env = OriginsEnv()
    
    def evaluate_dimensions(self):
        """Check board has correct 8x10 dimensions"""
        assert len(self.env.board) == 8, "Board must have exactly 8 rows"
        assert all(len(row) == 10 for row in self.env.board), "All rows must have 10 columns"
        return True
    
    def evaluate_corner_pieces(self):
        """Verify key corner pieces are placed correctly"""
        assert self.env.board[0][0] == "Creationist_Earth", "Top-left should be Creationist Earth"
        assert self.env.board[7][9] == "Evolutionist_Earth", "Bottom-right should be Evolutionist Earth"
        return True
    
    def evaluate_starting_positions(self):
        """Check human character starting positions"""
        assert hasattr(self.env, 'creationist_male_pos'), "Missing creationist_male_pos attribute"
        assert self.env.creationist_male_pos == (0, 5), "Creationist male at wrong position"
        
        assert hasattr(self.env, 'evolutionist_female_pos'), "Missing evolutionist_female_pos attribute"
        assert self.env.evolutionist_female_pos == (7, 4), "Evolutionist female at wrong position"
        return True
    
    def evaluate_board_consistency(self):
        """Validate all cells contain valid pieces"""
        for r, row in enumerate(self.env.board):
            for c, piece in enumerate(row):
                assert piece in self.valid_pieces, f"Invalid piece '{piece}' at ({r},{c})"
        return True
    
    def evaluate_all(self):
        """Run all evaluations with comprehensive reporting"""
        results = {
            'dimensions': False,
            'corner_pieces': False,
            'starting_positions': False,
            'board_consistency': False
        }
        
        try:
            results['dimensions'] = self.evaluate_dimensions()
        except AssertionError as e:
            print(f"❌ Dimension check failed: {e}")
        
        self.reset_environment()
        try:
            results['corner_pieces'] = self.evaluate_corner_pieces()
        except AssertionError as e:
            print(f"❌ Corner pieces check failed: {e}")
        
        self.reset_environment()
        try:
            results['starting_positions'] = self.evaluate_starting_positions()
        except AssertionError as e:
            print(f"❌ Starting positions check failed: {e}")
        
        self.reset_environment()
        try:
            results['board_consistency'] = self.evaluate_board_consistency()
        except AssertionError as e:
            print(f"❌ Board consistency check failed: {e}")
        
        passed = sum(results.values())
        total = len(results)
        
        print("\n=== Evaluation Summary ===")
        for name, success in results.items():
            status = "✓" if success else "✗"
            print(f"{status} {name.replace('_', ' ')}")
        
        print(f"\nOverall: {passed}/{total} checks passed")
        return passed == total

def run_evaluation():
    """Run comprehensive evaluation"""
    print("=== OriginsEnv Board Evaluation ===")
    evaluator = BoardEvaluator()
    success = evaluator.evaluate_all()
    
    if success:
        print("\n✅ All board initialization checks passed successfully!")
    else:
        print("\n❌ Some board initialization checks failed. See above for details.")
    
    return success

if __name__ == "__main__":
    run_evaluation()