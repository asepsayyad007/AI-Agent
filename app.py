import json

from agent.graph import ask
from agent.parser import parse_ai_response
from agent.planner import Plan, Planner
from agent.approval import request_approval, reset
from tools.dispatcher import execute

history = []

print("===== AI Agent v0.8 Planner =====")

while True:

    reset()

    user = input("\nYou > ").strip()

    if user.lower() in ("exit", "quit"):
        break

    history.append(
        {
            "role": "user",
            "content": user,
        }
    )

    reply = ask(history)

    parsed = parse_ai_response(reply)

    # ----------------------------------------
    # TEXT
    # ----------------------------------------

    if parsed["type"] == "text":

        print("\nAI:\n")
        print(parsed["data"])

        history.append(
            {
                "role": "assistant",
                "content": parsed["data"],
            }
        )

        continue

    # ----------------------------------------
    # LEGACY TOOL
    # ----------------------------------------

    if parsed["type"] == "tool":

        plan = Plan(
            goal="Single Tool",
            summary="Legacy execution",
            risk="LOW",
            actions=[parsed["data"]],
        )

    # ----------------------------------------
    # PLANNER
    # ----------------------------------------

    elif parsed["type"] == "plan":

        data = parsed["data"]

        plan = Plan(
            goal=data.get("goal", ""),
            summary=data.get("summary", ""),
            risk=data.get("risk", "LOW"),
            actions=data.get("plan", []),
        )

    else:

        print("Unknown response.")
        continue

    # ----------------------------------------
    # VALIDATE
    # ----------------------------------------

    errors = Planner.validate(plan)

    if errors:

        print("\nInvalid Plan\n")

        for err in errors:
            print(f"• {err}")

        continue

    # ----------------------------------------
    # SHOW PLAN
    # ----------------------------------------

    Planner.print(plan)

    # ----------------------------------------
    # APPROVAL
    # ----------------------------------------

    if not request_approval(plan.actions):

        print("\nExecution cancelled.\n")
        continue

    # ----------------------------------------
    # EXECUTE
    # ----------------------------------------

    print("\nExecuting...\n")

    success = 0
    failed = 0

    for index, step in enumerate(plan.actions, start=1):

        print(f"Step {index}")

        result = execute(step)

        print(json.dumps(result, indent=4))
        print()

        if result.get("success", False):
            success += 1
        else:
            failed += 1
            print("Execution stopped.")
            break

    # ----------------------------------------
    # SUMMARY
    # ----------------------------------------

    print("=" * 60)
    print("EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Goal    : {plan.goal}")
    print(f"Success : {success}")
    print(f"Failed  : {failed}")
    print("=" * 60)