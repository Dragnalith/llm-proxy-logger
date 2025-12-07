import uvicorn
import os
import pathlib
from litellm.proxy.proxy_server import app as litellm_app, initialize as litellm_initialize
from fastapi.responses import FileResponse
from fastapi import HTTPException
import asyncio

@litellm_app.get("/logs")
def serve_logs():
    log_file = 'local/llm-proxy-logger.log'
    if not log_file:
        raise HTTPException(status_code=500, detail="LLM_PROXY_LOGGER_LOG_FILE environment variable not set")
    log_path = pathlib.Path(log_file)
    return FileResponse(str(log_path))

async def startup_event():
    await litellm_initialize(config='config.yaml')

def check_required_env_vars():
    """Check that all required environment variables are set."""
    required_vars = [
        "OPENAI_API_KEY",
        "LITELLM_MASTER_KEY"
    ]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

if __name__ == "__main__":
    # Check required environment variables
    check_required_env_vars()
    
    # Create log file if it doesn't exist
    log_file = 'local/llm-proxy-logger.log'
    if log_file:
        log_path = pathlib.Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.touch(exist_ok=True)
    
    asyncio.run(startup_event())
    
    uvicorn.run(litellm_app, host="0.0.0.0", port=4000, lifespan="on")