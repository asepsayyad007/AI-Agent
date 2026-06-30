AUTO_APPROVE = False
AUTO_DENY = False


def reset():
    global AUTO_APPROVE
    global AUTO_DENY

    AUTO_APPROVE = False
    AUTO_DENY = False


def request_approval(plan):

    global AUTO_APPROVE
    global AUTO_DENY

    if AUTO_APPROVE:
        return True

    if AUTO_DENY:
        return False

    create_files = []
    read_files = []
    modify_files = []
    delete_files = []
    commands = []

    for step in plan:

        tool = step.get("tool")

        if tool == "write_file":
            create_files.append(step.get("path"))

        elif tool == "read_file":
            read_files.append(step.get("path"))

        elif tool == "delete_file":
            delete_files.append(step.get("path"))

        elif tool == "terminal":
            commands.append(step.get("command"))

    print()
    print("=" * 60)
    print("                EXECUTION PLAN")
    print("=" * 60)

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

    if modify_files:
        print("\nModify Files")
        print("-" * 20)
        for f in modify_files:
            print(f"~ {f}")

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

    print()
    print("=" * 60)

    print("\n[Y] Yes")
    print("[N] No")
    print("[A] Always Yes (Current Request)")
    print("[D] Always No (Current Request)")

    while True:

        choice = input("\nChoice > ").strip().lower()

        if choice == "y":
            return True

        if choice == "n":
            return False

        if choice == "a":
            AUTO_APPROVE = True
            return True

        if choice == "d":
            AUTO_DENY = True
            return False

        print("Invalid choice.")