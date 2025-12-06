import uvicorn
import os
import pathlib
from litellm.proxy.proxy_server import app as litellm_app, initialize as litellm_initialize
from fastapi.responses import FileResponse
from fastapi import HTTPException
import asyncio

@litellm_app.get("/logs")
def serve_logs():
    log_file = os.environ.get("LLM_PROXY_LOGGER_LOG_FILE")
    if not log_file:
        raise HTTPException(status_code=500, detail="LLM_PROXY_LOGGER_LOG_FILE environment variable not set")
    log_path = pathlib.Path(log_file)
    return FileResponse(str(log_path))

async def startup_event():
    await litellm_initialize(config='config.yaml')

if __name__ == "__main__":
    # Create log file if it doesn't exist
    log_file = os.environ.get("LLM_PROXY_LOGGER_LOG_FILE")
    if log_file:
        log_path = pathlib.Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.touch(exist_ok=True)
    
    asyncio.run(startup_event())
    
    uvicorn.run(litellm_app, host="0.0.0.0", port=4000, lifespan="on")