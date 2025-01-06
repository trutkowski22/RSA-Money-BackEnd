from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config.settings import Config

# Create async engine
engine = create_async_engine(
    f"mysql+aiomysql://{Config.DB_CONFIG['user']}:{Config.DB_CONFIG['password']}@{Config.DB_CONFIG['host']}/{Config.DB_CONFIG['database']}",
    pool_size=Config.DB_CONFIG['pool_size'],
    pool_recycle=Config.DB_CONFIG['pool_recycle']
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
