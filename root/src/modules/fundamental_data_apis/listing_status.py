import asyncio
from typing import List, Dict
from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError
from src.database import get_db
from src.core.runner import APIRunner
from src.core.batch import BatchProcessor
from src.utils.logger import logger
from src.config.settings import Config

class ListingStatusProcessor:
    def __init__(self):
        self.runner = APIRunner()
        self.batch_processor = BatchProcessor()
        
    async def fetch_listing_status(self) -> List[Dict]:
        """Fetch listing status data from API"""
        params = {
            'function': 'LISTING_STATUS',
            'state': 'active',
            'date': None,  # Will be set based on update mode
            'datatype': 'csv'
        }
        
        try:
            response = self.runner.make_api_call(params)
            return self._parse_csv_response(response)
        except Exception as e:
            logger.error(f"Failed to fetch listing status: {e}")
            raise

    def _parse_csv_response(self, response: str) -> List[Dict]:
        """Parse CSV response into structured data"""
        # Implementation depends on actual CSV format
        pass

    async def process_symbols(self, symbols: List[str]):
        """Process symbols into different tables"""
        await self.batch_processor.process_batch(
            symbols,
            self._process_symbol
        )

    async def _process_symbol(self, symbol: str):
        """Process individual symbol"""
        async with get_db() as session:
            try:
                # Check if symbol exists in active_symbols
                result = await session.execute(
                    select([active_symbols]).where(active_symbols.c.symbol == symbol)
                )
                
                if not result.scalar():
                    # Insert new symbol
                    await session.execute(
                        insert(active_symbols).values({
                            'symbol': symbol,
                            'status': 'active'
                        })
                    )
                    await session.commit()
                    logger.info(f"Inserted new symbol: {symbol}")
            except IntegrityError:
                await session.rollback()
                logger.warning(f"Symbol {symbol} already exists")

    async def run(self, update_mode: bool = False):
        """Main execution method"""
        logger.info("Starting listing status processing")
        
        try:
            # Fetch data
            listing_data = await self.fetch_listing_status()
            
            # Process symbols
            await self.process_symbols([item['symbol'] for item in listing_data])
            
            logger.info("Listing status processing completed successfully")
        except Exception as e:
            logger.error(f"Listing status processing failed: {e}")
            raise

async def main():
    processor = ListingStatusProcessor()
    await processor.run()

if __name__ == "__main__":
    asyncio.run(main())
