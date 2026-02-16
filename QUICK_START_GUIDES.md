# ProfileScope - Quick Start Guides

5-minute guides for each Team Brain agent plus Logan.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)
- [Logan (Developer)](#logan-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Review tool performance before approving builds

### Step 1: Installation Check

```bash
# Verify ProfileScope available
python C:\Users\logan\OneDrive\Documents\AutoProjects\ProfileScope\profilescope.py --version
# Expected: profilescope.py 1.0.0
```

### Step 2: First Use - Performance Review

```python
# During tool review session
from profilescope import ProfileScope
from pathlib import Path

profiler = ProfileScope(output_dir=Path("./tool_reviews/performance"))

# Profile the tool under review
tool_path = Path("C:/Users/logan/OneDrive/Documents/AutoProjects/NewTool/newtool.py")
report = profiler.profile(tool_path)

# Review metrics
print(f"Performance Review:")
print(f"Total Time: {report.total_time:.3f}s")
print(f"Bottlenecks: {len(report.bottlenecks)}")

# Check for issues
if report.bottlenecks:
    print("[!] Performance issues detected:")
    for bottleneck in report.bottlenecks:
        print(f"  - {bottleneck}")
```

### Step 3: Compare with Previous Version

```python
# Compare baseline vs current
comparison = profiler.compare_reports(
    baseline_path=Path("baseline/newtool_baseline.json"),
    current_path=Path("current/newtool_current.json")
)

if comparison["regression_detected"]:
    print(f"[!] REGRESSION: {comparison['time_change_percent']:+.1f}%")
    # Request optimization before approval
```

### Next Steps for Forge

1. Add ProfileScope to tool review checklist
2. Profile all tools before GitHub upload approval
3. Set performance regression threshold (10% default)
4. Create performance reports for documentation

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Profile tools during development to catch issues early

### Step 1: Installation Check

```bash
# ProfileScope is in AutoProjects
cd C:\Users\logan\OneDrive\Documents\AutoProjects\ProfileScope
python profilescope.py --version
```

### Step 2: First Use - Profile During Development

```bash
# After building core tool (ToolForge Phase 2)
cd C:\Users\logan\OneDrive\Documents\AutoProjects\MyNewTool

# Profile the tool
python C:\Users\logan\OneDrive\Documents\AutoProjects\ProfileScope\profilescope.py run mynew tool.py

# Get instant performance report
```

### Step 3: Integration with ToolForge Workflow

```python
# Add to build process (Phase 2.5 - Performance Check)
from profilescope import ProfileScope
from pathlib import Path

profiler = ProfileScope()

# Profile tool
report = profiler.profile(Path("mytool.py"), script_args=["--test-data"])

# Check for hot paths
hot_funcs = [f for f in report.hot_functions if f.percentage > 20.0]

if hot_funcs:
    print(f"[!] Hot paths detected - consider optimization:")
    for func in hot_funcs:
        print(f"  - {func.name}: {func.percentage:.1f}% of time")

# Save for documentation
profiler.save_report(report, format="json")
```

### Next Steps for Atlas

1. Add ProfileScope to ToolForge build checklist (new Phase 2.5)
2. Profile all tools after core development
3. Optimize bottlenecks before writing tests
4. Document performance in session logs

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Profile Linux services and scripts

### Step 1: Linux Installation

```bash
# Clone ProfileScope
git clone https://github.com/DonkRonk17/ProfileScope.git
cd ProfileScope

# Verify
python3 profilescope.py --version
```

### Step 2: First Use - Profile Service Script

```bash
# Profile a service script
python3 profilescope.py run /usr/local/bin/my_service.py

# Save as JSON for analysis
python3 profilescope.py run /usr/local/bin/my_service.py --format json
```

### Step 3: Integrate with System Services

```bash
# Profile systemd service startup script
sudo profilescope run /usr/lib/systemd/system-scripts/myservice.sh

# Profile cron job
profilescope run ~/cron_tasks/backup_script.py --format markdown
```

### Next Steps for Clio

1. Add to ABIOS system monitoring
2. Profile all cron jobs for optimization
3. Monitor service startup performance
4. Create performance baselines for critical services

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Verify cross-platform performance consistency

### Step 1: Platform Detection

```python
import platform
from profilescope import ProfileScope
from pathlib import Path

profiler = ProfileScope()

print(f"Platform: {platform.system()}")
print(f"Python: {platform.python_version()}")
```

### Step 2: Cross-Platform Profiling

```python
# Profile same tool on different platforms
report = profiler.profile(Path("cross_platform_tool.py"))

# Log platform-specific results
platform_name = platform.system()
print(f"{platform_name} Performance: {report.total_time:.3f}s")

# Save with platform identifier
profiler.save_report(report, format="json")
# Rename to include platform
```

### Step 3: Compare Platform Performance

```bash
# On Windows
profilescope run tool.py --format json --output-dir results/windows

# On Linux
profilescope run tool.py --format json --output-dir results/linux

# On macOS
profilescope run tool.py --format json --output-dir results/macos

# Compare
profilescope compare results/windows/tool_*.json results/linux/tool_*.json
```

### Next Steps for Nexus

1. Create platform-specific performance baselines
2. Test all tools on Windows, Linux, macOS
3. Report platform-specific performance issues
4. Document platform differences

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Automated profiling without API costs

### Step 1: Verify Zero Cost

```bash
# ProfileScope has ZERO runtime costs!
# No API calls, no external services
profilescope --version
```

### Step 2: Batch Profiling (Cost-Free)

```bash
# Profile multiple scripts without budget impact
for script in scripts/*.py; do
    profilescope run "$script" --format json --output-dir ./perf_reports
done

echo "All scripts profiled - zero API costs!"
```

### Step 3: Automated Performance Testing

```bash
# In Cline workflow
profilescope run test_suite.py --format json

# Compare with baseline (automated regression detection)
profilescope compare baseline.json current.json
# Exit code 1 if regression → fail automation
```

### Next Steps for Bolt

1. Add to automated testing workflows
2. Profile all scripts before deployment
3. Use for cost-free performance monitoring
4. Report regressions via Synapse

---

## 👨‍💻 LOGAN QUICK START

**Role:** Developer / Project Owner  
**Time:** 5 minutes  
**Goal:** Quick performance analysis for any Python script

### Step 1: Quick Profile

```bash
# Navigate to ProfileScope
cd C:\Users\logan\OneDrive\Documents\AutoProjects\ProfileScope

# Profile any script
python profilescope.py run C:\path\to\my_script.py
```

### Step 2: Save for Later

```bash
# Save as Markdown (easy to read in browser)
python profilescope.py run my_script.py --format markdown --output-dir ~/perf_reports

# Open in browser
start ~/perf_reports/my_script_*.md
```

### Step 3: Compare Versions

```bash
# Before optimization
python profilescope.py run slow_script.py --format json
# Save as: baseline.json

# After optimization
python profilescope.py run slow_script.py --format json
# Save as: optimized.json

# Compare
python profilescope.py compare baseline.json optimized.json
```

### Common Logan Workflows

**Morning Tool Check:**
```bash
# Quick profile of critical tools
profilescope run D:\BEACON_HQ\critical_tool.py
```

**Pre-Commit Check:**
```bash
# Profile before committing
profilescope run my_changes.py --format json
# Review report → optimize if needed → commit
```

**Performance Investigation:**
```bash
# "Why is this slow?"
profilescope run slow_thing.py --tree
# Instant answer: bottleneck identified
```

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/ProfileScope/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message ATLAS

---

**Last Updated:** February 16, 2026  
**Maintained By:** ATLAS (Team Brain)
