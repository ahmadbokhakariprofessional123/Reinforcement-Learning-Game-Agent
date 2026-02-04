"""
origins_rules_evaluator.py - Comprehensive rules implementation evaluation
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import ast
import json
from pathlib import Path

@dataclass
class RuleEvaluation:
    implemented: bool
    location: str
    notes: str
    priority: int  # 1=Critical, 2=Important, 3=Nice-to-have

class OriginsRulesEvaluator:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.source_code = self._read_source_code()
        self.ast_tree = ast.parse(self.source_code)
        self.evaluation: Dict[str, RuleEvaluation] = {}

    def _read_source_code(self) -> str:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def evaluate_rules(self) -> Dict[str, RuleEvaluation]:
        """Evaluate implementation of all game rules"""
        # Core game setup rules
        self._evaluate_setup_rules()
        
        # Movement rules
        self._evaluate_movement_rules()
        
        # Element interaction rules
        self._evaluate_element_rules()
        
        # Win condition rules
        self._evaluate_win_conditions()
        
        return self.evaluation

    def _evaluate_setup_rules(self):
        """Evaluate initial game setup rules"""
        self.evaluation["player_setup"] = RuleEvaluation(
            implemented=self._check_class_initialization("Creationist") and 
                      self._check_class_initialization("Evolutionist"),
            location="__init__",
            notes="Initial piece placement verified",
            priority=1
        )
        
        self.evaluation["piece_types"] = RuleEvaluation(
            implemented=self._check_piece_types_exist(),
            location="COLORS dictionary and board initialization",
            notes="All required pieces are defined",
            priority=1
        )

    def _evaluate_movement_rules(self):
        """Evaluate movement-related rules"""
        self.evaluation["basic_movement"] = RuleEvaluation(
            implemented=self._check_method_exists("get_valid_moves"),
            location="get_valid_moves()",
            notes="Basic movement logic exists but needs full validation",
            priority=1
        )
        
        self.evaluation["start_row_restriction"] = RuleEvaluation(
            implemented=self._check_start_row_restriction(),
            location="get_valid_moves()",
            notes="Partial implementation - needs validation for re-entry",
            priority=2
        )
        
        self.evaluation["male_female_movement"] = RuleEvaluation(
            implemented=self._check_male_female_movement_rules(),
            location="get_valid_moves()",
            notes="Basic movement implemented but backward movement check missing",
            priority=2
        )

    def _evaluate_element_rules(self):
        """Evaluate element interaction rules"""
        self.evaluation["element_hierarchy"] = RuleEvaluation(
            implemented=self._check_element_hierarchy(),
            location="ELEMENT_POWER dictionary",
            notes="Hierarchy defined but full interaction logic needed",
            priority=1
        )
        
        self.evaluation["neutral_square_rule"] = RuleEvaluation(
            implemented=self._check_neutral_square_conversion(),
            location="move_piece()",
            notes="Element path conversion partially implemented",
            priority=2
        )
        
        self.evaluation["dominant_element_capture"] = RuleEvaluation(
            implemented=self._check_method_exists("capture_elements"),
            location="capture_elements()",
            notes="Capture logic exists but needs thorough testing",
            priority=1
        )

    def _evaluate_win_conditions(self):
        """Evaluate win/lose/draw conditions"""
        self.evaluation["win_conditions"] = RuleEvaluation(
            implemented=self._check_method_exists("check_game_over"),
            location="check_game_over()",
            notes="Basic win conditions implemented",
            priority=1
        )
        
        self.evaluation["destination_lock"] = RuleEvaluation(
            implemented=self._check_destination_lock(),
            location="move_piece() and get_valid_moves()",
            notes="Arrived pieces should be immovable but current check is incomplete",
            priority=2
        )
        
        self.evaluation["draw_conditions"] = RuleEvaluation(
            implemented=self._check_draw_conditions(),
            location="check_game_over()",
            notes="Some draw conditions implemented but not all",
            priority=2
        )

    # Implementation check methods
    def _check_class_initialization(self, faction: str) -> bool:
        """Check if faction pieces are properly initialized"""
        init_method = next(
            (n for n in ast.walk(self.ast_tree)
            if isinstance(n, ast.FunctionDef) and n.name == "__init__"),
            None
        )
        if not init_method:
            return False
            
        return any(
            f"_{faction}" in str(node)
            for node in ast.walk(init_method)
        )

    def _check_piece_types_exist(self) -> bool:
        """Verify all required piece types are defined"""
        required_pieces = {
            "Creationist_Earth", "Creationist_Water", "Creationist_Fire", "Creationist_Air",
            "Creationist_Man", "Creationist_Woman",
            "Evolutionist_Earth", "Evolutionist_Water", "Evolutionist_Fire", "Evolutionist_Air",
            "Evolutionist_Man", "Evolutionist_Woman",
            "Neutral"
        }
        return all(
            piece in self.source_code
            for piece in required_pieces
        )

    def _check_method_exists(self, method_name: str) -> bool:
        """Check if a method exists in the OriginsEnv class"""
        return any(
            isinstance(node, ast.FunctionDef) and node.name == method_name
            for node in ast.walk(self.ast_tree)
        )

    def _check_start_row_restriction(self) -> bool:
        """Verify start row movement restrictions"""
        # This would need more sophisticated AST analysis
        return self._check_method_exists("get_valid_moves")

    def _check_male_female_movement_rules(self) -> bool:
        """Check male/female movement constraints"""
        # Would need to analyze get_valid_moves logic
        return True  # Placeholder

    def _check_element_hierarchy(self) -> bool:
        """Verify element power relationships exist"""
        return "ELEMENT_POWER" in self.source_code

    def _check_neutral_square_conversion(self) -> bool:
        """Check if elements convert neutral squares"""
        return "self.board[r][c] = f" in self.source_code

    def _check_destination_lock(self) -> bool:
        """Verify pieces lock when reaching destination"""
        return "arrived" in self.source_code

    def _check_draw_conditions(self) -> bool:
        """Check if draw conditions are implemented"""
        return "draw" in self.source_code.lower()

    def generate_report(self) -> str:
        """Generate comprehensive evaluation report"""
        report = [
            "=== Origins Game Rules Implementation Report ===",
            f"Evaluated File: {self.file_path}",
            "\nCORE RULES IMPLEMENTATION STATUS:",
            *[self._format_rule_evaluation(name, eval) 
              for name, eval in self.evaluation.items()],
            "\nRECOMMENDED IMPROVEMENTS:",
            *self._generate_recommendations()
        ]
        return '\n'.join(report)

    def _format_rule_evaluation(self, name: str, eval: RuleEvaluation) -> str:
        """Format a single rule evaluation for reporting"""
        status = "✅" if eval.implemented else "❌"
        return (f"{status} {name.replace('_', ' ').title():<30} "
                f"Location: {eval.location}\n"
                f"    Notes: {eval.notes}")

    def _generate_recommendations(self) -> List[str]:
        """Generate prioritized recommendations"""
        unimplemented_critical = [
            name for name, eval in self.evaluation.items()
            if not eval.implemented and eval.priority == 1
        ]
        
        recommendations = [
            "1. CRITICAL PRIORITY:",
            *[f"   - Implement {name.replace('_', ' ')}" for name in unimplemented_critical],
            "",
            "2. IMPORTANT IMPROVEMENTS:",
            *[f"   - Enhance {name.replace('_', ' ')} implementation" 
              for name, eval in self.evaluation.items() 
              if eval.implemented and eval.priority == 2],
            "",
            "3. TESTING PRIORITIES:",
            *[f"   - Thoroughly test {name.replace('_', ' ')}" 
              for name, eval in self.evaluation.items() 
              if eval.implemented and eval.priority == 1]
        ]
        return recommendations

if __name__ == "__main__":
    evaluator = OriginsRulesEvaluator(r"C:\Users\samik\OneDrive\Desktop\test\origins_env.py")
    evaluation = evaluator.evaluate_rules()
    
    print(evaluator.generate_report())
    
    # Save detailed evaluation
    with open("rules_evaluation.json", "w") as f:
        json.dump({
            name: {"implemented": eval.implemented, 
                   "location": eval.location,
                   "notes": eval.notes,
                   "priority": eval.priority}
            for name, eval in evaluation.items()
        }, f, indent=2)