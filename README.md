<div align="center">

# 🛑 DWEL
### Ultra-Lightweight Token Budget & Loop Circuit Breaker for AI Agents

[![Runtime: Sub-Millisecond](https://img.shields.io/badge/Interception-<0.5ms-brightgreen?style=flat-square)](https://github.com/Jaswanth1902/dwel)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)]()
[![Zero-Dependency](https://img.shields.io/badge/Dependencies-Zero-success?style=flat-square)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

**Stop runaway AI agent loops from burning your API credit balance.**  
DWEL intercepts non-progressing agent loops, repeated identical tool calls, and runaway token expansion in sub-millisecond latency.

[🚀 3-Line Quickstart](#quickstart) • [🛡️ Circuit Breaker Modes](#modes) • [📊 Benchmarks](#benchmarks)

</div>

---

### 🚀 3-Line Quickstart

```python
from dwel import circuit_breaker

@circuit_breaker(max_cycles=3, max_tokens=8000)
def agent_execution_step(prompt, history):
    # If the agent attempts 3 identical actions or exceeds token budget,
    # DWEL raises CircuitBreakerTripped and cleanly halts the loop.
    return llm.generate(prompt, history)
```
