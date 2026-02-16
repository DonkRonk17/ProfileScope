# ProfileScope - Integration Plan

Complete integration architecture for Team Brain agents and BCH.

---

## 🎯 INTEGRATION GOALS

ProfileScope integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools (AgentHealth, SynapseLink, TaskQueuePro, etc.)
3. BCH (Beacon Command Hub) - potential future integration
4. Logan's development workflows

---

## 📦 BCH INTEGRATION (Future)

**Status:** Not currently integrated with BCH

**Potential BCH Commands:**
```
@profilescope run <script>
@profilescope compare <baseline> <current>
@profilescope report <session_id>
```

**Implementation Plan:**
1. Add ProfileScope to BCH imports
2. Create command handlers for profiling requests
3. Store reports in BCH database
4. Enable notification on performance regressions

**Priority:** Low (standalone tool sufficient for now)

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Review code performance before approval | Python API | HIGH |
| **Atlas** | Profile tools during development | CLI + Python API | HIGH |
| **Clio** | Profile Linux services and scripts | CLI | MEDIUM |
| **Nexus** | Cross-platform performance testing | CLI | MEDIUM |
| **Bolt** | Zero-cost automated profiling | CLI | LOW |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Review code performance metrics before approving builds

**Integration Steps:**
1. Add ProfileScope to tool review checklist
2. Profile critical tools before GitHub upload
3. Compare with previous versions for regressions
4. Block uploads with >10% performance degradation

**Example Workflow:**
```python
from profilescope import ProfileScope
from pathlib import Path

# During tool review
profiler = ProfileScope(output_dir=Path("./reviews/performance"))

# Profile the new tool
report = profiler.profile(Path("newtool.py"))

# Check for bottlenecks
if report.bottlenecks:
    print("[!] Performance issues detected before upload:")
    for bottleneck in report.bottlenecks:
        print(f"  - {bottleneck}")
    # Request optimization before approval

# Save report for documentation
profiler.save_report(report, format="markdown")
```

#### Atlas (Executor / Builder)

**Primary Use Case:** Profile tools during development to catch performance issues early

**Integration Steps:**
1. Add to ToolForge build checklist (new Phase 2.5)
2. Profile all tools after core development
3. Optimize bottlenecks before tests
4. Document performance in session logs

**Example Workflow:**
```python
# In ToolForge build process
from profilescope import ProfileScope

# After core development (Phase 2)
profiler = ProfileScope()

# Profile the tool
report = profiler.profile(Path("mytool.py"), script_args=["--test-mode"])

# Optimization check
if any(func.percentage > 50.0 for func in report.hot_functions[:3]):
    print("[!] Hot path detected - consider optimization")
    
# Save for build documentation
profiler.save_report(report, format="json")
```

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Profile Linux services and background scripts

**Platform Considerations:**
- ProfileScope works identically on Linux
- Use with systemd services for monitoring
- Profile cron jobs for optimization

**Example:**
```bash
# Profile a service script
profilescope run /usr/local/bin/service_script.py

# Profile cron job
profilescope run /home/user/cron_tasks/backup.py --format json
```

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Verify cross-platform performance consistency

**Cross-Platform Notes:**
- ProfileScope uses pathlib (works on all platforms)
- Pure stdlib = no platform-specific dependencies
- Use to detect platform-specific performance issues

**Example:**
```python
# Cross-platform profiling
import platform
from profilescope import ProfileScope

profiler = ProfileScope()
report = profiler.profile(Path("cross_platform_tool.py"))

# Log platform-specific results
print(f"Platform: {platform.system()}")
print(f"Performance: {report.total_time:.3f}s")
```

#### Bolt (Cline / Free Executor)

**Primary Use Case:** Automated profiling without API costs

**Cost Considerations:**
- ProfileScope has zero runtime costs (no APIs)
- Perfect for Bolt's free-tier operation
- Can profile repeatedly without budget impact

**Example:**
```bash
# Bolt can run unlimited profiling
for script in scripts/*.py; do
    profilescope run "$script" --format json
done
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With AgentHealth

**Correlation Use Case:** Track performance metrics alongside agent health

**Integration Pattern:**
```python
from agenthealth import AgentHealth
from profilescope import ProfileScope

health = AgentHealth()
profiler = ProfileScope()

session_id = "tool_build_001"
health.start_session("ATLAS", session_id=session_id)

report = profiler.profile(Path("tool.py"))

# Log performance metrics
health.log_metric("ATLAS", "execution_time", report.total_time)
health.log_metric("ATLAS", "function_calls", report.total_calls)

health.end_session("ATLAS", session_id=session_id)
```

### With SynapseLink

**Notification Use Case:** Alert team of performance regressions

**Integration Pattern:**
```python
from synapselink import quick_send
from profilescope import ProfileScope

profiler = ProfileScope()

# Profile baseline vs current
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

### With TaskQueuePro

**Task Management Use Case:** Track profiling tasks in queue

**Integration Pattern:**
```python
from taskqueuepro import TaskQueuePro
from profilescope import ProfileScope

queue = TaskQueuePro()
profiler = ProfileScope()

task_id = queue.create_task(
    title="Profile performance of new feature",
    agent="ATLAS",
    priority=2
)

queue.start_task(task_id)

try:
    report = profiler.profile(Path("new_feature.py"))
    
    queue.complete_task(
        task_id,
        result=f"Profiled: {report.total_time:.3f}s, {report.total_calls:,} calls"
    )
except Exception as e:
    queue.fail_task(task_id, error=str(e))
```

### With MemoryBridge

**Context Persistence Use Case:** Store profiling history in memory core

**Integration Pattern:**
```python
from memorybridge import MemoryBridge
from profilescope import ProfileScope

memory = MemoryBridge()
profiler = ProfileScope()

# Load historical data
history = memory.get("profilescope_history", default=[])

# Profile and add to history
report = profiler.profile(Path("script.py"))
history.append({
    "script": "script.py",
    "timestamp": report.timestamp,
    "total_time": report.total_time,
    "total_calls": report.total_calls,
    "bottlenecks": report.bottlenecks
})

# Save updated history
memory.set("profilescope_history", history)
memory.sync()
```

### With SessionReplay

**Debugging Use Case:** Record profiling sessions for replay

**Integration Pattern:**
```python
from sessionreplay import SessionReplay
from profilescope import ProfileScope

replay = SessionReplay()
profiler = ProfileScope()

session_id = replay.start_session("ATLAS", task="Performance profiling")

try:
    replay.log_input(session_id, "Profiling script.py")
    
    report = profiler.profile(Path("script.py"))
    
    replay.log_output(
        session_id,
        f"Total time: {report.total_time:.3f}s, Bottlenecks: {len(report.bottlenecks)}"
    )
    
    replay.end_session(session_id, status="COMPLETED")
    
except Exception as e:
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features

**Steps:**
1. ✓ Tool deployed to GitHub
2. ☐ Quick-start guides sent via Synapse
3. ☐ Each agent tests basic workflow
4. ☐ Feedback collected

**Success Criteria:**
- All 5 agents have used ProfileScope at least once
- No blocking issues reported

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows

**Steps:**
1. ☐ Add to ToolForge build checklist (Atlas)
2. ☐ Add to tool review process (Forge)
3. ☐ Create integration examples with existing tools
4. ☐ Monitor usage patterns

**Success Criteria:**
- Used in at least 3 tool builds
- Integration examples tested

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
1. ☐ Collect efficiency metrics
2. ☐ Implement v1.1 improvements
3. ☐ Create advanced workflow examples
4. ☐ Full Team Brain ecosystem integration

**Success Criteria:**
- Measurable performance improvement in tools
- Positive feedback from all agents
- v1.1 feature requests identified

---

## 📊 SUCCESS METRICS

**Adoption Metrics:**
- Number of agents using tool: 0/5 (target: 5/5)
- Daily usage count: 0 (target: 5+ profiles/day)
- Integration with other tools: 0 (target: 5+ integrations)

**Efficiency Metrics:**
- Time saved per use: 25-55 minutes (estimated)
- Performance issues caught pre-production: 0 (target: 80%+)
- Tools optimized: 0 (target: 10+ in first month)

**Quality Metrics:**
- Bug reports: 0
- Feature requests: 0
- User satisfaction: TBD (collect feedback)

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import
from profilescope import ProfileScope

# Specific imports
from profilescope import ProfileScope, ProfileReport, FunctionStats
```

### Configuration Integration

**Config File:** ProfileScope uses output directories, no central config needed

**Shared Config Pattern:**
```python
# If using with ConfigManager
from configmanager import ConfigManager
from profilescope import ProfileScope

config = ConfigManager()
output_dir = config.get("profilescope.output_dir", "./profilescope_reports")

profiler = ProfileScope(output_dir=Path(output_dir))
```

### Error Handling Integration

**Standardized Error Codes:**
- 0: Success (profile completed)
- 1: Error (script failed, comparison shows regression, etc.)

### Logging Integration

**Log Format:** ProfileScope outputs to stdout (terminal reports)

**Integration with logging module:**
```python
import logging
from profilescope import ProfileScope

logger = logging.getLogger("ProfileScope")

profiler = ProfileScope()
report = profiler.profile(Path("script.py"))

logger.info(f"Profiled {report.script_path}: {report.total_time:.3f}s")
```

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy

- Minor updates (v1.x): As needed
- Major updates (v2.0+): When significant features added
- Security patches: Immediate (none expected for stdlib tool)

### Support Channels

- GitHub Issues: Bug reports and feature requests
- Synapse: Team Brain discussions
- Direct to Builder (ATLAS): Complex issues

### Known Limitations

- Profiling adds 5-10% overhead (cProfile limitation)
- Very fast functions (<0.001s) may not appear in reports
- Requires Python 3.7+ (dataclasses)

---

## 📚 ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- GitHub: https://github.com/DonkRonk17/ProfileScope

---

**Last Updated:** February 16, 2026  
**Maintained By:** ATLAS (Team Brain)
