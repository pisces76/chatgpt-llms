# chatgpt-llms

[![English badge](https://img.shields.io/badge/%E8%8B%B1%E6%96%87-English-blue)](./README.md)
[![简体中文 badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-Simplified%20Chinese-blue)](./README_CN.md)

A simple web chat application supporting popular LLM API interfaces.

Based on @xtekky's [chatgpt-clone](https://github.com/xtekky/chatgpt-clone) project, this project aims to provide a unified web platform for easily switching between different LLM models, such as LLaMa-3, DeepSeek, ChatGPT, Mixtral, Gemma etc. You can easily add more LLM API models by modifying config.json.

<img width="1470" src="./llm-demo.png" alt="Preview"/>

You can also visit https://miaomiao88.top for a demo.

## Installation

- Clone this project:
```
git clone https://github.com/pisces76/chatgpt-llms.git; cd chatgpt-llms
```
- Create a virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Configuration
- Copy config.json.example to config.json
- Modify the models section in config.json with your correct API KEY, for example:
```
    "models": [
        {
          "llm_name": "deepseek",
          "api_key": "sk-xxxx",
          "api_base": "https://api.deepseek.com",
          "model": "deepseek-chat",
          "developer": "DEEPSEEK"
        },
        ...
    ]
```
- You can add more models in config.json

## Running

- For testing, use Python Flask:
```
python run.py
```

- For production, running start.sh script to startup gunicorn:
```
./start.sh &
```

- Now you can visit http://ip:8080 for a chat. 

## Donations
This is my first Github code project. If you find this project useful and would like to support it, please consider making a donation. Your support will help to ensure the continuity and development of the project.

### WeChat Pay
<img width="180" src="https://raw.githubusercontent.com/pisces76/pisces76/master/wechat-QR.jpg">

### Alipay
<img width="180" src="https://raw.githubusercontent.com/pisces76/pisces76/master/alipay-QR.jpg">

### Paypal
[![PayPal badge](https://img.shields.io/badge/PayPal_Link-003087)](https://paypal.me/miaomiao38?country.x=C2&locale.x=en_US) 