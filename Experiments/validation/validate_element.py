from origins_env import OriginsEnv, ELEMENT_POWER

class ElementInteractionTester:
    def __init__(self):
        self.env = OriginsEnv()
        self.env.reset()
        self.setup_initial_board()

    def setup_initial_board(self):
        """Ensure all elements are in their expected starting positions"""
        # Creationist pieces (top row)
        self.env.board[0] = [
            "Creationist_Earth", "Creationist_Water", 
            "Creationist_Fire", "Creationist_Air",
            "Creationist_Woman", "Creationist_Man",
            "Creationist_Air", "Creationist_Fire",
            "Creationist_Water", "Creationist_Earth"
        ]
        
        # Evolutionist pieces (bottom row)
        self.env.board[7] = [
            "Evolutionist_Earth", "Evolutionist_Water",
            "Evolutionist_Fire", "Evolutionist_Air",
            "Evolutionist_Woman", "Evolutionist_Man",
            "Evolutionist_Air", "Evolutionist_Fire",
            "Evolutionist_Water", "Evolutionist_Earth"
        ]

    def test_element_hierarchy(self):
        """Verify the elemental power relationships"""
        try:
            assert ELEMENT_POWER["Earth"] == "Water", "Earth should beat Water"
            assert ELEMENT_POWER["Water"] == "Fire", "Water should beat Fire"
            assert ELEMENT_POWER["Fire"] == "Air", "Fire should beat Air"
            assert ELEMENT_POWER["Air"] == "Earth", "Air should beat Earth"
            print("✓ Element hierarchy test passed")
            return True
        except AssertionError as e:
            print(f"✗ Element hierarchy test failed: {str(e)}")
            return False

    def test_element_capture(self, attacker_type, defender_type, attacker_pos, capture_pos):
        """Test if one element can capture another"""
        try:
            # Set up the scenario
            self.env.reset()
            self.setup_initial_board()
            
            # Place defender
            self.env.board[capture_pos[0]][capture_pos[1]] = f"Evolutionist_{defender_type}"
            
            # Move attacker
            self.env.move_piece(attacker_pos, capture_pos)
            
            # Verify result
            result = self.env.board[capture_pos[0]][capture_pos[1]]
            expected = f"Creationist_{attacker_type}"
            assert result == expected, f"{attacker_type} should capture {defender_type}"
            print(f"✓ {attacker_type} vs {defender_type} capture test passed")
            return True
        except Exception as e:
            print(f"✗ {attacker_type} vs {defender_type} test failed: {str(e)}")
            return False

    def run_all_tests(self):
        print("\n" + "="*60)
        print("RUNNING ELEMENT INTERACTION VALIDATION TESTS")
        print("="*60)
        
        success = True
        
        # Test hierarchy
        if not self.test_element_hierarchy():
            success = False
        
        # Test all capture scenarios
        capture_tests = [
            ("Fire", "Air", (0, 2), (1, 2)),    # Fire at (0,2) captures Air at (1,2)
            ("Water", "Fire", (0, 1), (1, 1)),  # Water at (0,1) captures Fire at (1,1)
            ("Air", "Earth", (0, 3), (1, 0)),   # Air at (0,3) captures Earth at (1,0)
            ("Earth", "Water", (0, 0), (1, 1))  # Earth at (0,0) captures Water at (1,1)
        ]
        
        for test in capture_tests:
            if not self.test_element_capture(*test):
                success = False
        
        # Print final results
        print("\n" + "="*60)
        if success:
            print("✅ ALL ELEMENT INTERACTION TESTS PASSED!")
        else:
            print("❌ SOME TESTS FAILED - CHECK OUTPUT ABOVE")
        print("="*60)
        
        return success

if __name__ == "__main__":
    tester = ElementInteractionTester()
    tester.run_all_tests()