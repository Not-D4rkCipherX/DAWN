import asyncio
import logging
import warnings
import random
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Set
from curl_cffi import requests
from colorama import Fore, Style, init

init(autoreset=True)
warnings.simplefilter('ignore')

class Colors:
    SUCCESS = f"{Fore.GREEN}"
    ERROR = f"{Fore.RED}"
    INFO = f"{Fore.CYAN}"
    WARNING = f"{Fore.YELLOW}"
    RESULT = f"{Fore.LIGHTMAGENTA_EX}"
    RESET = f"{Style.RESET_ALL}"

class DawnValidatorBot:
    API_URLS = {
        "keepalive": "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive",
        "getPoints": "https://www.aeropres.in/api/atom/v1/userreferral/getpoint",
        "socialmedia": "https://www.aeropres.in/chromeapi/dawn/v1/profile/update"
    }
    
    EXTENSION_ID = "fpdkjdnhkakefebpekbdhillbhonfjjp"
    VERSION = "1.1.2"
    APP_ID_PREFIX = "6769d"
    SOCIAL_TYPES = ["twitter_x_id", "discordid", "telegramid"]

    def __init__(self):
        self.verified_accounts: Set[str] = set()
        self.proxies: List[str] = []
        self.used_proxies: Dict[str, str] = {}
        self.app_ids: Dict[str, str] = {}
        self.proxy_failures: Dict[str, int] = {}
        self.max_proxy_failures = 3
        self.sessions: Dict[str, requests.Session] = {}
        self.base_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site"
        }

    def get_base_headers(self, token: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Origin": f"chrome-extension://{self.EXTENSION_ID}"
        }

    def generate_app_id(self, token: str) -> str:
        return f"{self.APP_ID_PREFIX}{hashlib.md5(token.encode()).hexdigest()[:19]}"

    def get_app_id(self, email: str, token: str) -> str:
        if email not in self.app_ids:
            self.app_ids[email] = self.generate_app_id(token)
        return self.app_ids[email]

    @staticmethod
    def log(message: str, color: str = Colors.INFO, level: str = "INFO") -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {color}{message}{Colors.RESET}")

    def load_proxies(self) -> None:
        try:
            with open('proxies.txt', 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            if self.proxies:
                self.log(f"✓ Loaded {len(self.proxies)} proxies", Colors.SUCCESS)
            else:
                self.log("No proxies found in proxies.txt", Colors.WARNING)
        except FileNotFoundError:
            self.log("proxies.txt not found", Colors.WARNING)

    def format_proxy(self, proxy: str) -> Dict[str, str]:
        if ':' not in proxy:
            return {}

        if proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
            protocol = proxy.split('://')[0]
            proxy_str = proxy
        else:
            parts = proxy.split(':')
            if len(parts) == 2:
                protocol = 'http'
                proxy_str = f"{protocol}://{proxy}"
            elif len(parts) == 4:
                protocol = 'http'
                ip, port, user, pwd = parts
                proxy_str = f"{protocol}://{user}:{pwd}@{ip}:{port}"
            else:
                return {}

        return {protocol: proxy_str}

    def assign_proxy(self, email: str) -> Optional[Dict[str, str]]:
        if email in self.used_proxies:
            return self.format_proxy(self.used_proxies[email])
            
        available_proxies = [p for p in self.proxies if p not in self.used_proxies.values()]
        if not available_proxies:
            self.used_proxies.clear()
            available_proxies = self.proxies
            
        if available_proxies:
            proxy = random.choice(available_proxies)
            self.used_proxies[email] = proxy
            return self.format_proxy(proxy)
        return None

    def get_session(self, email: str) -> requests.Session:
        if email not in self.sessions:
            session = requests.Session()
            session.headers.update(self.base_headers)
            session.impersonate = "chrome110"
            session.timeout = 30
            self.sessions[email] = session
        return self.sessions[email]

    async def make_request(self, email: str, method: str, url: str, headers: Dict, **kwargs) -> requests.Response:
        max_retries = 3
        current_try = 0
        session = self.get_session(email)
        
        while current_try < max_retries:
            try:
                proxy = self.assign_proxy(email)
                session.headers.update(headers)
                
                if proxy:
                    session.proxies = proxy
                
                if method.upper() == 'GET':
                    response = session.get(url, **kwargs)
                else:
                    response = session.post(url, **kwargs)
                
                if response.status_code != 200:
                    raise Exception(f"HTTP {response.status_code}")
                
                return response
                
            except Exception as e:
                current_try += 1
                if current_try >= max_retries:
                    raise
                await asyncio.sleep(1)

    async def fetch_points(self, email: str, headers: Dict[str, str], app_id: str) -> int:
        try:
            response = await self.make_request(
                email=email,
                method='GET',
                url=f"{self.API_URLS['getPoints']}?appid={app_id}",
                headers=headers
            )
            
            data = response.json()
            if not data.get('status'):
                raise ValueError(data.get('message', 'Unknown error'))

            points_data = data.get('data', {})
            reward = points_data.get('rewardPoint', {})
            referral = points_data.get('referralPoint', {})
            
            return sum([
                reward.get('points', 0),
                reward.get('registerpoints', 0),
                reward.get('signinpoints', 0),
                reward.get('twitter_x_id_points', 0),
                reward.get('discordid_points', 0),
                reward.get('telegramid_points', 0),
                reward.get('bonus_points', 0),
                referral.get('commission', 0)
            ])

        except Exception as e:
            self.log(f"Failed to fetch points for {email}: {str(e)}", Colors.ERROR)
            return 0

    async def keep_alive_request(self, email: str, headers: Dict[str, str], app_id: str) -> bool:
        try:
            await self.make_request(
                email=email,
                method='POST',
                url=f"{self.API_URLS['keepalive']}?appid={app_id}",
                headers=headers,
                json={
                    "username": email,
                    "extensionid": self.EXTENSION_ID,
                    "numberoftabs": 0,
                    "_v": self.VERSION
                }
            )
            return True
        except Exception:
            return False

    async def verify_social_media(self, account: Dict[str, str], app_id: str) -> Dict[str, bool]:
        email = account['email']
        if email in self.verified_accounts:
            return {social: True for social in self.SOCIAL_TYPES}
            
        headers = self.get_base_headers(account['token'])
        results = {}
        
        for social_type in self.SOCIAL_TYPES:
            try:
                response = await self.make_request(
                    email=email,
                    method='POST',
                    url=f"{self.API_URLS['socialmedia']}?appid={app_id}",
                    headers=headers,
                    json={social_type: social_type}
                )
                
                results[social_type] = response.json().get('success', False)
                await asyncio.sleep(random.randint(1, 2))
                
            except Exception:
                results[social_type] = False
        
        if all(results.values()):
            self.verified_accounts.add(email)
            
        return results

    @staticmethod
    def _get_single_account() -> List[Dict[str, str]]:
        while True:
            email = input(f"{Colors.INFO}Email: {Colors.RESET}").strip()
            if not email:
                print(f"{Colors.ERROR}Email cannot be empty{Colors.RESET}")
                continue
            
            token = input(f"{Colors.INFO}Token: {Colors.RESET}").strip()
            if not token:
                print(f"{Colors.ERROR}Token cannot be empty{Colors.RESET}")
                continue
                
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{Colors.SUCCESS} ✓ Account details saved{Colors.RESET}")
            return [{'email': email, 'token': token}]

    @staticmethod
    def _load_accounts_from_file() -> List[Dict[str, str]]:
        try:
            accounts = []
            with open('accounts.txt', 'r') as f:
                for line in f:
                    if ':' not in line:
                        continue
                    email, token = line.strip().split(':')
                    if email and token:
                        accounts.append({'email': email.strip(), 'token': token.strip()})
        
            if not accounts:
                raise ValueError("No valid accounts found in accounts.txt")
        
            print(f"{Colors.SUCCESS}✓ Loaded {len(accounts)} accounts{Colors.RESET}")
            return accounts
        except FileNotFoundError:
            print(f"{Colors.ERROR}accounts.txt not found{Colors.RESET}")
            return []
        except Exception as e:
            print(f"{Colors.ERROR}Error loading accounts: {str(e)}{Colors.RESET}")
            return []

    @staticmethod
    def load_accounts(mode: str) -> List[Dict[str, str]]:
        return DawnValidatorBot._get_single_account() if mode == "1" else DawnValidatorBot._load_accounts_from_file()

    @staticmethod
    def display_welcome() -> None:
        print(f"""
{Colors.INFO}{Style.BRIGHT}
D4rkCipherX - DAWN BOT                {Colors.RESET}
""")

    async def process_account(self, account: Dict[str, str]) -> Dict:
        email = account['email']
        token = account['token']
        headers = self.get_base_headers(token)
        app_id = self.get_app_id(email, token)
        
        self.log(f"Processing: {email}", Colors.INFO)
        points = await self.fetch_points(email, headers, app_id)
        social_results = await self.verify_social_media(account, app_id)
        verified_count = sum(1 for status in social_results.values() if status)
        keepalive_status = await self.keep_alive_request(email, headers, app_id)
        current_proxy = self.used_proxies.get(email, "No proxy")
        
        return {
            'email': email,
            'points': points,
            'social_verified': f"{verified_count}/{len(self.SOCIAL_TYPES)}",
            'keepalive': keepalive_status,
            'proxy': current_proxy,
            'app_id': app_id
        }

    @staticmethod
    async def countdown(seconds: int) -> None:
        for remaining in range(seconds, 0, -1):
            print(f"\r[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{Colors.WARNING}⏳ Next cycle in {remaining}s{Colors.RESET}", end='')
            await asyncio.sleep(1)
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{Colors.INFO}✓ Starting new cycle, Please wait...{Colors.RESET}\n")

async def main():
    bot = DawnValidatorBot()
    bot.display_welcome()
    
    print(f"{Colors.INFO}Select mode:{Colors.RESET}")
    print("1. Single Account")
    print("2. Multiple Accounts [from accounts.txt]")
    
    while True:
        mode = input(f"{Colors.WARNING}Choice (1/2): {Colors.RESET}")
        if mode in ['1', '2']:
            break
        print(f"{Colors.ERROR}Invalid choice. Enter 1 or 2.{Colors.RESET}")
    
    accounts = bot.load_accounts(mode)
    if not accounts:
        bot.log("No accounts available. Exiting...", Colors.ERROR)
        return

    bot.load_proxies()

    try:
        while True:
            bot.log("Starting new process, Please wait...", Colors.INFO)
            results = await asyncio.gather(*[bot.process_account(account) for account in accounts])
            
            print("\n" + "═" * 70)
            print(f"{Colors.INFO}Process Summary:{Colors.RESET}")
            for result in results:
                color = Colors.SUCCESS if result['keepalive'] else Colors.ERROR
                status = "✓" if result['keepalive'] else "✗"
                print(f"{Colors.SUCCESS}[✓] Account: {Colors.RESET}{Colors.RESULT}{result['email']}{Colors.RESET}")
                print(f"{Colors.SUCCESS}[✓] Points: {Colors.RESET}{Colors.RESULT}{result['points']}{Colors.RESET}")
                print(f"{Colors.SUCCESS}[✓] Social: {Colors.RESET}{Colors.RESULT}{result['social_verified']} verified{Colors.RESET}")
                print(f"{color}[{status}] Keepalive: {'Active' if result['keepalive'] else 'Failed'}{Colors.RESET}")
                print(f"{Colors.SUCCESS}[✓] Proxy: {Colors.RESET}{Colors.RESULT}{result['proxy']}{Colors.RESET}")
                print(f"{Colors.SUCCESS}[✓] App ID: {Colors.RESET}{Colors.RESULT}{result['app_id']}{Colors.RESET}")
            print("═" * 70 + "\n")
            
            await bot.countdown(500)

    except KeyboardInterrupt:
        bot.log("Process interrupted by user", Colors.WARNING)
    except Exception as e:
        bot.log(f"Fatal error: {str(e)}", Colors.ERROR)

if __name__ == "__main__":
    asyncio.run(main())
