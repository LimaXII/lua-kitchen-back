import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if "test_create_recipe_api" not in " ".join(sys.argv):
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
