# ProfileScope - Integration Examples

Copy-paste-ready code examples for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [ProfileScope + AgentHealth](#pattern-1-profilescope--agenthealth)
2. [ProfileScope + SynapseLink](#pattern-2-profilescope--synapselink)
3. [ProfileScope + TaskQueuePro](#pattern-3-profilescope--taskqueuepro)
4. [ProfileScope + MemoryBridge](#pattern-4-profilescope--memorybridge)
5. [ProfileScope + SessionReplay](#pattern-5-profilescope--sessionreplay)
6. [ProfileScope + ConfigManager](#pattern-6-profilescope--configmanager)
7. [ProfileScope + ToolForge Build](#pattern-7-profilescope--toolforge-build)
8. [ProfileScope + CI/CD Pipeline](#pattern-8-profilescope--cicd-pipeline)
9. [ProfileScope + Batch Analysis](#pattern-9-profilescope--batch-analysis)
10. [ProfileScope + Full Team Brain Stack](#pattern-10-profilescope--full-team-brain-stack)

---

## Pattern 1: ProfileScope + AgentHealth

**Use Case:** Correlate performance metrics with agent health monitoring

**Why:** Understand if performance impacts agent health

**Code:**

```python
from agenthealth import AgentHealth
from profilescope import ProfileScope
from pathlib import Path

# Initialize
health = AgentHealth()
profiler = ProfileScope()

# Start session
session_id = "perf_test_001"
health.start_session("ATLAS", session_id=session_id)

try:
    # Profile script
    health.heartbeat("ATLAS", status="profiling")
    report = profiler.profile(Path("script.py"))
    
    # Log performance metrics
    health.log_metric("ATLAS", "execution_time", report.total_time)
    health.log_metric("ATLAS", "function_calls", report.total_calls)
    health.log_metric("ATLAS", "bottlenecks_found", len(report.bottlenecks))
    
    # Mark success
    health.heartbeat("ATLAS", status="completed")
    health.end_session("ATLAS", session_id=session_id, status="success")
    
except Exception as e:
    # Log error
    health.log_error("ATLAS", str(e))
    health.end_session("ATLAS", session_id=session_id, status="failed")
```

**Result:** Performance metrics correlated with agent health data

---

## Pattern 2: ProfileScope + SynapseLink

**Use Case:** Notify team of performance issues automatically

**Why:** Keep team informed without manual reporting

**Code:**

```python
from synapselink import quick_send
from profilescope import ProfileScope
from pathlib import Path

profiler = ProfileScope()

# Profile critical script
report = profiler.profile(Path("critical_task.py"))

# Check for performance issues
if report.bottlenecks:
    # Alert team
    quick_send(
        "FORGE,LOGAN",
        "[ProfileScope] Performance Issue Detected",
        f"Script: critical_task.py\\n"
        f"Total Time: {report.total_time:.3f}s\\n"
        f"Bottlenecks:\\n" +
        "\\n".join(f"  - {b}" for b in report.bottlenecks),
        priority="HIGH"
    )
elif report.total_time < 1.0:
    # Celebrate good performance
    quick_send(
        "TEAM",
        "[ProfileScope] Excellent Performance",
        f"Script: critical_task.py completed in {report.total_time:.3f}s",
        priority="NORMAL"
    )

# Compare with baseline
comparison = profiler.compare_reports(
    baseline_path=Path("baseline.json"),
    current_path=Path("current.json")
)

if comparison["regression_detected"]:
    quick_send(
        "FORGE,LOGAN",
        "[ProfileScope] Performance Regression Detected",
        f"Time change: {comparison['time_change_percent']:+.1f}%\\n"
        f"Baseline: {comparison['baseline_time']:.3f}s\\n"
        f"Current: {comparison['current_time']:.3f}s",
        priority="HIGH"
    )
```

**Result:** Team automatically notified of performance issues and regressions

---

## Pattern 3: ProfileScope + TaskQueuePro

**Use Case:** Track profiling tasks in centralized queue

**Why:** Manage profiling work alongside other agent tasks

**Code:**

```python
from taskqueuepro import TaskQueuePro
from profilescope import ProfileScope
from pathlib import Path

queue = TaskQueuePro()
profiler = ProfileScope()

# Create profiling task
task_id = queue.create_task(
    title="Profile data processing script",
    agent="ATLAS",
    priority=2,
    metadata={"script": "process_data.py", "type": "performance"}
)

# Start task
queue.start_task(task_id)

try:
    # Execute profiling
    report = profiler.profile(Path("process_data.py"))
    
    # Complete with results
    queue.complete_task(
        task_id,
        result={
            "status": "success",
            "total_time": report.total_time,
            "total_calls": report.total_calls,
            "bottlenecks": report.bottlenecks,
            "recommendations": report.recommendations
        }
    )
    
except Exception as e:
    # Fail task with error
    queue.fail_task(task_id, error=str(e))
```

**Result:** Profiling tasks tracked centrally with other work

---

## Pattern 4: ProfileScope + MemoryBridge

**Use Case:** Persist profiling history to memory core

**Why:** Track performance over time for trend analysis

**Code:**

```python
from memorybridge import MemoryBridge
from profilescope import ProfileScope
from pathlib import Path
import time

memory = MemoryBridge()
profiler = ProfileScope()

# Load historical data
history = memory.get("profilescope_history", default=[])

# Profile script
report = profiler.profile(Path("script.py"))

# Add to history
history.append({
    "script_path": report.script_path,
    "timestamp": report.timestamp,
    "total_time": report.total_time,
    "total_calls": report.total_calls,
    "bottlenecks": report.bottlenecks,
    "top_function": report.hot_functions[0].name if report.hot_functions else None
})

# Keep last 100 entries
if len(history) > 100:
    history = history[-100:]

# Save to memory core
memory.set("profilescope_history", history)
memory.sync()

# Analyze trends
if len(history) >= 2:
    current = history[-1]
    previous = history[-2]
    
    time_change = ((current["total_time"] - previous["total_time"]) / previous["total_time"]) * 100
    
    print(f"Performance trend: {time_change:+.1f}%")
```

**Result:** Long-term performance history persisted and analyzed

---

## Pattern 5: ProfileScope + SessionReplay

**Use Case:** Record profiling sessions for debugging

**Why:** Replay profiling attempts when investigating issues

**Code:**

```python
from sessionreplay import SessionReplay
from profilescope import ProfileScope
from pathlib import Path

replay = SessionReplay()
profiler = ProfileScope()

# Start recording session
session_id = replay.start_session("ATLAS", task="Profile slow script")

try:
    # Log inputs
    replay.log_input(session_id, "Profiling slow_script.py with test data")
    
    # Profile
    report = profiler.profile(Path("slow_script.py"), script_args=["--test-mode"])
    
    # Log results
    replay.log_output(
        session_id,
        f"Total time: {report.total_time:.3f}s\\n"
        f"Bottlenecks: {len(report.bottlenecks)}\\n"
        f"Top function: {report.hot_functions[0].name if report.hot_functions else 'N/A'}"
    )
    
    # Save report
    report_path = profiler.save_report(report, format="json")
    replay.log_output(session_id, f"Report saved: {report_path}")
    
    # Mark success
    replay.end_session(session_id, status="COMPLETED")
    
except Exception as e:
    # Log error
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
```

**Result:** Full session replay available for debugging profiling issues

---

## Pattern 6: ProfileScope + ConfigManager

**Use Case:** Centralize ProfileScope configuration

**Why:** Share profiling settings across tools and agents

**Code:**

```python
from configmanager import ConfigManager
from profilescope import ProfileScope
from pathlib import Path

config = ConfigManager()

# Load shared config
profilescope_config = config.get("profilescope", {
    "output_dir": "./profilescope_reports",
    "default_format": "json",
    "regression_threshold": 10.0
})

# Initialize with config
profiler = ProfileScope(output_dir=Path(profilescope_config["output_dir"]))

# Profile
report = profiler.profile(Path("script.py"))

# Save using configured format
report_path = profiler.save_report(report, format=profilescope_config["default_format"])

# Check regression threshold
comparison = profiler.compare_reports(Path("baseline.json"), Path("current.json"))

if comparison["time_change_percent"] > profilescope_config["regression_threshold"]:
    print(f"[!] Regression exceeds threshold: {comparison['time_change_percent']:.1f}%")
    
# Update config if needed
if report.total_time > 60.0:
    # Script is slow, increase threshold
    config.set("profilescope.regression_threshold", 20.0)
    config.save()
```

**Result:** Centralized configuration management for profiling

---

## Pattern 7: ProfileScope + ToolForge Build

**Use Case:** Integrate profiling into ToolForge build process

**Why:** Catch performance issues during development, not production

**Code:**

```python
# In ToolForge build script (Phase 2.5 - Performance Check)
from profilescope import ProfileScope
from pathlib import Path

profiler = ProfileScope(output_dir=Path("./build_reports"))

print("[ToolForge] Phase 2.5: Performance Check")

# Profile the tool
tool_path = Path("mytool.py")
report = profiler.profile(tool_path, script_args=["--test-mode"])

print(f"  Total Time: {report.total_time:.3f}s")
print(f"  Total Calls: {report.total_calls:,}")

# Check for hot paths (>20% of time)
hot_paths = [f for f in report.hot_functions if f.percentage > 20.0]

if hot_paths:
    print(f"  [!] Hot paths detected:")
    for func in hot_paths:
        print(f"    - {func.name}: {func.percentage:.1f}% of time")
    
    # Recommend optimization
    print(f"  [!] Consider optimizing before proceeding to tests")
else:
    print(f"  [OK] No significant hot paths detected")

# Save report
report_path = profiler.save_report(report, format="json")
print(f"  Report saved: {report_path}")

# Continue with Phase 3 (Tests)
print("[ToolForge] Proceeding to Phase 3: Testing")
```

**Result:** Performance checked as part of standard build process

---

## Pattern 8: ProfileScope + CI/CD Pipeline

**Use Case:** Automated performance testing in GitHub Actions

**Why:** Catch regressions before merge

**Code:**

**Python script (check_performance.py):**
```python
from profilescope import ProfileScope
from pathlib import Path
import sys

profiler = ProfileScope()

# Profile test suite
report = profiler.profile(Path("tests/performance_test.py"))

# Save report
report_path = profiler.save_report(report, format="json")
print(f"Report saved: {report_path}")

# Check against baseline
try:
    comparison = profiler.compare_reports(
        baseline_path=Path("baseline/performance_baseline.json"),
        current_path=report_path
    )
    
    print(f"Time change: {comparison['time_change_percent']:+.1f}%")
    
    if comparison["regression_detected"]:
        print("[!] REGRESSION DETECTED - Failing CI")
        sys.exit(1)
    else:
        print("[OK] No regression detected")
        sys.exit(0)
        
except FileNotFoundError:
    print("[!] No baseline found - saving current as baseline")
    import shutil
    shutil.copy(report_path, "baseline/performance_baseline.json")
    sys.exit(0)
```

**GitHub Actions Workflow (.github/workflows/performance.yml):**
```yaml
name: Performance Testing

on: [push, pull_request]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install ProfileScope
        run: |
          pip install -e git+https://github.com/DonkRonk17/ProfileScope.git#egg=profilescope
      
      - name: Run performance check
        run: python check_performance.py
```

**Result:** Automated performance regression detection in CI

---

## Pattern 9: ProfileScope + Batch Analysis

**Use Case:** Profile multiple scripts and compare

**Why:** Identify fastest implementation or detect anomalies

**Code:**

```python
from profilescope import ProfileScope
from pathlib import Path
import pandas as pd

profiler = ProfileScope()

# Scripts to profile
scripts = [
    Path("algorithm_v1.py"),
    Path("algorithm_v2.py"),
    Path("algorithm_v3.py"),
    Path("algorithm_v4.py"),
]

print("Batch profiling algorithms...")
results = []

for script in scripts:
    print(f"\\nProfiling {script.name}...")
    
    try:
        report = profiler.profile(script)
        
        results.append({
            "script": script.name,
            "total_time": report.total_time,
            "total_calls": report.total_calls,
            "bottlenecks": len(report.bottlenecks),
            "top_function": report.hot_functions[0].name if report.hot_functions else "N/A"
        })
        
        # Save report
        profiler.save_report(report, format="json")
        
    except Exception as e:
        print(f"[X] Error profiling {script.name}: {e}")
        results.append({
            "script": script.name,
            "total_time": None,
            "total_calls": None,
            "bottlenecks": None,
            "top_function": "ERROR"
        })

# Create DataFrame for analysis
df = pd.DataFrame(results)

# Sort by time
df_sorted = df.sort_values("total_time")

print("\\n" + "=" * 70)
print("BATCH PROFILING RESULTS")
print("=" * 70)
print(df_sorted.to_string(index=False))

# Identify fastest
fastest = df_sorted.iloc[0]
print(f"\\n[OK] Fastest: {fastest['script']} ({fastest['total_time']:.3f}s)")

# Identify slowest
slowest = df_sorted.iloc[-1]
print(f"[!] Slowest: {slowest['script']} ({slowest['total_time']:.3f}s)")

# Calculate speedup
if fastest['total_time'] and slowest['total_time']:
    speedup = slowest['total_time'] / fastest['total_time']
    print(f"\\nSpeedup: {speedup:.1f}x (fastest vs slowest)")
```

**Result:** Comprehensive batch analysis with performance rankings

---

## Pattern 10: ProfileScope + Full Team Brain Stack

**Use Case:** Complete integration with all Team Brain tools

**Why:** Production-grade profiling with full observability

**Code:**

```python
from profilescope import ProfileScope
from agenthealth import AgentHealth
from sessionreplay import SessionReplay
from taskqueuepro import TaskQueuePro
from synapselink import quick_send
from memorybridge import MemoryBridge
from pathlib import Path

# Initialize all tools
profiler = ProfileScope()
health = AgentHealth()
replay = SessionReplay()
queue = TaskQueuePro()
memory = MemoryBridge()

# Create task
task_id = queue.create_task("Profile production script", agent="ATLAS")
session_id = replay.start_session("ATLAS", task="Performance analysis")
health.start_session("ATLAS", session_id=session_id)

try:
    # Start work
    queue.start_task(task_id)
    replay.log_input(session_id, "Profiling production_script.py")
    health.heartbeat("ATLAS", status="profiling")
    
    # Profile
    report = profiler.profile(Path("production_script.py"))
    
    # Log metrics
    health.log_metric("ATLAS", "execution_time", report.total_time)
    replay.log_output(session_id, f"Profiled in {report.total_time:.3f}s")
    
    # Save to memory
    history = memory.get("profile_history", default=[])
    history.append({
        "timestamp": report.timestamp,
        "script": "production_script.py",
        "time": report.total_time,
        "calls": report.total_calls
    })
    memory.set("profile_history", history)
    memory.sync()
    
    # Complete task
    queue.complete_task(task_id, result=f"{report.total_time:.3f}s")
    replay.end_session(session_id, status="COMPLETED")
    health.end_session("ATLAS", session_id=session_id, status="success")
    
    # Notify team if issues found
    if report.bottlenecks:
        quick_send(
            "FORGE,LOGAN",
            "[ProfileScope] Bottlenecks Detected",
            f"Script: production_script.py\\n"
            f"Time: {report.total_time:.3f}s\\n"
            f"Issues:\\n" + "\\n".join(f"  - {b}" for b in report.bottlenecks),
            priority="NORMAL"
        )
    
except Exception as e:
    # Error handling across all tools
    queue.fail_task(task_id, error=str(e))
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    health.log_error("ATLAS", str(e))
    health.end_session("ATLAS", session_id=session_id, status="failed")
    
    # Alert team
    quick_send(
        "FORGE,LOGAN",
        "[ProfileScope] Profiling Failed",
        f"Error: {str(e)}",
        priority="HIGH"
    )
```

**Result:** Fully instrumented, observable profiling with Team Brain integration

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✓ AgentHealth - Health correlation
2. ✓ SynapseLink - Team notifications
3. ✓ SessionReplay - Debugging

**Week 2 (Productivity):**
4. ☐ TaskQueuePro - Task management
5. ☐ MemoryBridge - Historical tracking
6. ☐ ToolForge - Build integration

**Week 3 (Advanced):**
7. ☐ ConfigManager - Configuration
8. ☐ CI/CD - Automated testing
9. ☐ Full stack - Production integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure ProfileScope is in path
import sys
from pathlib import Path
sys.path.insert(0, str(Path("C:/Users/logan/OneDrive/Documents/AutoProjects/ProfileScope")))

from profilescope import ProfileScope
```

**Version Conflicts:**
```bash
# Check versions
python -c "from profilescope import __version__; print(__version__)"

# Update if needed
cd C:\\Users\\logan\\OneDrive\\Documents\\AutoProjects\\ProfileScope
git pull origin master
```

---

**Last Updated:** February 16, 2026  
**Maintained By:** ATLAS (Team Brain)
