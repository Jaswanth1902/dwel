"""
dwel.server — Fast MCP server for runtime agent cycle detection.
"""

from __future__ import annotations
import json
import sys
from typing import Any, Dict, List, Optional

from .detector import ActionTrace, get_cycle_detector


def handle_evaluate(params: Dict[str, Any]) -> Dict[str, Any]:
    tool = params.get("tool", "")
    tool_params = params.get("params", {})
    output = params.get("output", "")
    detector = get_cycle_detector()
    trace = ActionTrace(tool=tool, params=tool_params, output=output)
    is_cycle, diag = detector.evaluate(trace)
    return {
        "is_cycle": is_cycle,
        "cycle_length": diag.cycle_length,
        "repetitions": diag.repetitions,
        "reason": diag.reason,
        "suggested_remediation": diag.suggested_remediation,
    }


def main():
    """Stdio JSON-RPC server loop for MCP."""
    detector = get_cycle_detector()
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "tools": [
                        {
                            "name": "evaluate_action",
                            "description": "Evaluates agent action for repetitive or oscillating execution cycles in < 0.5ms.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "tool": {"type": "string"},
                                    "params": {"type": "object"},
                                    "output": {"type": "string"}
                                },
                                "required": ["tool"]
                            }
                        }
                    ]
                }
                resp = {"jsonrpc": "2.0", "id": req_id, "result": res}
            elif method == "tools/call":
                call_name = params.get("name")
                call_args = params.get("arguments", {})
                if call_name == "evaluate_action":
                    eval_res = handle_evaluate(call_args)
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(eval_res)}]
                        }
                    }
                else:
                    resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            elif method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "dwel", "version": "0.1.0"}
                    }
                }
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
