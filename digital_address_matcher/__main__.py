import uvicorn
from digital_address_matcher.config.config import get_config

if __name__ == '__main__':
    settings = get_config()
    uvicorn.run(
       'digital_address_matcher.main:app',
        host=settings.api_settings.host,
        port=settings.api_settings.port,
        reload=True,
    )
