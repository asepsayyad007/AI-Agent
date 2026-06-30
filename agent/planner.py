from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Plan:
    goal: str
    summary: str
    risk: str
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

        if not plan.goal.strip():
            errors.append("Goal is missing.")

        if not plan.summary.strip():
            errors.append("Summary is missing.")

        if plan.risk not in ["LOW", "MEDIUM", "HIGH"]:
            errors.append("Risk must be LOW, MEDIUM or HIGH.")

        if len(plan.actions) == 0:
            errors.append("Plan contains no actions.")

        for i, action in enumerate(plan.actions, start=1):

            tool = action.get("tool")

            if tool not in Planner.VALID_TOOLS:
                errors.append(
                    f"Step {i}: Unknown tool '{tool}'."
                )
                continue

            if tool == "terminal":
                if "command" not in action:
                    errors.append(
                        f"Step {i}: Missing command."
                    )

            else:

                if "path" not in action:
                    errors.append(
                        f"Step {i}: Missing path."
                    )

        return errors

    @staticmethod
    def print(plan: Plan):

        print("\n" + "=" * 60)
        print("                EXECUTION PLAN")
        print("=" * 60)

        print(f"\nGoal")
        print(f"  {plan.goal}")

        print(f"\nSummary")
        print(f"  {plan.summary}")

        print(f"\nRisk")
        print(f"  {plan.risk}")

        create = []
        read = []
        delete = []
        commands = []

        for action in plan.actions:

            tool = action["tool"]

            if tool == "write_file":
                create.append(action["path"])

            elif tool == "read_file":
                read.append(action["path"])

            elif tool == "delete_file":
                delete.append(action["path"])

            elif tool == "terminal":
                commands.append(action["command"])

        if create:

            print("\nCreate Files")

            for f in create:
                print(f"  + {f}")

        if read:

            print("\nRead Files")

            for f in read:
                print(f"  * {f}")

        if delete:

            print("\nDelete Files")

            for f in delete:
                print(f"  - {f}")

        if commands:

            print("\nCommands")

            for cmd in commands:
                print(f"  > {cmd}")

        print("\n" + "=" * 60)