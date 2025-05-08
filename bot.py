import requests
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, os, pytz, uuid

wib = pytz.timezone('Asia/Jakarta')

class Dawn:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://fpdkjdnhkakefebpekbdhillbhonfjjp",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": FakeUserAgent().random
        }
        self.BASE_API = "https://ext-api.dawninternet.com"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}╭─[{datetime.now().astimezone(wib).strftime('%x %X %Z')}]{Style.RESET_ALL}\n"
            f"{Fore.CYAN + Style.BRIGHT}╰──▶{Style.RESET_ALL} {message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""{Fore.BLUE + Style.BRIGHT}
   ██████╗  █████╗ ██╗    ██╗███╗   ██╗
   ██╔══██╗██╔══██╗██║    ██║████╗  ██║
   ██║  ██║███████║██║ █╗ ██║██╔██╗ ██║
   ██║  ██║██╔══██║██║███╗██║██║╚██╗██║
   ██████╔╝██║  ██║╚███╔███╔╝██║ ╚████║
   ╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝
            {Fore.GREEN + Style.BRIGHT}AUTO PING BOT{Style.RESET_ALL}
            {Fore.YELLOW + Style.BRIGHT}https://t.me/D4rkCipherX{Style.RESET_ALL}
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}✗ File {filename} not found{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                response = requests.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt")
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}✗ File {filename} not found{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}✗ No proxies found{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}✓ Proxies loaded: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}✗ Proxy load failed: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, email):
        if email not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[email] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[email]

    def rotate_proxy_for_account(self, email):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[email] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
            
    def generate_app_id(self):
        prefix = "67"
        app_id = prefix + uuid.uuid4().hex[len(prefix):]
        return app_id
    
    def mask_account(self, account):
        if "@" in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"
        
        mask_account = account[:3] + '*' * 3 + account[-3:]
        return mask_account
    
    def print_message(self, email, proxy, color, message):
        self.log(
            f"{Fore.MAGENTA + Style.BRIGHT}Account:{Style.RESET_ALL} "
            f"{Fore.CYAN + Style.BRIGHT}{self.mask_account(email)}{Style.RESET_ALL} | "
            f"{Fore.MAGENTA + Style.BRIGHT}Proxy:{Style.RESET_ALL} "
            f"{Fore.CYAN + Style.BRIGHT}{proxy if proxy else 'No Proxy'}{Style.RESET_ALL}\n"
            f"{Fore.MAGENTA + Style.BRIGHT}Status:{Style.RESET_ALL} "
            f"{color + Style.BRIGHT}{message}{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print(f"{Fore.YELLOW + Style.BRIGHT}Proxy Options:{Style.RESET_ALL}")
                print(f"{Fore.GREEN + Style.BRIGHT}1. {Fore.CYAN}Use Monosans Proxy{Style.RESET_ALL}")
                print(f"{Fore.GREEN + Style.BRIGHT}2. {Fore.CYAN}Use Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.GREEN + Style.BRIGHT}3. {Fore.CYAN}No Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.YELLOW + Style.BRIGHT}Select option [1/2/3]: {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Monosans Proxy" if choose == 1 else 
                        "Private Proxy" if choose == 2 else 
                        "No Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}✓ Selected: {proxy_type}{Style.RESET_ALL}")
                    return choose
                else:
                    print(f"{Fore.RED + Style.BRIGHT}✗ Invalid option. Choose 1, 2 or 3{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}✗ Invalid input. Enter a number{Style.RESET_ALL}")

    async def user_data(self, app_id: str, email: str, token: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/api/atom/v1/userreferral/getpoint?appid={app_id}"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        for attempt in range(retries):
            try:
                response = requests.get(url=url, headers=headers, proxies={"http": proxy, "https": proxy} if proxy else None, timeout=120)
                response.raise_for_status()
                result = response.json()
                return result["data"]
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return self.print_message(email, proxy, Fore.YELLOW, f"✗ Failed to get data: {str(e)}")

    async def send_keepalive(self, app_id: str, email: str, token: str, use_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/chromeapi/dawn/v1/userreward/keepalive?appid={app_id}"
        data = json.dumps({"username":email, "extensionid":"fpdkjdnhkakefebpekbdhillbhonfjjp", "numberoftabs":0, "_v":"1.1.6"})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
        }

        for attempt in range(retries):
            try:
                response = requests.post(url=url, headers=headers, data=data, proxies={"http": proxy, "https": proxy} if proxy else None, timeout=120)
                response.raise_for_status()
                result = response.json()
                return result["data"]
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(email, proxy, Fore.RED, f"✗ Ping failed: {str(e)}")
                proxy = self.rotate_proxy_for_account(email) if use_proxy else None
                return None
            
    async def process_user_earning(self, app_id: str, email: str, token: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None
            user = await self.user_data(app_id, email, token, proxy)
            if user:
                referral_point = user.get("referralPoint", {}).get("commission", 0)
                reward_point = user.get("rewardPoint", {})
                reward_points = sum(
                    value for key, value in reward_point.items()
                    if "points" in key.lower() and isinstance(value, (int, float))
                )

                total_points = referral_point + reward_points
                self.print_message(email, proxy, Fore.GREEN, f"✓ Earning: {total_points:.0f} PTS")

            await asyncio.sleep(10 * 60)    

    async def process_send_keepalive(self, app_id: str, email: str, token: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None
            print(
                f"{Fore.CYAN + Style.BRIGHT}╭─[{datetime.now().astimezone(wib).strftime('%x %X %Z')}]{Style.RESET_ALL}\n"
                f"{Fore.CYAN + Style.BRIGHT}╰──▶{Style.RESET_ALL} {Fore.BLUE + Style.BRIGHT}Sending ping...{Style.RESET_ALL}",
                end="\r",
                flush=True
            )

            keepalive = await self.send_keepalive(app_id, email, token, use_proxy, proxy)
            if keepalive and keepalive.get("success"):
                server_name = keepalive.get("servername", "N/A")
                self.print_message(email, proxy, Fore.GREEN, f"✓ Ping successful | Server: {server_name}")

            print(
                f"{Fore.CYAN + Style.BRIGHT}╭─[{datetime.now().astimezone(wib).strftime('%x %X %Z')}]{Style.RESET_ALL}\n"
                f"{Fore.CYAN + Style.BRIGHT}╰──▶{Style.RESET_ALL} {Fore.BLUE + Style.BRIGHT}Waiting 10 minutes for next ping...{Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            await asyncio.sleep(10 * 60)
        
    async def process_accounts(self, app_id: str, email: str, token: str, use_proxy: bool):
        tasks = [
            asyncio.create_task(self.process_user_earning(app_id, email, token, use_proxy)),
            asyncio.create_task(self.process_send_keepalive(app_id, email, token, use_proxy))
        ]
        await asyncio.gather(*tasks)
    
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED + Style.BRIGHT}✗ No accounts loaded{Style.RESET_ALL}")
                return
            
            use_proxy_choice = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}✓ Accounts loaded: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}━{Style.RESET_ALL}"*50)

            while True:
                tasks = []
                for account in accounts:
                    app_id = self.generate_app_id()
                    email = account.get('Email')
                    token = account.get('Token')

                    if app_id and "@" in email and token:
                        tasks.append(asyncio.create_task(self.process_accounts(app_id, email, token, use_proxy)))

                await asyncio.gather(*tasks)
                await asyncio.sleep(10)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}✗ Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = Dawn()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}╭─[{datetime.now().astimezone(wib).strftime('%x %X %Z')}]{Style.RESET_ALL}\n"
            f"{Fore.CYAN + Style.BRIGHT}╰──▶{Style.RESET_ALL} {Fore.RED + Style.BRIGHT}✗ Bot stopped by user{Style.RESET_ALL}"
        )
