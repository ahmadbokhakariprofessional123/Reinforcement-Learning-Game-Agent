"""
origins_game_validator.py - Complete and fixed validation for Origins game
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Tuple
import inspect

@dataclass
class TestResult:
    passed: bool
    message: str
    details: dict = None

class OriginsGameValidator:
    def __init__(self):
        from origins_env import OriginsEnv  # Import your actual game class
        self.env = OriginsEnv()
        self.results: List[TestResult] = []
    
    def run_all_checks(self) -> List[TestResult]:
        """Execute all validation checks"""
        check_methods = [
            self.check_element_conversion,
            self.check_gender_movement_restrictions,
            self.check_destination_lock,
            self.check_element_dominance,
            self.check_start_row_reentry,
            self.check_piece_capture,
            self.check_draw_conditions,
            self.check_element_chain_reactions,
            self.check_equal_element_blockade,
            self.check_multi_turn_strategy
        ]
        
        for method in check_methods:
            try:
                method()
            except Exception as e:
                self.results.append(TestResult(
                    False,
                    f"Test {method.__name__} crashed: {str(e)}",
                    {"error": str(e)}
                ))
        
        return self.results

    def check_element_conversion(self):
        """Verify neutral squares convert when elements move"""
        self.env.reset()
        test_cases = [
            ("Creationist_Earth", [(1,0), (2,0)]),
            ("Evolutionist_Fire", [(6,9), (6,8)])
        ]
        
        for element, path in test_cases:
            start_pos = (0,0) if "Creationist" in element else (7,9)
            self.env.board[start_pos[0]][start_pos[1]] = element
            
            for r, c in path:
                self.env.move_piece(start_pos, (r,c))
                if self.env.board[r][c] != element:
                    self.results.append(TestResult(
                        False,
                        f"{element} failed to convert square at ({r},{c})",
                        {"expected": element, "actual": self.env.board[r][c]}
                    ))
                    break
            else:
                self.results.append(TestResult(
                    True,
                    f"{element} correctly converted path {path}",
                    {"path": path}
                ))

    def check_gender_movement_restrictions(self):
        """Verify male/female pieces can't move backward"""
        self.env.reset()
        test_cases = [
            ("Creationist_Man", (0,5), (1,5), (-1,5)),
            ("Evolutionist_Woman", (7,4), (6,4), (8,4))
        ]
        
        for piece, start, valid_move, invalid_move in test_cases:
            self.env.board[start[0]][start[1]] = piece
            moves = self.env.get_valid_moves(*start)
            
            if valid_move not in moves:
                self.results.append(TestResult(
                    False,
                    f"{piece} missing valid move to {valid_move}",
                    {"position": start, "valid_moves": moves}
                ))
            
            if invalid_move in moves:
                self.results.append(TestResult(
                    False,
                    f"{piece} can illegally move to {invalid_move}",
                    {"position": start, "invalid_move": invalid_move}
                ))
            else:
                self.results.append(TestResult(
                    True,
                    f"{piece} movement constraints working at {start}",
                    {"valid_moves": moves}
                ))

    def check_destination_lock(self):
        """Verify pieces lock when reaching destination"""
        self.env.reset()
        test_cases = [
            ("Creationist_Woman", 6, 4),
            ("Evolutionist_Man", 1, 5)
        ]
        
        for piece, dest_row, col in test_cases:
            self.env.board[dest_row][col] = piece
            setattr(self.env, f"{piece.split('_')[0].lower()}_{'female' if 'Woman' in piece else 'male'}_arrived", True)
            
            if self.env.get_valid_moves(dest_row, col):
                self.results.append(TestResult(
                    False,
                    f"{piece} remains movable at destination ({dest_row},{col})",
                    {"position": (dest_row, col)}
                ))
            else:
                self.results.append(TestResult(
                    True,
                    f"{piece} correctly locked at destination",
                    {"position": (dest_row, col)}
                ))

    def check_element_dominance(self):
        """Test all element power relationships"""
        self.env.reset()
        test_cases = [
            ("Earth", "Water", True),
            ("Water", "Fire", True),
            ("Fire", "Air", True),
            ("Air", "Earth", True),
            ("Earth", "Fire", False),
            ("Water", "Air", False)
        ]
        
        for attacker, defender, should_capture in test_cases:
            self.env.board[3][3] = f"Creationist_{attacker}"
            self.env.board[3][4] = f"Evolutionist_{defender}"
            original = self.env.board[3][4]
            
            self.env.move_piece((3,3), (3,5))
            result = self.env.board[3][4]
            
            if (should_capture and result != "Neutral") or (not should_capture and result != original):
                self.results.append(TestResult(
                    False,
                    f"Element dominance failed: {attacker} vs {defender}",
                    {"expected": "Neutral" if should_capture else original, "actual": result}
                ))
            else:
                self.results.append(TestResult(
                    True,
                    f"Element dominance passed: {attacker} vs {defender}",
                    {"outcome": "captured" if should_capture else "blocked"}
                ))

    def check_start_row_reentry(self):
        """Verify pieces can't re-enter starting rows"""
        self.env.reset()
        test_cases = [
            ("Creationist_Earth", 0, 0, 1, 0),
            ("Evolutionist_Water", 7, 9, 6, 9)
        ]
        
        for piece, start_r, start_c, move_r, move_c in test_cases:
            self.env.board[start_r][start_c] = piece
            self.env.move_piece((start_r, start_c), (move_r, move_c))
            moves = self.env.get_valid_moves(move_r, move_c)
            
            if (start_r, start_c) in moves:
                self.results.append(TestResult(
                    False,
                    f"{piece} can illegally re-enter start row",
                    {"from": (move_r, move_c), "invalid_move": (start_r, start_c)}
                ))
            else:
                self.results.append(TestResult(
                    True,
                    f"{piece} correctly blocked from re-entering start row",
                    {"position": (move_r, move_c)}
                ))

    def check_piece_capture(self):
        """Verify male/female capture requires element neutralization"""
        self.env.reset()
        test_cases = [
            ("Creationist_Fire", "Evolutionist_Man", "Air", True),
            ("Creationist_Water", "Evolutionist_Woman", "Fire", True),
            ("Evolutionist_Air", "Creationist_Man", "Earth", True),
            ("Creationist_Earth", "Evolutionist_Woman", "Water", False)
        ]
        
        for attacker, target, base_element, should_capture in test_cases:
            self.env.board[3][3] = attacker
            self.env.board[3][4] = f"{target.split('_')[0]}_{base_element}"
            self.env.board[3][4] = target
            
            if "Man" in target:
                setattr(self.env, f"{target.split('_')[0].lower()}_male_pos", (3,4))
            else:
                setattr(self.env, f"{target.split('_')[0].lower()}_female_pos", (3,4))
            
            original = self.env.board[3][4]
            self.env.move_piece((3,3), (3,5))
            
            if should_capture:
                if self.env.board[3][4] != "Neutral":
                    self.results.append(TestResult(
                        False,
                        f"Failed to capture {target} with {attacker}",
                        {"attacker": attacker, "target": target, "actual": self.env.board[3][4]}
                    ))
                else:
                    self.results.append(TestResult(
                        True,
                        f"Correctly captured {target} with {attacker}",
                        {"attacker": attacker, "target": target}
                    ))
            else:
                if self.env.board[3][4] != original:
                    self.results.append(TestResult(
                        False,
                        f"Wrongly captured {target} with {attacker}",
                        {"attacker": attacker, "target": target, "actual": self.env.board[3][4]}
                    ))
                else:
                    self.results.append(TestResult(
                        True,
                        f"Correctly blocked capture of {target} with {attacker}",
                        {"attacker": attacker, "target": target}
                    ))

    def check_draw_conditions(self):
        """Test draw scenarios"""
        self.env.reset()
        
        # Test 1: Both genders lost
        self.env.creationist_male_pos = None
        self.env.creationist_female_pos = None
        self.env.evolutionist_male_pos = None
        self.env.evolutionist_female_pos = None
        
        if not self.env.check_game_over():
            self.results.append(TestResult(
                False,
                "Draw condition not detected: both genders lost",
                {}
            ))
        else:
            self.results.append(TestResult(
                True,
                "Correctly detected draw: both genders lost",
                {}
            ))
        
        # Test 2: No valid moves
        self.env.reset()
        original_get_valid_moves = self.env.get_valid_moves
        self.env.get_valid_moves = lambda *args: []
        
        try:
            if not self.env.check_game_over():
                self.results.append(TestResult(
                    False,
                    "Draw condition not detected: no valid moves",
                    {}
                ))
            else:
                self.results.append(TestResult(
                    True,
                    "Correctly detected draw: no valid moves",
                    {}
                ))
        finally:
            self.env.get_valid_moves = original_get_valid_moves

    def check_element_chain_reactions(self):
        """Verify element conversions trigger chain reactions"""
        self.env.reset()
        self.env.board[3][3] = "Creationist_Water"
        self.env.board[3][2] = "Evolutionist_Fire"
        self.env.board[3][4] = "Evolutionist_Fire"
        self.env.board[2][3] = "Evolutionist_Fire"
        self.env.board[4][3] = "Evolutionist_Fire"
        
        self.env.move_piece((3,3), (3,5))
        
        failed = []
        for r,c in [(3,2), (3,4), (2,3), (4,3)]:
            if self.env.board[r][c] != "Neutral":
                failed.append((r,c))
        
        if failed:
            self.results.append(TestResult(
                False,
                "Chain reaction failed at positions",
                {"positions": failed, "expected": "Neutral"}
            ))
        else:
            self.results.append(TestResult(
                True,
                "Element chain reactions working correctly",
                {"converted": [(3,2), (3,4), (2,3), (4,3)]}
            ))

    def check_equal_element_blockade(self):
        """Verify equal strength elements block each other"""
        self.env.reset()
        pairs = [("Earth", "Fire"), ("Water", "Air")]
        
        for elem1, elem2 in pairs:
            self.env.board[3][3] = f"Creationist_{elem1}"
            self.env.board[3][4] = f"Evolutionist_{elem2}"
            moves = self.env.get_valid_moves(3,3)
            
            if (3,4) in moves:
                self.results.append(TestResult(
                    False,
                    f"{elem1} can illegally move through {elem2}",
                    {"elements": (elem1, elem2)}
                ))
            else:
                self.results.append(TestResult(
                    True,
                    f"{elem1} correctly blocked by {elem2}",
                    {"elements": (elem1, elem2)}
                ))

    def check_multi_turn_strategy(self):
        """Test a complete 3-turn strategy"""
        self.env.reset()
        strategy = [
            ("Creationist_Earth", (0,0), (3,0)),
            ("Creationist_Man", (0,5), (1,5)),
            ("Creationist_Water", (0,1), (3,3))
        ]
        
        failed = []
        for piece, start, end in strategy:
            if end not in self.env.get_valid_moves(*start):
                failed.append((piece, start, end))
            self.env.move_piece(start, end)
        
        if failed:
            self.results.append(TestResult(
                False,
                "Multi-turn strategy failed at steps",
                {"failed_steps": failed}
            ))
        else:
            checks = [
                (self.env.board[3][0] == "Creationist_Earth", "Earth path"),
                (self.env.board[1][5] == "Creationist_Man", "Male advance"),
                (any(self.env.board[3][c] == "Creationist_Water" for c in [2,3,4]), "Flank attack")
            ]
            
            failed_checks = [desc for passed, desc in checks if not passed]
            if failed_checks:
                self.results.append(TestResult(
                    False,
                    "Strategy failed final state checks",
                    {"failed_checks": failed_checks}
                ))
            else:
                self.results.append(TestResult(
                    True,
                    "Multi-turn strategy executed successfully",
                    {"steps": [s[0] for s in strategy]}
                ))

    def generate_report(self, filename="game_validation_report.json"):
        """Generate comprehensive validation report"""
        report = {
            "summary": {
                "total_tests": len(self.results),
                "passed": sum(1 for r in self.results if r.passed),
                "failed": sum(1 for r in self.results if not r.passed),
                "success_rate": f"{sum(1 for r in self.results if r.passed)/len(self.results)*100:.1f}%"
            },
            "details": [
                {
                    "test": method.__name__,
                    "passed": result.passed,
                    "message": result.message,
                    **({} if result.details is None else {"details": result.details})
                }
                for method, result in zip(
                    [getattr(self, name) for name in dir(self) if name.startswith('check_')],
                    self.results
                )
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report

if __name__ == "__main__":
    validator = OriginsGameValidator()
    print("Running Origins Game Validation...")
    results = validator.run_all_checks()
    
    # Print summary
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"\nValidation Results: {passed}/{total} passed ({passed/total*100:.1f}%)")
    
    # Generate report
    report = validator.generate_report()
    print(f"Detailed report saved to game_validation_report.json")
    
    # Show failures
    failures = [r for r in results if not r.passed]
    if failures:
        print("\nCritical Failures:")
        for fail in failures[:3]:
            print(f"- {fail.message}")
        if len(failures) > 3:
            print(f"- Plus {len(failures)-3} more...")
    else:
        print("\nAll tests passed successfully!")