from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Plan:
    goal: str
    summary: str = ""
    risk: str = ""
    actions: List[Dict[str, Any]] = field(default_factory=list)


class Planner:

    VALID_TOOLS = {
        "terminal",
        "read_file",
        "write_file",
        "delete_file",
        "list_directory",
    }

    @staticmethod
    def validate(plan: Plan):

        errors = []

        # Goal is mandatory
        if not plan.goal.strip():
            errors.append("Goal is missing.")

        # Plan must contain at least one action
        if len(plan.actions) == 0:
            errors.append("Plan contains no actions.")

        # Risk is optional
        if plan.risk:
            if plan.risk.upper() not in ("LOW", "MEDIUM", "HIGH"):
                errors.append(
                    "Risk must be LOW, MEDIUM or HIGH."
                )

        # Validate every action
        for i, action in enumerate(plan.actions, start=1):

            if not isinstance(action, dict):
                errors.append(
                    f"Step {i}: Invalid action."
                )
                continue

            tool = action.get("tool")

            if tool not in Planner.VALID_TOOLS:
                errors.append(
                    f"Step {i}: Unknown tool '{tool}'."
                )
                continue

            # ----------------------------
            # Terminal
            # ----------------------------

            if tool == "terminal":

                if not action.get("command"):
                    errors.append(
                        f"Step {i}: Missing command."
                    )

                continue

            # ----------------------------
            # Filesystem tools
            # ----------------------------

            if not action.get("path"):
                errors.append(
                    f"Step {i}: Missing path."
                )

            if tool == "write_file":

                if "content" not in action:
                    errors.append(
                        f"Step {i}: Missing content."
                    )

        return errors

    @staticmethod
    def print(plan: Plan):

        print("\n" + "=" * 60)
        print("                EXECUTION PLAN")
        print("=" * 60)

        print(f"\nGoal:\n  {plan.goal}")

        if plan.summary:
            print(f"\nSummary:\n  {plan.summary}")

        if plan.risk:
            print(f"\nRisk:\n  {plan.risk}")

        create_files = []
        read_files = []
        delete_files = []
        commands = []

        for action in plan.actions:

            tool = action["tool"]

            if tool == "write_file":
                create_files.append(action["path"])

            elif tool == "read_file":
                read_files.append(action["path"])

            elif tool == "delete_file":
                delete_files.append(action["path"])

            elif tool == "terminal":
                commands.append(action["command"])

        if create_files:
            print("\nCreate Files")
            print("-" * 20)
            for f in create_files:
                print(f"+ {f}")

        if read_files:
            print("\nRead Files")
            print("-" * 20)
            for f in read_files:
                print(f"* {f}")

        if delete_files:
            print("\nDelete Files")
            print("-" * 20)
            for f in delete_files:
                print(f"- {f}")

        if commands:
            print("\nCommands")
            print("-" * 20)
            for cmd in commands:
                print(f"> {cmd}")

        print("\n" + "=" * 60)