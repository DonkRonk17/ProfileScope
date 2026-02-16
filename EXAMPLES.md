# ProfileScope - Usage Examples

Complete guide with 10 real-world profiling scenarios.

Quick navigation:
- [Example 1: First-Time Profiling](#example-1-first-time-profiling)
- [Example 2: Finding Bottlenecks](#example-2-finding-bottlenecks)
- [Example 3: Profiling with Arguments](#example-3-profiling-with-arguments)
- [Example 4: Export to JSON](#example-4-export-to-json)
- [Example 5: Detecting Regressions](#example-5-detecting-regressions)
- [Example 6: Python API Usage](#example-6-python-api-usage)
- [Example 7: CI/CD Integration](#example-7-cicd-integration)
- [Example 8: Batch Profiling](#example-8-batch-profiling)
- [Example 9: Recursive Function Analysis](#example-9-recursive-function-analysis)
- [Example 10: Real Production Workflow](#example-10-real-production-workflow)

---

## Example 1: First-Time Profiling

**Scenario:** You're new to ProfileScope and want to profile a simple script.

**Script (test_basic.py):**
```python
def calculate_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total

result = calculate_sum(1000000)
print(f"Result: {result}")
```

**Command:**
```bash
profilescope run test_basic.py
```

**Expected Output:**
```
[ProfileScope] Profiling test_basic.py...

================================================================================
PROFILESCOPE PERFORMANCE REPORT
================================================================================
Script: test_basic.py
Total Time: 0.045s
Total Calls: 8
Timestamp: 2026-02-16 12:00:00
================================================================================

[HOT FUNCTIONS - Top 10 by Cumulative Time]
--------------------------------------------------------------------------------
Function                                Time (s)    Calls       %
--------------------------------------------------------------------------------
calculate_sum                           0.032       1           71.1
<module>                                0.045       1           100.0
print                                   0.001       1           2.2

[OPTIMIZATION RECOMMENDATIONS]
--------------------------------------------------------------------------------
1. Performance looks good! No major bottlenecks detected.

================================================================================

[OK] Profiling complete: 0.045s, 8 calls
```

**What You Learned:**
- Basic profiling syntax
- How to read terminal reports
- Identifying the slowest function (calculate_sum)

---

## Example 2: Finding Bottlenecks

**Scenario:** Your script is slow and you need to find why.

**Script (slow_app.py):**
```python
import time

def slow_database_query():
    time.sleep(2)  # Simulates slow DB
    return [{"id": i, "name": f"User{i}"} for i in range(100)]

def process_users(users):
    processed = []
    for user in users:
        # Inefficient processing
        processed.append({**user, "processed": True})
    return processed

def main():
    for i in range(5):  # Called 5 times!
        users = slow_database_query()  # BUG: Should cache this
        processed = process_users(users)
    print(f"Processed {len(processed)} users")

if __name__ == "__main__":
    main()
```

**Command:**
```bash
profilescope run slow_app.py
```

**Expected Output:**
```
[HOT FUNCTIONS - Top 10 by Cumulative Time]
--------------------------------------------------------------------------------
Function                                Time (s)    Calls       %
--------------------------------------------------------------------------------
slow_database_query                     10.012      5           99.1
main                                    10.100      1           100.0
process_users                           0.002       5           0.02

[BOTTLENECKS DETECTED]
--------------------------------------------------------------------------------
[!] slow_database_query (99.1% of total time)

[OPTIMIZATION RECOMMENDATIONS]
--------------------------------------------------------------------------------
1. Hot path detected in slow_database_query: 10.012s (99.1%)
2. Consider optimizing slow_database_query: called 5 times
```

**What You Learned:**
- Bottleneck detection identifies slow_database_query
- Function called 5 times unnecessarily (should cache)
- 99.1% of time spent in one function = easy optimization target

**Fix:**
```python
# Cache the query result
users = slow_database_query()  # Call ONCE
for i in range(5):
    processed = process_users(users)
# Result: 10s → 2s (5x speedup!)
```

---

## Example 3: Profiling with Arguments

**Scenario:** Your script takes command-line arguments. How do you profile it?

**Script (process_file.py):**
```python
import sys

def process(filename, mode):
    with open(filename) as f:
        data = f.read()
    print(f"Processed {filename} in {mode} mode: {len(data)} bytes")

if __name__ == "__main__":
    filename = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "default"
    process(filename, mode)
```

**Command:**
```bash
# Profile with arguments: data.txt and "fast" mode
profilescope run process_file.py data.txt fast
```

**Expected Output:**
```
[ProfileScope] Profiling process_file.py...
Processed data.txt in fast mode: 1024 bytes

================================================================================
PROFILESCOPE PERFORMANCE REPORT
================================================================================
Script: process_file.py
Total Time: 0.003s
Total Calls: 15
...
[OK] Profiling complete: 0.003s, 15 calls
```

**What You Learned:**
- Pass script arguments after the script name
- ProfileScope transparently forwards all arguments
- Works exactly like `python script.py arg1 arg2`

---

## Example 4: Export to JSON

**Scenario:** You want to save profiling data for later analysis or sharing.

**Command:**
```bash
profilescope run my_script.py --format json
```

**Expected Output:**
```
[ProfileScope] Profiling my_script.py...

[OK] Report saved: profilescope_reports/my_script_20260216_120000.json

[OK] Profiling complete: 0.123s, 456 calls
```

**JSON File Contents:**
```json
{
  "script_path": "my_script.py",
  "total_time": 0.123,
  "total_calls": 456,
  "hot_functions": [
    {
      "name": "slow_function",
      "filename": "my_script.py",
      "line_number": 10,
      "total_calls": 1,
      "primitive_calls": 1,
      "total_time": 0.100,
      "cumulative_time": 0.100,
      "time_per_call": 0.100,
      "cumulative_per_call": 0.100,
      "percentage": 81.3
    }
  ],
  "bottlenecks": ["slow_function (81.3% of total time)"],
  "call_tree": {"total_calls": 456, "primitive_calls": 450, "total_functions": 23},
  "recommendations": ["Hot path detected in slow_function: 0.100s (81.3%)"],
  "timestamp": "2026-02-16 12:00:00"
}
```

**What You Learned:**
- `--format json` saves structured data
- Perfect for programmatic analysis
- Includes all report data (functions, bottlenecks, recommendations)

---

## Example 5: Detecting Regressions

**Scenario:** You optimized code. Did it actually get faster? Or did you break something?

**Step 1: Profile baseline (before optimization)**
```bash
profilescope run app.py --format json
# Saved: profilescope_reports/app_20260216_100000.json
```

**Step 2: Make optimization changes**

**Step 3: Profile again (after optimization)**
```bash
profilescope run app.py --format json
# Saved: profilescope_reports/app_20260216_110000.json
```

**Step 4: Compare**
```bash
profilescope compare \
  profilescope_reports/app_20260216_100000.json \
  profilescope_reports/app_20260216_110000.json
```

**Output (Improvement):**
```
================================================================================
PROFILESCOPE COMPARISON REPORT
================================================================================
Baseline Time: 5.000s
Current Time:  2.500s
Change:        -50.0%

Baseline Calls: 10,000
Current Calls:  5,000
Change:         -50.0%

[OK] No significant performance regression
================================================================================
```

**Output (Regression - if you broke something):**
```
================================================================================
PROFILESCOPE COMPARISON REPORT
================================================================================
Baseline Time: 2.000s
Current Time:  5.000s
Change:        +150.0%

Baseline Calls: 5,000
Current Calls:  12,000
Change:         +140.0%

[!] New Bottlenecks:
  - new_slow_function (75.0% of total time)

[!] REGRESSION DETECTED
================================================================================
```

**What You Learned:**
- Compare runs to detect regressions
- Percentage changes show impact
- Exit code 1 if regression detected (for CI/CD)
- New bottlenecks automatically flagged

---

## Example 6: Python API Usage

**Scenario:** You want to profile from within Python code, not CLI.

**Script (auto_profiler.py):**
```python
from profilescope import ProfileScope
from pathlib import Path

# Initialize profiler
profiler = ProfileScope(output_dir=Path("./perf_reports"))

# Profile a script
script_to_profile = Path("my_algorithm.py")
report = profiler.profile(script_to_profile)

# Access report data programmatically
print(f"\\n[Performance Analysis]")
print(f"Total Time: {report.total_time:.3f}s")
print(f"Total Calls: {report.total_calls:,}")

# Show top 5 hot functions
print(f"\\n[Top 5 Hot Functions]")
for i, func in enumerate(report.hot_functions[:5], 1):
    print(f"{i}. {func.name}: {func.cumulative_time:.3f}s ({func.percentage:.1f}%)")

# Check for bottlenecks
if report.bottlenecks:
    print(f"\\n[BOTTLENECKS DETECTED]")
    for bottleneck in report.bottlenecks:
        print(f"[!] {bottleneck}")
else:
    print(f"\\n[OK] No bottlenecks detected")

# Show recommendations
print(f"\\n[Recommendations]")
for i, rec in enumerate(report.recommendations, 1):
    print(f"{i}. {rec}")

# Save in multiple formats
json_path = profiler.save_report(report, format="json")
md_path = profiler.save_report(report, format="markdown")

print(f"\\n[Reports Saved]")
print(f"- JSON: {json_path}")
print(f"- Markdown: {md_path}")
```

**Run:**
```bash
python auto_profiler.py
```

**What You Learned:**
- Import ProfileScope class
- Initialize with custom output directory
- Access all report data programmatically
- Save in multiple formats from Python

---

## Example 7: CI/CD Integration

**Scenario:** Automatically detect performance regressions in CI pipeline.

**GitHub Actions Workflow (.github/workflows/performance.yml):**
```yaml
name: Performance Testing

on: [push, pull_request]

jobs:
  performance-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install ProfileScope
        run: |
          git clone https://github.com/DonkRonk17/ProfileScope.git
          echo "$PWD/ProfileScope" >> $GITHUB_PATH
      
      - name: Profile baseline (main branch)
        run: |
          git checkout main
          profilescope run tests/performance_test.py --format json --output-dir baseline
      
      - name: Profile current (PR branch)
        run: |
          git checkout ${{ github.head_ref }}
          profilescope run tests/performance_test.py --format json --output-dir current
      
      - name: Compare and check for regression
        run: |
          profilescope compare baseline/*.json current/*.json
          # Exit code 1 if regression detected → fails CI
```

**What You Learned:**
- Integrate ProfileScope in CI/CD
- Automatically compare baseline vs current
- Fail builds on performance regressions
- Works on any CI platform (GitHub Actions, GitLab CI, Jenkins, etc.)

---

## Example 8: Batch Profiling

**Scenario:** Profile multiple scripts and compare performance.

**Script (batch_profiler.py):**
```python
from profilescope import ProfileScope
from pathlib import Path

profiler = ProfileScope()

scripts = [
    Path("algorithm_v1.py"),
    Path("algorithm_v2.py"),
    Path("algorithm_v3.py"),
]

print("Profiling multiple algorithms...")
results = []

for script in scripts:
    print(f"\\nProfiling {script.name}...")
    report = profiler.profile(script)
    results.append((script.name, report.total_time, report.total_calls))
    profiler.save_report(report, format="json")

# Compare results
print("\\n" + "=" * 60)
print("BATCH PROFILING RESULTS")
print("=" * 60)
print(f"{'Script':<20} {'Time (s)':<15} {'Calls':<15}")
print("-" * 60)

for name, time, calls in sorted(results, key=lambda x: x[1]):
    print(f"{name:<20} {time:<15.3f} {calls:<15,}")

fastest = min(results, key=lambda x: x[1])
print(f"\\n[OK] Fastest: {fastest[0]} ({fastest[1]:.3f}s)")
```

**What You Learned:**
- Profile multiple scripts programmatically
- Collect and compare results
- Identify fastest implementation
- Automate performance comparisons

---

## Example 9: Recursive Function Analysis

**Scenario:** You suspect recursive function is inefficient. How bad is it?

**Script (fibonacci.py):**
```python
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

result = fibonacci_recursive(30)
print(f"Fibonacci(30) = {result}")
```

**Command:**
```bash
profilescope run fibonacci.py
```

**Output:**
```
[HOT FUNCTIONS - Top 10 by Cumulative Time]
--------------------------------------------------------------------------------
Function                                Time (s)    Calls       %
--------------------------------------------------------------------------------
fibonacci_recursive                     0.823       2,692,537   98.5

[OPTIMIZATION RECOMMENDATIONS]
--------------------------------------------------------------------------------
1. Recursive function fibonacci_recursive: 2,692,537 calls (1 primitive)
2. Hot path detected in fibonacci_recursive: 0.823s (98.5%)
3. Consider optimizing fibonacci_recursive: called 2,692,537 times
```

**What You Learned:**
- Recursive functions show massive call counts
- 2.7M calls for fibonacci(30) = exponential complexity
- Recommendation clearly flags recursion issue

**Fix (use memoization):**
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_memo(n):
    if n <= 1:
        return n
    return fibonacci_memo(n-1) + fibonacci_memo(n-2)

# Result: 2.7M calls → 59 calls = 45,000x fewer calls!
```

---

## Example 10: Real Production Workflow

**Scenario:** End-to-end workflow for optimizing a production script.

**Phase 1: Baseline Profiling**
```bash
# Profile current production version
profilescope run production_app.py --format json --output-dir baseline
profilescope run production_app.py --format markdown --output-dir baseline
```

**Analysis:**
- Open Markdown report in browser
- Identify: `database_query()` takes 80% of time (called 1000 times in loop)

**Phase 2: Optimization**
```python
# BEFORE: Query in loop
for user_id in user_ids:  # 1000 iterations
    user = database_query(user_id)  # 1000 queries!
    process(user)

# AFTER: Batch query
users = database_batch_query(user_ids)  # 1 query!
for user in users:
    process(user)
```

**Phase 3: Validate Optimization**
```bash
# Profile optimized version
profilescope run production_app.py --format json --output-dir optimized

# Compare
profilescope compare baseline/production_app_*.json optimized/production_app_*.json
```

**Output:**
```
Baseline Time: 30.000s
Current Time:  2.500s
Change:        -91.7%

[OK] No significant performance regression
```

**Phase 4: Deploy with Confidence**
```bash
# Optimized version is 12x faster!
# Deploy to production
git commit -m "Optimize database queries - 12x speedup"
git push
```

**What You Learned:**
- Complete real-world optimization workflow
- Baseline → Analysis → Optimization → Validation
- Concrete performance improvements (12x)
- Data-driven optimization decisions

---

## Additional Resources

- **Main Documentation:** [README.md](README.md)
- **Quick Reference:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- **Integration Guides:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- **GitHub:** https://github.com/DonkRonk17/ProfileScope

---

**Last Updated:** February 16, 2026  
**Maintained By:** ATLAS (Team Brain)
