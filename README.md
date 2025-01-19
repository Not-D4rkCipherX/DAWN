# Dawn Validator Bot
Automation farming Script for Dawn Validator using proxies. This bot support multi accounts.
## Tools and components required
1. Dawn Validator Account | Download [Dawn Validator Extension](https://chromewebstore.google.com/detail/dawn-validator-chrome-ext/fpdkjdnhkakefebpekbdhillbhonfjjp)
2. Open ``chrome-extension://fpdkjdnhkakefebpekbdhillbhonfjjp/pages/signup.html``, insert Referral code ``24kysvyf`` and Register
3. Proxies (OPTIONAL)
4. VPS or RDP (OPTIONAL)
5. Python version 3.10 or Latest
### Buy Proxies
- Free Proxies Static Residental: 
1. [WebShare](https://www.webshare.io/?referral_code=p7k7whpdu2jg)
2. [ProxyScrape](https://proxyscrape.com/?ref=odk1mmj)
3. [MonoSans](https://github.com/monosans/proxy-list)
- Paid Premium Static Residental:
1. [922proxy](https://www.922proxy.com/register?inviter_code=d03d4fed)
2. [Proxy-Cheap](https://app.proxy-cheap.com/r/JysUiH)
3. [Infatica](https://dashboard.infatica.io/aff.php?aff=544)
## Getting Token
- Open ``chrome-extension://fpdkjdnhkakefebpekbdhillbhonfjjp/dashboard.html`` in your browser and login
- Press F12 or CTRL+SHIFT+I and Select Network
- Look for ``getpoint?appid=``
- Open request headers and copy the token. Bearer ``a1b2c3d4ef5g`` < your token
![image](https://github.com/user-attachments/assets/2cf7d088-8ecb-4925-a470-5b398cb88e1f)
- Insert your account details in ``accounts.txt``, with each line in the format ``email:token`` for each account, like:
```bash
email:token
email:token
email:token
```
# Installation
- Install Python For Windows: [Python](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)
- For Unix: ``apt install python3 python3-pip -y``
- Install requirements, Windows:
```bash
pip install -r requirements.txt
```
- Unix:
```bash
pip3 install -r requirements.txt
```
### Run the Bot
- Replace the proxies example in ```proxies.txt``` to your own proxies
#### Run for single account
- Windows:
```bash
python main.py
```
- Unix
```bash
python3 main.py
```
- Select: 1
- Then insert your email and token
#### Run for multi accounts
- Windows:
```bash
python main.py
```
- Unix
```bash
python3 main.py
```
- Select: 2
# Notes
- Run this bot, and it will update your referrer code to my invite code if you don't have one.
- This bot have delay every 500 seconds. 
- You can just run this bot at your own risk, I'm not responsible for any loss or damage caused by this bot. This bot is for educational purposes only.
