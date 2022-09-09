import pytest
import sqlite3
from ...models.ProviderModels import Provider

class TestDB:

    def test_db_entry(db):
        assert db
        
        provider = Provider(
            name = 'Test Provider'
        )

        assert provider
        db.session.add(provider)
        db.session.commit()

        test_provider = Provider.query.get(1)

        assert test_provider

        

            