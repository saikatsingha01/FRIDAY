# ==========================================================
# CALCULATOR TOOL
#
# Phase 5 — safe arithmetic evaluation. Replaces the old
# eval()-based calculate() with an ast-based evaluator that
# never executes arbitrary code. Receives a structured
# expression parameter, never raw user text.
# ==========================================================

import ast
import operator

from src.contracts.tool import (
    ToolRequest,
    ToolResult,
    ToolMetadata,
    ToolPermission,
)
from src.skills.skill_registry import register
from src.skills.tool_base import BaseTool


_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalculatorTool(BaseTool):

    metadata = ToolMetadata(
        name="calculate",
        description=(
            "Evaluate a simple arithmetic expression "
            "(numbers and basic operators only)."
        ),
        capabilities=["mathematics"],
        goals=["calculate", "solve_problem"],
        permission=ToolPermission.SAFE,
        actions={
            "evaluate": {
                "input": {
                    "expression": "str — a plain arithmetic expression",
                },
                "output": {
                    "result": "number",
                },
            },
        },
        needs_network=False,
        errors=["unsupported_action", "empty_expression", "invalid_expression"],
    )

    def execute(self, request: ToolRequest) -> ToolResult:

        action = request.action

        if action != "evaluate":
            return self.fail(
                request,
                f"unsupported_action: {action}",
            )

        expression = str(request.parameters.get("expression") or "").strip()

        if not expression:
            return self.fail(request, "empty_expression")

        try:
            value = self._eval_expr(expression)
        except Exception as exc:
            return self.fail(
                request,
                f"invalid_expression: {type(exc).__name__}: {exc}",
            )

        return self.ok(request, data={"result": value})

    def _eval_expr(self, expression: str):
        tree = ast.parse(expression, mode="eval")

        return self._walk(tree.body)

    def _walk(self, node):

        if isinstance(node, ast.Expression):
            return self._walk(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("non-numeric constant")

        if isinstance(node, ast.BinOp):
            left = self._walk(node.left)
            right = self._walk(node.right)
            op = _BIN_OPS.get(type(node.op))
            if op is None:
                raise ValueError("unsupported operator")
            return op(left, right)

        if isinstance(node, ast.UnaryOp):
            operand = self._walk(node.operand)
            op = _UNARY_OPS.get(type(node.op))
            if op is None:
                raise ValueError("unsupported operator")
            return op(operand)

        raise ValueError(f"unsupported expression node: {type(node).__name__}")


def calculate(expression):
    """
    Back-compat wrapper for the old signature. Returns a string
    for callers that have not migrated to ToolRequest yet.
    """
    tool = CalculatorTool()
    result = tool.execute(ToolRequest(
        tool_name="calculate",
        action="evaluate",
        parameters={"expression": expression},
    ))
    if result.is_ok():
        return f"The answer is {result.data['result']}"
    return "I couldn't calculate that."


calculator_tool = CalculatorTool()

register(calculator_tool)
