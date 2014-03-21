# cChat.py
# defines the 'say' command, the 'tell' command, the 'yell' command, the 'global' command, and all individual chat channel commands

def say(client, args, CLIENT_LIST, CLIENT_DATA):
    """
    Echo whatever client types after the command 'say' to everyone.
    """

    message = ""
    space = " "
    # for arg in args:
    message = space.join(args)
    clientDataLoc = str(client.addrport())
    prompt = CLIENT_DATA[clientDataLoc]['prompt']

    print '%s: %s' % (CLIENT_DATA[clientDataLoc]['name'], message)

    for guest in CLIENT_LIST:
        if guest != client:
            guest.send('\n%s: %s\n' % (CLIENT_DATA[clientDataLoc]['name'], message))
            # guest.send(prompt)
        else:
            guest.send('You say "%s"\n' % message)
            # guest.send(prompt)