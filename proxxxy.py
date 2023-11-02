import signal
import os
import random
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style

def clear_console():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

def check_proxy(proxy, user_agent, proxy_type):
    try:
        headers = {'User-Agent': user_agent}
        response = requests.get('http://google.com', proxies={'http': proxy, 'https': proxy}, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"{Fore.GREEN}{proxy} SI funciona correctamente{Style.RESET_ALL}")
            with open(os.path.join('CHECKED_PROXY', f"CHECKED{proxy_type.upper()}.txt"), 'a') as file:
                file.write(proxy + '\n')
        else:
            print(f"{Fore.RED}{proxy} NO funciona correctamente{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}{proxy} NO funciona correctamente. Excepción: {e}{Style.RESET_ALL}")

def read_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
        return proxies

def read_user_agents(file_path):
    with open(file_path, 'r') as file:
        user_agents = file.read().splitlines()
        return user_agents

def proxy_sources():
    return {
        "HTTP": [
        "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
        "https://raw.githubusercontent.com/casals-ar/proxy-list/main/http",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/lkx1331anon/proxy-list/main/http_worldwide.txt",
        ],
        "SOCKS4": [
        "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks4",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
        ],
        "SOCKS5": [
        "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks5",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
        "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks5",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
        ],
    }

def main_menu():
    print("""
██████  ██████   ██████  ██   ██ ██    ██      ██████      ██ 
██   ██ ██   ██ ██    ██  ██ ██   ██  ██      ██  ████    ███ 
██████  ██████  ██    ██   ███     ████       ██ ██ ██     ██ 
██      ██   ██ ██    ██  ██ ██     ██        ████  ██     ██ 
██      ██   ██  ██████  ██   ██    ██         ██████  ██  ██
    
    Version 1.0
    
    Creador: https://www.nodo313.net/miembros/0-1.80264/
    """)
    print("========================================")
    print("   B I E N V E N I D O  A  P R O X X X Y")
    print("========================================")
    print("           Seleccione una opción:       ")
    print("========================================")
    print("1. Verificar Proxies")
    print("2. Extraer Proxies")
    print("3. Salir")
    print("========================================")

def verify_proxies_menu():
    print("1. Verificar proxies HTTP")
    print("2. Verificar proxies SOCKS4")
    print("3. Verificar proxies SOCKS5")
    choice = input("Por favor, seleccione el tipo de proxies que desea verificar: ")
    return choice

def execute_checker():
    try:
        while True:
            proxy_type_choice = verify_proxies_menu()
            folder_path = 'doctxt/'
            user_agents = read_user_agents(os.path.join(folder_path, 'user-agents.txt'))

            if proxy_type_choice == '1':
                proxy_type = 'http'
            elif proxy_type_choice == '2':
                proxy_type = 'socks4'
            elif proxy_type_choice == '3':
                proxy_type = 'socks5'
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")
                continue

            file_path = os.path.join(folder_path, f'{proxy_type}.txt')
            if os.path.exists(file_path):
                proxies = read_proxies(file_path)
                with ThreadPoolExecutor(max_workers=30) as executor:
                    for proxy in proxies:
                        user_agent = random.choice(user_agents)
                        executor.submit(check_proxy, proxy, user_agent, proxy_type.upper())
            else:
                print(f'No se encontró el archivo {proxy_type}.txt en la carpeta doctxt.')
    except Exception as e:
        print(f"Error al ejecutar el verificador: {e}")

def extract_proxies(source_list, limit_per_source=5000, total_limit=10000):
    proxies = set()
    total_proxies = 0

    for proxy_type, sources in source_list.items():
        file_path = os.path.join('doctxt', f"{proxy_type.upper()}.txt")
        for source in sources:
            response = requests.get(source, stream=True)
            if response.status_code == 200:
                extracted_proxies = response.iter_lines(decode_unicode=True)
                with tqdm(total=limit_per_source, desc=f"Extrayendo proxies de {proxy_type}", unit='proxy') as pbar:
                    for proxy in extracted_proxies:
                        if total_proxies < total_limit and proxy not in proxies:
                            with open(file_path, 'a') as file:
                                file.write(proxy + '\n')
                            proxies.add(proxy)
                            total_proxies += 1
                            pbar.update(1)
                            if total_proxies % limit_per_source == 0:
                                break
                print(f"Proxies de tipo {proxy_type} extraídos con éxito desde {source}")
            else:
                print(f"No se pudo extraer proxies de tipo {proxy_type} desde {source}")

        if total_proxies >= total_limit:
            break
    clear_console()

if __name__ == '__main__':
    while True:
        main_menu()
        choice = input("Ingrese su elección: ")

        if choice == '1':
            execute_checker()
        elif choice == '2':
            sources = proxy_sources()
            print("¿Qué quieres extraer?")
            print("1) HTTP")
            print("2) SOCKS4")
            print("3) SOCKS5")
            format_choice = input("Ingrese su elección: ")
            if format_choice == '1':
                extract_proxies({ "HTTP": sources["HTTP"] })
            elif format_choice == '2':
                extract_proxies({ "SOCKS4": sources["SOCKS4"] })
            elif format_choice == '3':
                extract_proxies({ "SOCKS5": sources["SOCKS5"] })
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")
        elif choice == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")