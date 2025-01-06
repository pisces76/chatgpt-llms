from json import dumps
from time import time
from flask import request
from hashlib import sha256
from datetime import datetime
from requests import get
from requests import post 
from json     import loads
import os
import traceback

class Backend_Api:
    def __init__(self, app, config: dict) -> None:
        self.app = app
        self.api_key = os.getenv("OPENAI_API_KEY") or config['openai_key']
        self.api_base = os.getenv("OPENAI_API_BASE") or config['openai_api_base']
        self.proxy = config['proxy']
        self.config = config
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            }
        }

    def _conversation(self):
        try:
            config = self.config
            _conversation = request.json['meta']['content']['conversation']
            prompt = request.json['meta']['content']['parts'][0]
            current_date = datetime.now().strftime("%Y-%m-%d")

            m_idx = int(request.json['model'])
            self.api_key = config['models'][m_idx]['api_key']
            self.api_base = config['models'][m_idx]['api_base']
            self.model = config['models'][m_idx]['model']
            self.developer = config['models'][m_idx]['developer'] 

            system_message = f'You are a helpful AI assistant, a large language model trained by {self.developer}. Current date: {current_date}'
            extra = []

            conversation = [{'role': 'system', 'content': system_message}] + \
                            extra + _conversation + [prompt]        
            if self.developer == 'google':
                url = f"{self.api_base}/v1beta/chat/completions"
            else:
                url = f"{self.api_base}/v1/chat/completions"

            proxies = None
            if self.proxy['enable']:
                proxies = {
                    'http': self.proxy['http'],
                    'https': self.proxy['https'],
                }

            gpt_resp = post(
                url     = url,
                proxies = proxies,
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer %s' % self.api_key
                }, 
                json    = {
                    'model'             : self.model, 
                    'messages'          : conversation,
                    'stream'            : True
                },
                stream  = True
            )

            if gpt_resp.status_code >= 400:
                error_data =gpt_resp.json().get('error', {})
                error_code = error_data.get('code', None)
                error_message = error_data.get('message', "An error occurred")
                return {
                    'successs': False,
                    'error_code': error_code,
                    'message': error_message,
                    'status_code': gpt_resp.status_code
                }, gpt_resp.status_code

            def stream():
                for chunk in gpt_resp.iter_lines():
                    try:
                        if len(chunk) == 0: #avoid empty lines
                            continue

                        if chunk.decode("utf-8") == 'data: [DONE]': #last line
                            break

                        decoded_line = loads(chunk.decode("utf-8").split("data: ")[1])
                        token = decoded_line["choices"][0]['delta'].get('content')
                        if token is not None and token: 
                            yield token
                            
                    except GeneratorExit:
                        break

                    except Exception as e:
                        print(e)
                        print(e.__traceback__.tb_next)
                        traceback.print_exc()
                        continue
                        
            return self.app.response_class(stream(), mimetype='text/event-stream')

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return {
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"}, 400
