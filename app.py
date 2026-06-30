import json

from agent.graph import ask
from agent.parser import parse_ai_response
from agent.approval import request_approval, reset
from tools.dispatcher import execute

history = []

print("===== AI Agent v0.8 Planner =====")

while True:

    reset()

    user = input("\nYou > ").strip()

    if user.lower() in ["exit", "quit"]:
        break

    history.append({
        "role": "user",
        "content": user
    })

    reply = ask(history)

    print("\nAI:\n")
    print(reply)

    parsed = parse_ai_response(reply)

    # -----------------------------------
    # Normal Text
    # -----------------------------------

    if parsed["type"] == "text":

        history.append({
            "role": "assistant",
            "content": parsed["data"]
        })

        continue

    # -----------------------------------
    # Single Tool (Backward Compatibility)
    # -----------------------------------

    if parsed["type"] == "tool":

        plan = [
            parsed["data"]
        ]

    # -----------------------------------
    # Planner
    # -----------------------------------

    elif parsed["type"] == "plan":

        plan = parsed["data"]

    else:

        print("Unknown response.")
        continue

    # -----------------------------------
    # Approval
    # -----------------------------------

    approved = request_approval(plan)

    if not approved:

        print("\nExecution cancelled.\n")
        continue

    # -----------------------------------
    # Execute Plan
    # -----------------------------------

    print("\nExecuting...\n")

    for i, step in enumerate(plan, start=1):

        print(f"Step {i}")

        result = execute(step)

        print(json.dumps(result, indent=4))
        print()

    print("Plan completed.")