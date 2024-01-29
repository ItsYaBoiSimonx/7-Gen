import httpx,json,string, threading, requests, random
from random import choice,choices
import time 
from uuid import uuid4
from datetime import datetime
from pystyle import Colorate, Center, Colors, Write
import os
from colorama import Fore, Style, Back


def set_console_window_size(width, height):
    os.system(f"mode con: cols={width} lines={height}")

def generate_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_email():
    username_length = random.randint(5, 10)
    domain_length = random.randint(5, 8)

    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(username_length))
    domain = ''.join(random.choice(string.ascii_lowercase) for _ in range(domain_length))

    email = f"{username}@{domain}.com"
    return email

def warning(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"{Fore.LIGHTBLACK_EX}{timestamp} {Fore.YELLOW}? {Style.RESET_ALL}{message}")

def success(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"{Fore.LIGHTBLACK_EX}{timestamp} {Fore.GREEN}+ {Style.RESET_ALL}{message}")

def error(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"{Fore.LIGHTBLACK_EX}{timestamp} {Fore.RED}! {Style.RESET_ALL}{message}")

def formatCookies(items: dict) -> str:
    cookies_text = str()
    for cookie in items: cookies_text += f'{cookie[0]}={cookie[1]}; '
    success('formatted the cookies successfully')
    return cookies_text[:len(cookies_text)-2]

proxy = open('proxies.txt','r',encoding='utf-8').read().splitlines()

os.system('cls' if os.name == 'nt' else 'clear')
set_console_window_size(90,25)

print(Colorate.Vertical(Colors.white_to_green, Center.XCenter("""
                                         
                    ██████████                             
                   ░███░░░░███                             
                   ░░░    ███   ███████  ██████  ████████  
                         ███   ███░░███ ███░░███░░███░░███ 
                        ███   ░███ ░███░███████  ░███ ░███ 
                       ███    ░███ ░███░███░░░   ░███ ░███ 
                      ███     ░░███████░░██████  ████ █████
                     ░░░       ░░░░░███ ░░░░░░  ░░░░ ░░░░░ 
                               ███ ░███                    
                              ░░██████                     
                               ░░░░░░                      
                                                                  
            ⌜―――――――――――――――――――――――――――――――――――――――――――――――――――――⌝
            ┇      [Github]  https://github.com/ItsYaBoiSimonx    ┇                                                                  
            ┇             guilded is very well made               ┇
            ⌞―――――――――――――――――――――――――――――――――――――――――――――――――――――⌟ 
                                                            
                                                            """, 2)))

preInvite = input(Fore.LIGHTGREEN_EX + "Enter invite link - ")
fullInv = preInvite.split('/i/')[1]
channelid = input(Fore.LIGHTGREEN_EX + "Enter channel ID - ")
message = input(Fore.LIGHTGREEN_EX + "Enter message - ")


def joinServer(session: httpx.Client, code):
   success('starting the joinServer function')
   session.headers['content-length'] = "19"
   
   r = session.put(url=f'https://www.guilded.gg/api/invites/{code}', data=json.dumps({"type":"consume"}))
   
   if r.status_code == 200:
       success("Invite code joined")
   else:
       warning('Joining server')

def spamMessages(session: httpx.Client, channnelID, message, name):
    while True:
        try:
            payload = {"messageId": str(uuid4()),"content":{"object":"value","document":{"object":"document","data":{},"nodes":[{"object":"block","type":"paragraph","data":{},"nodes":[{"object":"text","leaves":[{"object":"leaf","text":f"{message} | get botted lmfao","marks":[]}]}]}]}},"repliesToIds":[],"confirmed":False,"isSilent":False,"isPrivate":False}
            dumpedPayload = json.dumps(payload)
            session.headers['content-length'] = str(len(dumpedPayload))
            res = session.post(
                f"https://www.guilded.gg/api/channels/{channnelID}/messages",
                json=payload
            )
            success(f"Sent message as {name}")
            time.sleep(1)
        except Exception as e:
            error(str(e)) 
    
        
def create(invite):
    """

    Starts the creation process for the account.
    Uses HTTPX for the requests.
    PROXY SUPPORT IS NOT ADDED YET.

    """

    global proxy, message, channelid
    while True:
        email = generate_email()
        password = generate_password()
        proxytouse = random.choice(proxy)
        alphanumeric = string.ascii_letters + string.digits
        # proxyStruct = {
        #     "http://": f"http://{proxytouse}",
        #     "https://": f"http://{proxytouse}"
        # }

        # im too lazy to account for every proxy error so i just commented it out till i can manage.

        username = ''.join(random.choice(alphanumeric) for _ in range(10))
        session = httpx.Client()
        payload = {"extraInfo":{"platform":"desktop"},
                "name": username,
                "email": email,
                "password": password,
                "fullName": username,
        }

        try:
            r = session.post(url='https://www.guilded.gg/api/users?type=email', json=payload, timeout=3.5)
            success('Posted the login payload successfully')
        except Exception as e:
            error(f'ERROR! {e}')
        try:
            if "email" in r.text:
                with open('accounts.txt', 'a') as f:
                    f.write(f"{username}:{email}:{password}:{session.cookies['hmac_signed_session']}\n")
            else:
                error('Failed to generate account with email.')
                time.sleep(5)
        except Exception as e:
            error(e)

        if r.status_code == 200:
            id = r.json()['user']['id']
            success(f"{username} created")
            joinServer(session, invite)
            spamMessages(session, channelid, message, username)
            time.sleep(2)


num_threads = 7
threads = []

for i in range(num_threads):
    thread = threading.Thread(target=create, args=(fullInv,))
    threads.append(thread)
    thread.start()