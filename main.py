import CommandManagement

consoleInput = input(": ")

while consoleInput != "-exit":
    command = CommandManagement.RecieveNextCommand(consoleInput)

    if command == None:
        consoleInput = input(": ")
        continue

    command.ActivateCommand()

    consoleInput = input(": ")