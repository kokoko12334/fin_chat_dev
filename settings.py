import os
from dotenv import load_dotenv
from typing import Optional
load_dotenv(override=True)
# print(os.getenv("DATABASE_USERNAME"))
class Settings:
	
    ENVIRONMENT : str = os.getenv("ENVIRONMENT", "dev")

    OPENAI_API_KEY : str = os.getenv("OPENAI_API_KEY")
    IEX_API_KEY : str = os.getenv("IEX_API_KEY")
    PINECONE_API : str = os.getenv("PINECONE_API")
    FINNHUB_API_KEY: str = os.getenv("FINNHUB_API_KEY")
    
    DATABASE_USERNAME : str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST : str = os.getenv("DATABASE_HOST","localhost")
    DATABASE_PORT : int = int(os.getenv("DATABASE_PORT"))
    DATABASE_NAME : str = os.getenv("DATABASE_NAME")
     
    DATABASE_URL = str = os.getenv('DATABASE_URL')
    
    SSH_HOST : str = os.getenv("SSH_HOST")
    SSH_PORT : int = int(os.getenv("SSH_PORT", '0'))
    SSH_USER : str = os.getenv("SSH_USER")
    SSH_PASSWORD : str = os.getenv("SSH_PASSWORD")
    
    @property
    def need_ssh(self) -> bool:
        return all(
            [
                self.SSH_HOST,
                self.SSH_PORT,
                self.SSH_USER,
                self.SSH_PASSWORD
            ]
        )
settings = Settings()
# print(settings.DATABASE_URL)