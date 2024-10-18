import asyncio
import websockets
import matplotlib.pyplot as plt
import numpy as np
import json

g_PasswordCorrect = False

async def plot_updates(plot, guess):
    plt.ion() 
    plt.title('Power Trace Capture')
    
    line, = plt.plot(plot['x'], plot['y'], label=guess)
    plt.legend()
    plt.xlabel('Time (ms)')
    plt.ylabel('Current (milliamperes)')

async def main():
    global g_PasswordCorrect
    uri = "ws://localhost:6789"

    async with websockets.connect(uri) as websocket:
        # Receive the initial message.
        initial_message = json.loads(await websocket.recv())
        assert('kind' in initial_message and initial_message['kind'] == 'boot')
        print(initial_message['content'])

        # Keep going until the password is determined correct.
        while not g_PasswordCorrect:
            # This is where we enter our password.
            guess = input('')
            
            # This is where we send our input.
            await websocket.send(guess)

            # This is where we get our response.
            response = json.loads(await websocket.recv())
            
            # If the password is the wrong length, then just forward the message from the server.
            if response['kind'] == 'password' and not response['is_correct'] and response['reason'] == 'wrong_character_count':
                print(response['content'])
                continue
            
            # The password is the right length, lets plot the trace.
            await plot_updates(response['trace'], f'password = {guess}')

            # Check if the password is correct.
            if response['is_correct']:
                g_PasswordCorrect = True
                print(response['content'])
                continue
            
            # Password isn't correct, but is the same length; print the server message.
            print(response['content'])

if __name__ == '__main__':
    asyncio.run(main())
