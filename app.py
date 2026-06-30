from agent.graph import ask
from agent.parser import parse_tool_call
from tools.terminal import run

history = []

print("===== AI Agent v0.4 =====")

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

        # If AI wants to use a tool
        if tool:

            if tool["tool"] == "terminal":

                command = tool["command"]

                print(f"\nExecuting: {command}\n")

                result = run(command)

                tool_output = f"""
Command:
{command}

Return Code:
{result["returncode"]}

STDOUT:
{result["stdout"]}

STDERR:
{result["stderr"]}
"""

                # Give command output back to AI
                history.append({
                    "role": "user",
                    "content": tool_output
                })

                # Let AI think again
                continue

        # Normal response
        history.append({
            "role": "assistant",
            "content": reply
        })

        break