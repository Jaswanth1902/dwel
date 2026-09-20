# DWEL (Directed Walk & Execution-Loop Interceptor)

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/dwel/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

**DWEL** is a zero-dependency, ultra-low-latency (< 0.5ms) cycle detection and trajectory stabilizer for autonomous AI agents and tool-calling loops.

## The Problem
When autonomous agents hit failing tool calls or ambiguous environments, they frequently enter degenerative loops:
1. **Immediate Stutters**: Repeatedly calling the same tool with identical parameters.
2. **Oscillating Cycles**: Alternating between two or three steps (e.g. `list_dir` -> `view_file` -> `list_dir` -> `view_file`) without progressing environment state.

DWEL intercepts cycles deterministically using rolling action hashing and n-gram trajectory matching before token burn occurs.

## Installation
```bash
pip install dwel
```

## Quick Start
```python
from dwel import CycleDetector, ActionTrace

detector = CycleDetector(window_size=8, max_cycle_repeats=2)

# Record action traces
trace = ActionTrace(tool="view_file", params={"path": "config.json"})
is_cycle, diag = detector.evaluate(trace)

if is_cycle:
    print(f"Cycle intercepted! Length: {diag.cycle_length}, Reason: {diag.reason}")
    # Inject remediation directive to agent prompt
```

## Benchmarks
- Hash & Detection Latency: **< 0.15ms** per action on standard modern x86/ARM hardware.
- Memory Overhead: **< 32KB** per session history buffer.
- External Dependencies: **Zero** (pure Python standard library).

## License
Distributed under the Apache License, Version 2.0. Copyright (c) 2026 Jaswanth Reddy.
