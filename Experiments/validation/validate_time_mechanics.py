"""
time_validation.py - Validation tests for temporal game mechanics
Validates destination timing, turn limits, and temporal progression rules.
"""

from origins_env import OriginsEnv
import pytest

class TestTimeMechanics:
    """Validation suite for time-based game mechanics"""
    
    def setup_method(self):
        """Initialize a fresh game environment"""
        self.env = OriginsEnv()
    
    def validate_creationist_journey(self):
        """Test Creationist's 6-day journey completion"""
        # Initial position check
        assert self.env.creationist_male_pos == (0, 5), \
            "Creationist man should start at (0,5)"
        
        # Simulate movement
        self.env.move_piece((0, 5), (6, 5))
        
        # Validate arrival
        assert hasattr(self.env, 'creationist_male_arrived'), \
            "Missing arrival tracking attribute"
        assert self.env.creationist_male_arrived, \
            "Creationist should arrive after reaching row 6"
            
        # Validate day counter
        if hasattr(self.env, 'days_passed'):
            assert self.env.days_passed == 6, \
                "Should track 6 days of journey"
        
        print("✓ Creationist timing validated: 6-day journey")

    def validate_evolutionist_journey(self):
        """Test Evolutionist's 6M-year journey completion"""
        # Switch to Evolutionist turn
        self.env.turn = "Evolutionist"
        
        # Initial position check
        assert self.env.evolutionist_male_pos == (7, 5), \
            "Evolutionist man should start at (7,5)"
        
        # Simulate movement
        self.env.move_piece((7, 5), (1, 5))
        
        # Validate arrival
        assert hasattr(self.env, 'evolutionist_male_arrived'), \
            "Missing arrival tracking attribute"
        assert self.env.evolutionist_male_arrived, \
            "Evolutionist should arrive after reaching row 1"
            
        # Validate year counter
        if hasattr(self.env, 'years_passed'):
            assert self.env.years_passed == 6, \
                "Should track 6M years of journey"
        
        print("✓ Evolutionist timing validated: 6M-year journey")

    def validate_temporal_mechanics(self):
        """Test time progression rules"""
        # Verify initial state
        assert not getattr(self.env, 'creationist_male_arrived', True), \
            "Creationist should start unarrived"
        assert not getattr(self.env, 'evolutionist_male_arrived', True), \
            "Evolutionist should start unarrived"
        
        # Test partial journeys
        self.env.move_piece((0, 5), (3, 5))  # Halfway for Creationist
        assert not getattr(self.env, 'creationist_male_arrived', True), \
            "Shouldn't arrive at halfway point"
            
        self.env.turn = "Evolutionist"
        self.env.move_piece((7, 5), (4, 5))  # Halfway for Evolutionist
        assert not getattr(self.env, 'evolutionist_male_arrived', True), \
            "Shouldn't arrive at halfway point"
        
        print("✓ Partial journey validation passed")

    def validate_stalemate_conditions(self):
        """Test game termination after maximum turns"""
        # Simulate max turns
        for turn in range(100):
            self.env.turn = "Creationist" if turn % 2 == 0 else "Evolutionist"
            if hasattr(self.env, 'increment_turn_counter'):
                self.env.increment_turn_counter()
            
            # Early exit if game ends prematurely
            if self.env.check_game_over():
                break
                
        # Verify game ended
        assert self.env.check_game_over(), \
            "Game should terminate after maximum turns"
            
        # Verify stalemate condition
        if hasattr(self.env, 'game_result'):
            assert self.env.game_result == "Stalemate", \
                "Should declare stalemate after turn limit"
        
        print("✓ Turn limit stalemate validated")

def run_validation():
    """Execute all validation tests with detailed reporting"""
    print("\n=== Temporal Mechanics Validation Suite ===")
    tester = TestTimeMechanics()
    
    tests = [
        tester.validate_creationist_journey,
        tester.validate_evolutionist_journey,
        tester.validate_temporal_mechanics,
        tester.validate_stalemate_conditions
    ]
    
    failures = 0
    for test in tests:
        tester.setup_method()  # Reset environment
        try:
            test()
        except AssertionError as e:
            failures += 1
            print(f"\n❌ {test.__name__} FAILED")
            print(f"   Error: {str(e)}")
        except Exception as e:
            failures += 1
            print(f"\n💥 {test.__name__} CRASHED")
            print(f"   Exception: {str(e)}")
    
    # Summary report
    if failures == 0:
        print("\n✅ All temporal mechanics validated successfully!")
    else:
        print(f"\n🔴 {failures} temporal validation failures detected")
    
    return failures == 0

if __name__ == "__main__":
    run_validation()