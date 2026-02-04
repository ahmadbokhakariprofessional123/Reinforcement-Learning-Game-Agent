

import ast
import json
from pathlib import Path
import numpy as np

class OriginsEnvEvaluator:
    def __init__(self):
        self.file_path = Path(r"C:\Users\samik\OneDrive\Desktop\test\origins_env.py")
        self.source_code = self._read_source_code()
        self.ast_tree = ast.parse(self.source_code)
        self.metrics = {
            'structure': {},
            'performance': {},
            'style': {},
            'potential_issues': [],
            'game_specific': {}
        }

    def _read_source_code(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"Game file not found at {self.file_path}")
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def evaluate(self):
        """Run all evaluation metrics"""
        self._analyze_class_structure()
        self._check_game_mechanics()
        self._detect_performance_issues()
        self._verify_style()
        self._find_potential_bugs()
        return self.metrics

    def _analyze_class_structure(self):
        """Evaluate the OriginsEnv class structure"""
        class_node = next(
            (n for n in ast.walk(self.ast_tree) 
             if isinstance(n, ast.ClassDef) and n.name == 'OriginsEnv'),
            None
        )
        
        if not class_node:
            raise ValueError("OriginsEnv class not found in the file")

        methods = [f for f in ast.walk(class_node) if isinstance(f, ast.FunctionDef)]
        self.metrics['structure'] = {
            'method_count': len(methods),
            'public_methods': [m.name for m in methods if not m.name.startswith('_')],
            'method_lengths': {m.name: len(m.body) for m in methods}
        }

    def _check_game_mechanics(self):
        """Verify core game rules implementation"""
        game_metrics = {
            'element_hierarchy': False,
            'piece_movement': False,
            'win_conditions': False,
            'ai_integration': False
        }

        # Check element power system
        for node in ast.walk(self.ast_tree):
            if (isinstance(node, ast.Assign) and 
                isinstance(node.targets[0], ast.Name) and 
                node.targets[0].id == 'ELEMENT_POWER'):
                game_metrics['element_hierarchy'] = True
                break

        # Check movement system
        method_names = [m.name for m in ast.walk(self.ast_tree) 
                       if isinstance(m, ast.FunctionDef)]
        game_metrics['piece_movement'] = all(
            m in method_names 
            for m in ['move_piece', 'get_valid_moves']
        )

        self.metrics['game_specific'] = game_metrics

    def _detect_performance_issues(self):
        """Identify potential performance bottlenecks"""
        hotspots = []
        board_scans = 0

        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.For):
                # Check for full board iteration
                targets = [t.id for t in ast.walk(node.target) if isinstance(t, ast.Name)]
                if any(t in ['GRID_ROWS', 'GRID_COLS'] for t in targets):
                    board_scans += 1
                    func = next(
                        (f for f in ast.walk(self.ast_tree) 
                         if isinstance(f, ast.FunctionDef) and node in ast.walk(f)),
                        None
                    )
                    if func:
                        hotspots.append(func.name)

        self.metrics['performance'] = {
            'board_scans': board_scans,
            'hotspots': list(set(hotspots)),
            'nested_loops': sum(
                1 for node in ast.walk(self.ast_tree) 
                if isinstance(node, ast.For) and 
                any(isinstance(parent, ast.For) for parent in ast.walk(node))
            )
        }

    def _verify_style(self):
        """Check code style consistency"""
        style_issues = []
        magic_numbers = set()

        for node in ast.walk(self.ast_tree):
            # Check for magic numbers
            if isinstance(node, ast.Num) and not any(
                isinstance(parent, ast.Assign) for parent in ast.walk(self.ast_tree)
            ):
                magic_numbers.add(node.n)

            # Check naming conventions
            if isinstance(node, ast.FunctionDef) and '_' not in node.name and node.name != node.name.lower():
                style_issues.append(f"Function '{node.name}' should use snake_case")

        self.metrics['style'] = {
            'magic_numbers': list(magic_numbers),
            'naming_issues': style_issues,
            'docstring_coverage': self._calculate_docstring_coverage()
        }

    def _calculate_docstring_coverage(self):
        """Calculate percentage of documented methods"""
        funcs = [n for n in ast.walk(self.ast_tree) if isinstance(n, ast.FunctionDef)]
        documented = sum(1 for f in funcs if ast.get_docstring(f))
        return documented / len(funcs) if funcs else 0

    def _find_potential_bugs(self):
        """Detect potential logical issues"""
        issues = []

        # Check position tracking
        pos_attrs = ['male_pos', 'female_pos']
        for node in ast.walk(self.ast_tree):
            if (isinstance(node, ast.Attribute) and 
                any(attr in node.attr for attr in pos_attrs) and
                any(isinstance(parent, ast.Assign) for parent in ast.walk(self.ast_tree))):
                issues.append(f"Position tracking - verify null checks for {node.attr}")

        self.metrics['potential_issues'] = issues

    def generate_report(self):
        """Generate comprehensive evaluation report"""
        report = [
            "=== Origins Game Evaluation Report ===",
            f"File: {self.file_path}",
            "\n[STRUCTURE]",
            f"- Methods: {self.metrics['structure'].get('method_count', 0)}",
            f"- Longest method: {max(self.metrics['structure'].get('method_lengths', {}).values(), default=0)} lines",
            "\n[GAME MECHANICS]",
            *[f"- {k}: {'✅' if v else '❌'}" for k, v in self.metrics['game_specific'].items()],
            "\n[PERFORMANCE]",
            f"- Full board scans: {self.metrics['performance'].get('board_scans', 0)}",
            f"- Nested loops: {self.metrics['performance'].get('nested_loops', 0)}",
            f"- Hotspots: {', '.join(self.metrics['performance'].get('hotspots', []))}",
            "\n[CODE QUALITY]",
            f"- Magic numbers: {len(self.metrics['style'].get('magic_numbers', []))}",
            f"- Docstring coverage: {self.metrics['style'].get('docstring_coverage', 0)*100:.1f}%",
            "\n[POTENTIAL ISSUES]",
            *[f"- {issue}" for issue in self.metrics.get('potential_issues', [])],
            "\n[RECOMMENDATIONS]",
            "1. Refactor long methods (especially movement logic)",
            "2. Add input validation for position tracking",
            "3. Replace magic numbers with constants",
            "4. Add docstrings for all public methods"
        ]
        return '\n'.join(report)

if __name__ == "__main__":
    try:
        evaluator = OriginsEnvEvaluator()
        metrics = evaluator.evaluate()
        
        print(evaluator.generate_report())
        
        # Save detailed metrics
        with open(r"C:\Users\samik\OneDrive\Desktop\test\game_metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)
        print("\nDetailed metrics saved to game_metrics.json")
        
    except Exception as e:
        print(f"Evaluation failed: {str(e)}")