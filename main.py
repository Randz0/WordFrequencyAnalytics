import CommandManagement

CommandManagement.AddHelpMenu()

consoleInput = input(": ")

while consoleInput != "-exit":
    command = CommandManagement.RecieveNextCommand(consoleInput)

    if command == None:
        consoleInput = input(": ")
        continue

    command.TryActivateCommand()

    consoleInput = input(": ")
