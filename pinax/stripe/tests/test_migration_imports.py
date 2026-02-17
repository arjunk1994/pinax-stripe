from pathlib import Path
from unittest import TestCase


class MigrationImportTests(TestCase):

    def test_0004_plan_metadata_imports_models(self):
        source = Path("pinax/stripe/migrations/0004_plan_metadata.py").read_text()
        self.assertIn("from django.db import migrations, models", source)

    def test_0013_charge_outcome_imports_models(self):
        source = Path("pinax/stripe/migrations/0013_charge_outcome.py").read_text()
        self.assertIn("from django.db import migrations, models", source)
