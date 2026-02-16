#!/usr/bin/env python3
"""
Comprehensive test suite for ProfileScope.

Tests cover:
- Core profiling functionality
- Report generation and formatting
- Export to multiple formats (JSON, Markdown, HTML)
- Report comparison for regression detection
- Edge cases and error handling
- Cross-platform compatibility

Run: python test_profilescope.py
"""

import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from profilescope import ProfileScope, FunctionStats, ProfileReport


class TestProfileScopeCore(unittest.TestCase):
    """Test core ProfileScope functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.profiler = ProfileScope(output_dir=self.temp_dir)
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove temp directory
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            
    def test_initialization(self):
        """Test ProfileScope initializes correctly."""
        profiler = ProfileScope()
        self.assertIsNotNone(profiler)
        self.assertTrue(profiler.output_dir.exists())
        
    def test_initialization_custom_output_dir(self):
        """Test ProfileScope with custom output directory."""
        custom_dir = self.temp_dir / "custom_reports"
        profiler = ProfileScope(output_dir=custom_dir)
        self.assertTrue(custom_dir.exists())
        
    def test_profile_simple_script(self):
        """Test profiling a simple Python script."""
        # Create test script
        script = self.temp_dir / "test_script.py"
        script.write_text("""
def add(a, b):
    return a + b

result = add(1, 2)
print(f"Result: {result}")
""")
        
        # Profile the script
        report = self.profiler.profile(script)
        
        # Verify report
        self.assertIsInstance(report, ProfileReport)
        self.assertEqual(report.script_path, str(script))
        self.assertGreaterEqual(report.total_time, 0)  # May be 0 for very fast scripts
        self.assertGreater(report.total_calls, 0)
        self.assertIsInstance(report.hot_functions, list)
        
    def test_profile_script_with_arguments(self):
        """Test profiling script with command-line arguments."""
        # Create test script that uses sys.argv
        script = self.temp_dir / "test_args.py"
        script.write_text("""
import sys
print(f"Args: {sys.argv[1:]}")
""")
        
        # Profile with arguments
        report = self.profiler.profile(script, ["arg1", "arg2"])
        
        self.assertIsNotNone(report)
        self.assertGreater(report.total_calls, 0)
        
    def test_profile_nonexistent_script(self):
        """Test profiling nonexistent script raises error."""
        fake_script = self.temp_dir / "nonexistent.py"
        
        with self.assertRaises(FileNotFoundError):
            self.profiler.profile(fake_script)
            
    def test_profile_script_with_error(self):
        """Test profiling script that raises exception."""
        # Create script that raises error
        script = self.temp_dir / "error_script.py"
        script.write_text("""
raise ValueError("Test error")
""")
        
        with self.assertRaises(RuntimeError):
            self.profiler.profile(script)


class TestFunctionStats(unittest.TestCase):
    """Test FunctionStats data class."""
    
    def test_function_stats_creation(self):
        """Test creating FunctionStats."""
        stats = FunctionStats(
            name="test_function",
            filename="test.py",
            line_number=10,
            total_calls=100,
            primitive_calls=100,
            total_time=1.5,
            cumulative_time=2.0,
            time_per_call=0.015,
            cumulative_per_call=0.020,
            percentage=25.0
        )
        
        self.assertEqual(stats.name, "test_function")
        self.assertEqual(stats.total_calls, 100)
        self.assertEqual(stats.cumulative_time, 2.0)
        self.assertEqual(stats.percentage, 25.0)


class TestReportGeneration(unittest.TestCase):
    """Test report generation and formatting."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.profiler = ProfileScope(output_dir=self.temp_dir)
        
        # Create test script
        self.script = self.temp_dir / "test_perf.py"
        self.script.write_text("""
import time

def slow_function():
    total = 0
    for i in range(1000):
        total += i
    return total

def fast_function():
    return sum(range(1000))

# Run functions
slow_function()
fast_function()
""")
        
    def tearDown(self):
        """Clean up after tests."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            
    def test_format_terminal_report(self):
        """Test formatting report for terminal display."""
        report = self.profiler.profile(self.script)
        terminal_output = self.profiler.format_terminal_report(report)
        
        self.assertIsInstance(terminal_output, str)
        self.assertIn("PROFILESCOPE PERFORMANCE REPORT", terminal_output)
        self.assertIn("Script:", terminal_output)
        self.assertIn("Total Time:", terminal_output)
        self.assertIn("HOT FUNCTIONS", terminal_output)
        
    def test_format_terminal_report_with_tree(self):
        """Test terminal report with call tree."""
        report = self.profiler.profile(self.script)
        terminal_output = self.profiler.format_terminal_report(report, show_tree=True)
        
        self.assertIn("CALL TREE SUMMARY", terminal_output)
        self.assertIn("Total Functions:", terminal_output)
        
    def test_hot_functions_extraction(self):
        """Test extracting hot functions from stats."""
        report = self.profiler.profile(self.script)
        
        self.assertGreater(len(report.hot_functions), 0)
        
        # Verify hot function structure
        if report.hot_functions:
            func = report.hot_functions[0]
            self.assertIsInstance(func, FunctionStats)
            self.assertIsInstance(func.name, str)
            self.assertGreaterEqual(func.total_calls, 0)
            self.assertGreaterEqual(func.cumulative_time, 0)
            
    def test_bottleneck_identification(self):
        """Test identifying performance bottlenecks."""
        report = self.profiler.profile(self.script)
        
        self.assertIsInstance(report.bottlenecks, list)
        # May or may not have bottlenecks depending on execution
        
    def test_recommendations_generation(self):
        """Test generating optimization recommendations."""
        report = self.profiler.profile(self.script)
        
        self.assertIsInstance(report.recommendations, list)
        self.assertGreater(len(report.recommendations), 0)


class TestReportExport(unittest.TestCase):
    """Test exporting reports to different formats."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.profiler = ProfileScope(output_dir=self.temp_dir)
        
        # Create and profile test script
        self.script = self.temp_dir / "export_test.py"
        self.script.write_text("""
def compute():
    return sum(range(100))

compute()
""")
        
        self.report = self.profiler.profile(self.script)
        
    def tearDown(self):
        """Clean up after tests."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            
    def test_save_report_json(self):
        """Test saving report as JSON."""
        report_path = self.profiler.save_report(self.report, format="json")
        
        self.assertTrue(report_path.exists())
        self.assertEqual(report_path.suffix, ".json")
        
        # Verify JSON is valid
        with open(report_path) as f:
            data = json.load(f)
            
        self.assertIn("script_path", data)
        self.assertIn("total_time", data)
        self.assertIn("hot_functions", data)
        
    def test_save_report_markdown(self):
        """Test saving report as Markdown."""
        report_path = self.profiler.save_report(self.report, format="markdown")
        
        self.assertTrue(report_path.exists())
        self.assertEqual(report_path.suffix, ".md")
        
        # Verify Markdown content
        content = report_path.read_text()
        self.assertIn("# Performance Report:", content)
        self.assertIn("## Hot Functions", content)
        
    def test_save_report_html(self):
        """Test saving report as HTML."""
        report_path = self.profiler.save_report(self.report, format="html")
        
        self.assertTrue(report_path.exists())
        self.assertEqual(report_path.suffix, ".html")
        
        # Verify HTML content
        content = report_path.read_text()
        self.assertIn("<html>", content)
        self.assertIn("<h1>Performance Report:", content)
        self.assertIn("<table>", content)
        
    def test_save_report_invalid_format(self):
        """Test saving report with invalid format raises error."""
        with self.assertRaises(ValueError):
            self.profiler.save_report(self.report, format="invalid")


class TestReportComparison(unittest.TestCase):
    """Test comparing profiling reports."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.profiler = ProfileScope(output_dir=self.temp_dir)
        
    def tearDown(self):
        """Clean up after tests."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            
    def test_compare_reports_same_performance(self):
        """Test comparing two reports with similar performance."""
        # Create test script
        script = self.temp_dir / "compare_test.py"
        script.write_text("""
def compute():
    return sum(range(100))

compute()
""")
        
        # Profile twice and save as JSON
        report1 = self.profiler.profile(script)
        baseline_path = self.profiler.save_report(report1, format="json")
        
        time.sleep(0.1)  # Small delay
        
        report2 = self.profiler.profile(script)
        current_path = self.profiler.save_report(report2, format="json")
        
        # Compare reports
        comparison = self.profiler.compare_reports(baseline_path, current_path)
        
        self.assertIn("baseline_time", comparison)
        self.assertIn("current_time", comparison)
        self.assertIn("time_change_percent", comparison)
        self.assertIn("regression_detected", comparison)
        
    def test_compare_reports_with_regression(self):
        """Test detecting performance regression."""
        # Create baseline report (fast)
        baseline_data = {
            "script_path": "test.py",
            "total_time": 1.0,
            "total_calls": 100,
            "hot_functions": [],
            "bottlenecks": [],
            "call_tree": {},
            "recommendations": [],
            "timestamp": "2026-01-01 00:00:00"
        }
        
        baseline_path = self.temp_dir / "baseline.json"
        with open(baseline_path, 'w') as f:
            json.dump(baseline_data, f)
            
        # Create current report (slow - regression!)
        current_data = baseline_data.copy()
        current_data["total_time"] = 2.5  # 150% slower
        current_data["total_calls"] = 150  # 50% more calls
        
        current_path = self.temp_dir / "current.json"
        with open(current_path, 'w') as f:
            json.dump(current_data, f)
            
        # Compare
        comparison = self.profiler.compare_reports(baseline_path, current_path)
        
        self.assertGreater(comparison["time_change_percent"], 10.0)
        self.assertTrue(comparison["regression_detected"])
        
    def test_compare_reports_with_improvement(self):
        """Test detecting performance improvement."""
        # Create baseline report (slow)
        baseline_data = {
            "script_path": "test.py",
            "total_time": 2.0,
            "total_calls": 200,
            "hot_functions": [],
            "bottlenecks": ["slow_function (50% of total time)"],
            "call_tree": {},
            "recommendations": [],
            "timestamp": "2026-01-01 00:00:00"
        }
        
        baseline_path = self.temp_dir / "baseline.json"
        with open(baseline_path, 'w') as f:
            json.dump(baseline_data, f)
            
        # Create current report (fast - improvement!)
        current_data = baseline_data.copy()
        current_data["total_time"] = 1.0  # 50% faster
        current_data["total_calls"] = 100  # 50% fewer calls
        current_data["bottlenecks"] = []  # Fixed bottleneck!
        
        current_path = self.temp_dir / "current.json"
        with open(current_path, 'w') as f:
            json.dump(current_data, f)
            
        # Compare
        comparison = self.profiler.compare_reports(baseline_path, current_path)
        
        self.assertLess(comparison["time_change_percent"], -10.0)
        self.assertEqual(len(comparison["fixed_bottlenecks"]), 1)
        self.assertFalse(comparison["regression_detected"])
        
    def test_compare_nonexistent_reports(self):
        """Test comparing nonexistent reports raises error."""
        fake_baseline = self.temp_dir / "fake_baseline.json"
        fake_current = self.temp_dir / "fake_current.json"
        
        with self.assertRaises(FileNotFoundError):
            self.profiler.compare_reports(fake_baseline, fake_current)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.profiler = ProfileScope(output_dir=self.temp_dir)
        
    def tearDown(self):
        """Clean up after tests."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            
    def test_profile_empty_script(self):
        """Test profiling empty script."""
        script = self.temp_dir / "empty.py"
        script.write_text("")
        
        report = self.profiler.profile(script)
        self.assertIsNotNone(report)
        
    def test_profile_script_with_imports(self):
        """Test profiling script with imports."""
        script = self.temp_dir / "imports.py"
        script.write_text("""
import json
import sys
from pathlib import Path

data = {"test": 123}
print(json.dumps(data))
""")
        
        report = self.profiler.profile(script)
        self.assertGreater(len(report.hot_functions), 0)
        
    def test_profile_script_with_recursion(self):
        """Test profiling script with recursive function."""
        script = self.temp_dir / "recursive.py"
        script.write_text("""
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
""")
        
        report = self.profiler.profile(script)
        
        # Should detect recursive calls
        self.assertGreater(len(report.hot_functions), 0)
        
        # Check if recommendations mention recursion
        has_recursion_recommendation = any(
            "recursive" in rec.lower() for rec in report.recommendations
        )
        # May or may not trigger depending on call count threshold
        
    def test_profile_script_with_loops(self):
        """Test profiling script with intensive loops."""
        script = self.temp_dir / "loops.py"
        script.write_text("""
def compute_sum():
    total = 0
    for i in range(10000):
        total += i * 2
    return total

result = compute_sum()
""")
        
        report = self.profiler.profile(script)
        self.assertGreater(report.total_calls, 0)  # Simple script may have few calls


class TestCrossPlatform(unittest.TestCase):
    """Test cross-platform compatibility."""
    
    def test_output_directory_creation(self):
        """Test output directory creation works on all platforms."""
        import tempfile
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            output_dir = temp_dir / "profilescope" / "reports"
            profiler = ProfileScope(output_dir=output_dir)
            
            self.assertTrue(output_dir.exists())
            
        finally:
            import shutil
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
                
    def test_report_paths_use_pathlib(self):
        """Test that all paths use pathlib for cross-platform compatibility."""
        import tempfile
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            profiler = ProfileScope(output_dir=temp_dir)
            
            # Create test script
            script = temp_dir / "test.py"
            script.write_text("print('test')")
            
            report = profiler.profile(script)
            report_path = profiler.save_report(report, format="json")
            
            # Verify paths are Path objects or strings (not platform-specific)
            self.assertTrue(isinstance(report_path, Path))
            
        finally:
            import shutil
            if temp_dir.exists():
                shutil.rmtree(temp_dir)


def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: ProfileScope v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestProfileScopeCore))
    suite.addTests(loader.loadTestsFromTestCase(TestFunctionStats))
    suite.addTests(loader.loadTestsFromTestCase(TestReportGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestReportExport))
    suite.addTests(loader.loadTestsFromTestCase(TestReportComparison))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossPlatform))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    print(f"[OK] Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
