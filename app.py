from agent.graph import ask
from agent.parser import parse_tool_call
from tools.dispatcher import execute
import json

history = []

print("===== AI Agent v0.6 =====")

while True:

    user = input("\nYou > ")

    history.append({
        "role": "user",
        "content": user
    })

    while True:

        reply = ask(history)

        print("\nAI:\n")
        print(reply)

        tool = parse_tool_call(reply)

        # AI answered normally
        if tool is None:

            history.append({
                "role": "assistant",
                "content": reply
            })

            break

        # Execute requested tool
        output = execute(tool)

        print("\nTool Output:\n")
        print(json.dumps(output, indent=4))

        # VERY IMPORTANT
        history.append({
            "role": "assistant",
            "content": reply
        })

        history.append({
            "role": "user",
            "content":
f"""
The requested tool has already been executed.

Tool Output:

{json.dumps(output, indent=4)}

If the task is complete,
respond normally.

Otherwise call another tool.
"""
        })