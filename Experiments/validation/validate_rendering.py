# rendering_validation.py

from origins_env import OriginsEnv, COLORS

class TestRenderingValidation:
    """Class to validate color assignments and visual distinctions in the game environment."""

    def test_color_assignments(self):
        """Test that colors are assigned correctly to pieces."""
        assert COLORS["Creationist_Fire"] == (255, 0, 0), "Fire should be red"
        assert COLORS["Evolutionist_Water"] == (0, 0, 255), "Water should be blue"
        print("✓ Color assignment test passed")

    def test_piece_visual_distinction(self):
        """Test that factions have distinct colors."""
        assert COLORS["Creationist_Man"] != COLORS["Evolutionist_Man"], "Factions should have distinct colors"
        print("✓ Visual distinction test passed")

def run_rendering_validation_tests():
    """Run the rendering validation tests."""
    print("\n=== Running Rendering Validation Tests ===")
    tester = TestRenderingValidation()
    
    # Run the tests
    try:
        tester.test_color_assignments()
        tester.test_piece_visual_distinction()
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"💥 Test crashed: {e}")
    else:
        print("✅ All rendering tests passed!")

if __name__ == "__main__":
    run_rendering_validation_tests()