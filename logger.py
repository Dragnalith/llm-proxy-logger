import json
from datetime import datetime
import pathlib
import os

async def log_request(kwargs, response_obj, start_time, end_time):
    log_file = 'local/llm-proxy-logger.log'
    if not log_file:
        return
    log_path = pathlib.Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'a') as f:
        try:
            tool_calls = None
            if response_obj.choices[0].message.tool_calls:
                tool_calls = [t.model_dump() for t in response_obj.choices[0].message.tool_calls]
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'messages': kwargs.get('input'),
                'tools': kwargs.get('tools'),
                'response': {
                    'content': response_obj.choices[0].message.content,
                    'tool_calls': tool_calls
                }
            }
            f.write(json.dumps(log_entry, indent=2) + ',\n')
        except Exception as e:
            f.write(f"Logging error: {e}\n")
