from agent.graph import ask
from tools.terminal import run

history = []

print("===== AI Agent =====")

while True:

    user = input("\nYou > ")

    history.append(
        {
            "role": "user",
            "content": user
        }
    )

    reply = ask(history)

    print("\nAI:\n")
    print(reply)

    history.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    if reply.startswith("TOOL: terminal"):

        command = reply.split("COMMAND:")[1].strip()

        print("\nExecuting...\n")

        result = run(command)

        print(result["stdout"])

        if result["stderr"]:
            print(result["stderr"])

