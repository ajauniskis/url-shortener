from unittest import TestCase
from app.infrastructure import get_database
import os


class TestGetDatabase(TestCase):
    def test_get_database__invalid_database_type__thorws(self):
        os.environ["DATABASE_TYPE"] = "invalid-database"

        with self.assertRaises(ValueError) as exception_context:
            get_database("some_table")

        self.assertEqual(
            str(exception_context.exception),
            "Unknown database type: invalid-database. "
            + "Valid database types: ['deta-base'].",
        )

    def test_get_database__returns_database_client(self):
        database = get_database("some_table")
        actual = type(database).__bases__[0].__name__

        self.assertEquals(
            actual,
            "AbstractDatabaseClient",
        )
