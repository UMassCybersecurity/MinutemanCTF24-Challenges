import socket
import os
from sys import argv

def usage():
    print(f"Usage: {argv[0]} HOST PORT")

def help():
    print("""
Hardware

Atmega 1280
          
There is a LED on .
 - It functions like a normal 7 bit address I2C device
 - In write mode: 
    - It will first take 3 bytes for the data address. (little endian)
    - Then write to that address and auto incriment for each byte of data sent.
 - In read mode:
    - It will use the last data address from the current transaction.
    - Then read the byte at that address and auto incriment.
 - Note: 
    - When in read mode, the eeprom does not use the ACK bit and a stop signal must be sent to end the transaction.
    - When a transaction is ended, the data address is reset to 0

There is also a laser module on io port C. 
- To use it simply set the pins on the port(register) to the desired intensity.


Commands

  firmware <command> <flags...>
    commands:
        upload  [PATH]  Uploads a firmware from your computer onto the simulation enviornment. 
                        It will have the same file name as on your computer and may overwrite old files.
        list            List the firmwares avalible to upload to microcontroller
        load    [PATH]  Resets the microcontroller and loads a firmware from the simulation enviornment onto the microcontroller.
        uplload [PATH]  Uploads then loads a firmware
    flags:
        -r              Resets the peripherals (loads default eeprom data) and uart log file before loading firmware
        -s              Start the microcontroller once the firmware is loaded
  
  sim <commands...>
    commands:
        start           Starts the microcontroller. Note: you need to load firmware first.
        stop            Stops the microcontroller
        reset           Stops and resets the microcontroller
        restart         Resets and starts the microcontroller
        resetperf       Stops the microcontroller and resets peripherals (loads default eeprom data)
        state           Gets the state of the microcontroller

  log <type> <flags...>
    types:
        uart            Gets the serial(uart 0) communication from the controller
                        *This will default decode the bytes when printing to the terminal 
        error           Gets all messages from stderr in the enviornment (good for troubleshooting)
    flags:
        -p      [PATH]  Downlaod the log to a path
        -c              Clear the log in the environment
        -r              Use raw bytes (only applies when printing to terminal)
        -a              Append to a file instead of overwriting it (only used with -p)
          
  help              Prints the help message(this message)
  last              Runs the last valid command (does not check if command was parsed or run correctly)
  flag              Tries to get the flag
  exit              Exits the program
""")

def send_data(data: bytes)->bool:    
    con.sendall(int.to_bytes(len(data), 4, 'little'))
    
    recv = con.recv(1)
    if not recv or not recv == b'\x00': # check for return err
        return False
        
    con.sendall(data)
    
    recv = con.recv(1)
    if not recv or not recv == b'\x00': # check for return err
        return False
        
    return True

def get_data() -> tuple[bool, bytes|None]:
    recv = con.recv(4)
    if not len(recv) == 4:
        con.sendall(b'\x01') # transaction error
        return (False, None)
    con.sendall(b'\x00') # Ok
    
    size = int.from_bytes(recv, 'little', signed=False)
    recv = b''
    while len(recv) < size:
        recv += con.recv(size - len(recv))
    
    # if not len(recv) == size:
    #     con.sendall(b'\x01') # transaction error
    #     return (False, None)

    con.sendall(b'\x00') # Ok

    return (True, recv)

def get_transaction_type(targets : list[int], error_base: str) -> tuple[bool,bytes|None]:
    recv = con.recv(1)
    if not recv or not recv[0] & 0x0f in targets: # didn't recv valid transaction
        print(f"{error_base} server did not repond correctly")
        return (False, None)
    return (True, recv)

def handle_firmware_upload(path : str):
    s = True

    error_base = "firmware: upload:"
    
    if not os.path.isfile(path):
        print(f"{error_base} the path supplied is invalid")
        return False
    
    with open(path, 'rb') as f:
        data = f.read()

    con.sendall(b'\x00') # send fimrware upload command
    if not get_transaction_type([0], error_base)[0]:
        return False

    if not send_data(os.path.basename(path).encode()):
        print(f"{error_base} failed to send file name")
        s = False
    
    if not get_transaction_type([0], error_base):
        return False
    
    if not send_data(data):
        print(f"{error_base} failed to send file")
        s = False
        
    valid = get_transaction_type([2], error_base)
    if valid[0] and not valid[1] == b'\x02':
        print(f"{error_base} server failed to save file")
        return False

    return s

def handle_firmware_list():
    error_base = "firmware: list:"

    con.sendall(b'\x01') # send fimrware list command
    
    transaction_data = get_transaction_type([1,2], error_base)
    while transaction_data[0]:
        if transaction_data[1][0] & 0x0f == 2: # end
            if not transaction_data[1][0] & 0xf0 == 0: # error
                print(f"{error_base} server failed to send file names")
            return
        
        data = get_data()
        if not data[0]:
            print(f"{error_base} failed to get file name")
            continue

        print(data[1].decode())

        transaction_data = get_transaction_type([1,2], error_base)

def handle_firmware_load(file_name : str):
    error_base = "firmware: load:"

    con.sendall(b'\x02') # send fimrware load command
    if not get_transaction_type([0], error_base)[0]:
        return

    if not send_data(file_name.encode()):
        print(f"{error_base} failed to send file name")
        
    valid = get_transaction_type([2], error_base)
    if not (valid[0] and valid[1] == b'\x02'):
        print(f"{error_base} server failed to load file")

def handle_sim_start():
    error_base = "sim: start:"

    con.sendall(b'\x03') # send sim start command

    valid = get_transaction_type([2], error_base)
    if valid[0] and not valid[1] == b'\x02': # error
        print(f"{error_base} server failed to start simulation")

def handle_sim_stop():
    error_base = "sim: stop:"

    con.sendall(b'\x04') # send sim stop command

    valid = get_transaction_type([2], error_base)
    if valid[0] and not valid[1] == b'\x02': # error
        print(f"{error_base} server failed to stop simulation")

def handle_sim_reset():
    error_base = "sim: reset:"

    con.sendall(b'\x05') # send sim reset command

    valid = get_transaction_type([2], error_base)
    if valid[0] and not valid[1] == b'\x02': # error
        print(f"{error_base} server failed to reset simulation")

def handle_sim_reset_perfs():
    error_base = "sim: reset peripherals:"

    con.sendall(b'\x06') # send sim reset perfs command

    valid = get_transaction_type([2], error_base)
    if valid[0] and not valid[1] == b'\x02': # error
        print(f"{error_base} server failed to reset simulation peripherals")

state_map = {
    0:"CPU Limbo",
    1:"CPU Stopped",
    2:"CPU Running",
    3:"CPU Sleeping",
    4:"CPU Step",
    5:"CPU Step Done",
    6:"CPU Done",
    7:"CPU Crashed",
}

def handle_sim_get_state():
    error_base = "sim: get state:"

    con.sendall(b'\x07') # send sim state command

    recv = con.recv(1)
    if not recv:
        print(f"{error_base} failed to recive sim state")
    else:
        if recv[0] not in state_map:
            print(f"{error_base} server returned unknown state")
        else:
            print(f"AVR simulator state: {state_map[recv[0]]}")

    valid = get_transaction_type([2], error_base)
    if valid[0] and not valid[1] == b'\x02': # error (should never trigger)
        print(f"{error_base} server failed to get sim state")

def handle_get_log(type: str, cmd: bytes, path: str | None = None, append: bool = False, print_raw: bool = False):
    error_base = f"log: {type}:"
    
    con.sendall(cmd) # send get uart command

    if not get_transaction_type([1], error_base)[0]:
        return

    data = get_data()
    if not data[0]:
        print(f"{error_base} failed to receive uart log")
    else:
        if path:
            with open(path, 'ab' if append else 'wb') as f:
                if not f.writable():
                    print(f"{error_base} can not write to {path}")
                else:
                    f.write(data[1])
        else:
            try:
                print(data[1] if print_raw else data[1].decode())
            except(UnicodeDecodeError):
                print(f"{error_base} failed to decode log, try using the -r flag")
    
    valid = get_transaction_type([2], error_base)
    if valid[0] and not valid[1] == b'\x02': # error
        print(f"{error_base} server failed to get {type} log")


def handle_get_uart_log(path: str | None = None, append: bool = False, print_raw: bool = False):
    handle_get_log("uart", b'\x08', path, append, print_raw)


def handle_clear_uart_log():
    error_base = "log: uart:"

    con.sendall(b'\x09') # send clear uart command

    transaction_data = get_transaction_type([2], error_base)
    if transaction_data[0] and not transaction_data[1] == b'\x02': # error
        print(f"{error_base} server failed to clear uart log")

def handle_get_error_log(path: str | None = None, append: bool = False, print_raw: bool = False):
    handle_get_log("error", b'\x0a', path, append, print_raw)

def handle_clear_error_log():
    error_base = "log: error:"

    con.sendall(b'\x0b') # send clear error command

    transaction_data = get_transaction_type([2], error_base)
    if transaction_data[0] and not transaction_data[1] == b'\x02': # error
        print(f"{error_base} server failed to clear error log")


def handle_firmware(tokens):
    if not tokens:
        print("firmware: no command supplied")
        return
    
    command = tokens[0]
    if not command in ['list', 'upload', 'load', 'uplload']:
        print(f"firmware: unknown command {command}")
        return

    if not command == 'list':
        if not len(tokens) >= 2:
            print(f"firmware: command {command} requires a path")
            return
        
        path = tokens[1]
    
    tokens = tokens[2:]

    flags=[]
    for token in tokens:
        if not token in ['-r', '-s']:
            print(f"firmware: unknown token {token}")
            return
        flags.append(token)

    if '-r' in flags:
        handle_sim_reset_perfs()
        handle_clear_uart_log()

    match command:
        case 'list':
            handle_firmware_list()
        case 'upload':
            handle_firmware_upload(path)
        case 'load':
            handle_firmware_load(path)
        case 'uplload':
            if(handle_firmware_upload(path)):
                handle_firmware_load(os.path.basename(path))

    if '-s' in flags:
        handle_sim_start()

def handle_sim(tokens):
    for token in tokens:
        match token:
            case 'start':
                handle_sim_start()
            case 'stop':
                handle_sim_stop()
            case 'reset':
                handle_sim_reset()
            case 'restart':
                handle_sim_reset()
                handle_sim_start()
            case 'resetperf':
                handle_sim_reset_perfs()
            case 'state':
                handle_sim_get_state()
            case _:
                print(f"sim: unknown command verb {token}")
                return

def handle_log(tokens):
    if not tokens:
        print("log: no type supplied")

    type = tokens[0]
    tokens = tokens[1:]

    path_required = False
    flags = {}
    avalible_flags = ['-p', '-c', '-r', '-a']
    for t in tokens:
        if path_required:
            flags['-p']=t
            path_required = False
            continue

        if not t in avalible_flags:
            print(f"log: unknown token {t}")
            return

        if t in flags:
            print(f"log: flag {t} was used twice")
            return

        if t == '-p':
            path_required = True

        flags[t]=None

    if path_required:
        print("log: the -p path flag was used but no path was supplied")
        return
    
    match type:
        case 'uart':
            if '-p' in flags:
                handle_get_uart_log(flags['-p'], '-a' in flags)
            elif not '-c' in flags:
                handle_get_uart_log(print_raw= '-r' in flags)
            if '-c' in flags:
                handle_clear_uart_log()
        case 'error':
            if '-p' in flags:
                handle_get_error_log(flags['-p'], '-a' in flags)
            elif not '-c' in flags:
                handle_get_error_log(print_raw= '-r' in flags)
            if '-c' in flags:
                handle_clear_error_log()
        case _:
            print(f"log: unknown type {type}")

def handle_flag():
    error_base = "flag:"

    con.sendall(b'\x0c') # send get flag command

    valid = get_transaction_type([1,2], error_base)
    if not valid[0]:
        print("flag: unknown server behavior")
        return
    
    if valid[1][0] & 0x0f == 2: # end
        if valid[1][0] & 0xf0 == 0x30:
            print("Flag is not unlocked yet")
        else:
            print(f"{error_base} server was unable to get flag")
        return

    data = get_data()
    if not data[0]:
        print(f"{error_base} failed to receive flag")
    else:
        print(data[1].decode())

    valid = get_transaction_type([2], error_base)
    if valid[0] and not valid[1] == b'\x02': # error
        print(f"{error_base} server failed to get flag")

last_command = "exit"
def handle_command(data: str): 
    global last_command
    tokens = list(filter(lambda s : not s == '', data.split(" ")))
    if not len(tokens):
        return
    cmd = tokens[0].lower()
    try:
        match cmd:
            case "firmware":
                handle_firmware(tokens[1:])
            case "sim":
                handle_sim(tokens[1:])
            case "log":
                handle_log(tokens[1:])
            case "exit":
                print("goodbye :)")
                exit(0)
            case "help":
                help()
            case "flag":
                handle_flag()
            case "last":
                handle_command(last_command)
            case _:
                print(f"Unknown command {cmd}. Type help for help")
                return
    except(Exception):
        print(f"Fatal error running command {cmd}.")
        return
    
    if not cmd == "last":
        last_command = data


if __name__ == "__main__":
    if(len(argv) != 3):
        usage()
        exit(2)
    host = argv[1]
    port = argv[2]
    print(f"Connecting to '{host}' on port {port}")
    con = socket.create_connection([host,port], 10)
    print("Connected!")
    print("Welcome to Minuteman CTF :)")
    help()
    print("Enter a command")
    while(True):
        handle_command(input(">>> "))