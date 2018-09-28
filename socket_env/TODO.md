## Problems
* thread(GUI DEAD)
* sent package in order, player by player
* effient package, only with message I need or data is compressed

For now in simple_client and simple_server package order is right and server send just 26 packages(5\*5+1) in order which is great and just what I want

but this is just simple socket, and for player without move, has to sent that package just get back which is not right

how server to check if that client socket is close I am not sure if it is right, using if thet recv is `b''`
