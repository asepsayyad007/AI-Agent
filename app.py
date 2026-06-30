from agent.graph import ask
from agent.parser import parse_tool_call
from tools.dispatcher import execute

history = []

print("===== AI Agent v0.5 =====")

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

        # No tool needed
        if tool is None:

            history.append({
                "role": "assistant",
                "content": reply
            })

            break

        # Execute requested tool
        output = execute(tool)

        history.append({
            "role": "user",
            "content": str(output)
        })