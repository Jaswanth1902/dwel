import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ActionTrace:
    tool: str
    params: Dict[str, Any] = field(default_factory=dict)
    output: str = ""
    exit_code: Optional[int] = 0

    def fingerprint(self) -> str:
        """Generates deterministic semantic fingerprint for the action."""
        # Normalize params by sorting keys
        norm_params = json.dumps(self.params, sort_keys=True, default=str)
        # Normalize output sample
        out_sample = self.output[:256].strip()
        raw = f"{self.tool}::{norm_params}::{out_sample}::{self.exit_code}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


@dataclass
class CycleDiagnosis:
    is_cycle: bool
    cycle_length: int = 0
    repetitions: int = 0
    reason: str = ""
    suggested_remediation: str = ""


class CycleDetector:
    """Runtime cyclic loop interceptor for AI agent action streams."""

    def __init__(self, window_size: int = 8, max_cycle_repeats: int = 2):
        self.window_size = window_size
        self.max_cycle_repeats = max_cycle_repeats
        self.history: List[str] = []
        self.traces: List[ActionTrace] = []

    def evaluate(self, trace: ActionTrace) -> Tuple[bool, CycleDiagnosis]:
        fp = trace.fingerprint()
        self.history.append(fp)
        self.traces.append(trace)

        if len(self.history) < 3:
            return False, CycleDiagnosis(is_cycle=False)

        # 1. Immediate identical stutter: A -> A -> A
        if len(self.history) >= 2 and self.history[-1] == self.history[-2]:
            stutter_count = 0
            for item in reversed(self.history):
                if item == fp:
                    stutter_count += 1
                else:
                    break
            if stutter_count >= self.max_cycle_repeats:
                return True, CycleDiagnosis(
                    is_cycle=True,
                    cycle_length=1,
                    repetitions=stutter_count,
                    reason=f"Repeated identical tool call '{trace.tool}' without state progression ({stutter_count} times).",
                    suggested_remediation="Mutate search query, verify previous failure message, or escalate to architect mode."
                )

        # 2. Oscillating cycle detection (A -> B -> A -> B)
        recent = self.history[-self.window_size:]
        n = len(recent)
        for k in range(2, n // 2 + 1):
            pattern = recent[-k:]
            prev_pattern = recent[-2*k:-k]
            if pattern == prev_pattern:
                return True, CycleDiagnosis(
                    is_cycle=True,
                    cycle_length=k,
                    repetitions=2,
                    reason=f"Detected oscillating {k}-step execution cycle in agent trajectory.",
                    suggested_remediation="Break oscillation by changing strategy or executing a standalone minimal test."
                )

        return False, CycleDiagnosis(is_cycle=False)
