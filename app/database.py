from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from fastapi import HTTPException
from app.config import DATABASES

class DatabaseManager:
    def __init__(self, db_configs):
        self.db_configs = db_configs
        self._connections = {}
        self._sessionmakers = {}
        
    async def initialize(self):
        """Initialize database connections"""
        for tenant, url in self.db_configs.items():
            if tenant not in self._connections:
                self._connections[tenant] = Database(url)
                await self._connections[tenant].connect()
                
    async def close(self):
        """Close all database connections"""
        for connection in self._connections.values():
            await connection.disconnect()
            
    def get_database(self, tenant: str) -> Database:
        if tenant not in self.db_configs:
            raise HTTPException(status_code=400, detail="Tenant not found")
            
        if tenant not in self._connections:
            db_url = self.db_configs[tenant]
            self._connections[tenant] = Database(db_url)
            
        return self._connections[tenant]
        
    def get_sessionmaker(self, tenant: str):
        if tenant not in self._sessionmakers:
            db = self.get_database(tenant)
            engine = create_engine(str(db.url))
            self._sessionmakers[tenant] = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            )
        return self._sessionmakers[tenant]

# Create global database manager instance
db_manager = DatabaseManager(DATABASES)