# Dawn Validator BOT
Dawn Validator BOT

- Download Extension Here : [Dawn Validator](https://chromewebstore.google.com/detail/dawn-validator-chrome-ext/fpdkjdnhkakefebpekbdhillbhonfjjp?hl=en)
- Use Code : 24kysvyf

## Features

  - Auto Get Account Information
  - Auto Run With [Monosans](https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt) Proxy - Choose 1
  - Auto Run With Private Proxy - Choose 2
  - Auto Run Without Proxy - Choose 3
  - Auto Send Keep-Alive Every 5 Minutes
  - Multi Accounts With Threads

Note: Dawn Server may be experiencing problems receiving requests, please be patient.

## Requiremnets

- Make sure you have Python3.9 or higher installed and pip.

## Instalation

1. **Clone The Repositories:**
   ```bash
   git clone https://github.com/Not-D4rkCipherX/DAWN.git
   cd DAWN
   pip install -r requirements.txt
   ```

## Getting Token
- Open ``chrome-extension://fpdkjdnhkakefebpekbdhillbhonfjjp/dashboard.html`` in your browser and login
- Press F12 or CTRL+SHIFT+I and Select Network
- Look for ``getpoint?appid=``
- Open request headers and copy the token. Bearer ``a1b2c3d4ef5g`` < your token
![image](https://github.com/user-attachments/assets/2cf7d088-8ecb-4925-a470-5b398cb88e1f)
- Insert your account details in ``accounts.txt``, with each line in the format ``email:token`` for each account, like:
  ```bash
  [
      {
          "Email": "your_email_address 1",
          "Token": "your_berear_token 1"
      },
      {
          "Email": "your_email_address 2",
          "Token": "your_berear_token 2"
      }
  ]
  ```
## PROXY (OPTINAL)
- Make sure `proxy.txt` contains data that matches the format expected by the script. Here are examples of file formats:
  ```bash
    ip:port # Default Protcol HTTP.
    protocol://ip:port
    protocol://user:pass@ip:port
  ```

## Run the BOT

```bash
python bot.py #or python3 bot.py
```

## Buy Me a Coffee

- **EVM:** 0x47f41Fcb17cF9B7A02C26EE855d26bB8D3928E1b
- **TON:** UQA-qG5eyQ7gVxvPDpy484xzc0UPS9a8hJsUAwe0T_3D7_oF
- **SOL:** A1pUv13rRDtubtYJuXswZYSQBJojPhthXJftfNZBRnEX
- **SUI:** 0xeb697918d66c4ade867d61d0b8fb541df83675e8f60b6b81da8917aab149ee8f