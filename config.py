from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    

    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
    API_KEY = os.getenv("GEMINI_API_KEY") 
    APP_NAME = os.getenv("APP_NAME", "QuizzAI")
    
  
    HOST = "127.0.0.1"  
    PORT = 8080
    
  
    MAX_PDF_SIZE = int(os.getenv("MAX_PDF_SIZE", 10 * 1024 * 1024))  # 10MB default
    
    @classmethod
    def is_dev(cls):
        
        return cls.ENVIRONMENT == "dev"
    
    @classmethod
    def validate(cls):
       
        print("=" * 50)
        print("🚀 QuizzAI Configuration")
        print("=" * 50)
        print(f"📦 App Name:      {cls.APP_NAME}")
        print(f"🌍 Environment:   {cls.ENVIRONMENT}")
        print(f"🏠 Host:          {cls.HOST}")
        print(f"🔌 Port:          {cls.PORT}")
        print(f"📄 Max PDF Size:  {cls.MAX_PDF_SIZE / (1024*1024):.1f} MB")
        print(f"🔑 API Key Set:   {'✅ Yes' if cls.API_KEY else '❌ No (WILL FAIL!)'}")
        print("=" * 50)
        
      
        if not cls.API_KEY:
            print("⚠️  WARNING: API_KEY not set in .env file!")
            print("   Your AI agent will not work without this!")
            print("=" * 50)
    
    @classmethod
    def get_cors_origins(cls):
       
        if cls.is_dev():
          
            return ["*"]
        else:
           
            return [
                "http://localhost:3000",
                "http://localhost:5500",
                "http://localhost:5501",
                "http://127.0.0.1:5500",
                "http://127.0.0.1:5501",
                
            ]