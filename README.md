# Railway Deployment

Create a railway account on https://railway.com.

Then you can deploy with the following command

```bash
railway login   # login for cli
railway init    # Create a railway project
railway add     # Create a service. When prompted set OPENAI_API_KEY, LITELLM_MASTER_KEY, and PORT variables
railway domain  # Create a ***.up.railway.app domain for the service
railway up      # Deploy
```

When running `railway add`, Railway will prompt you to set environment variables. Set:
- `OPENAI_API_KEY` - Your OpenRouter API key
- `LITELLM_MASTER_KEY` - Key used by your client for authentication
- `PORT` - Set to `4000`
