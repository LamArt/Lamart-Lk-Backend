from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environ
env = environ.Env()
env.read_env(Path.joinpath(BASE_DIR, ".env"))