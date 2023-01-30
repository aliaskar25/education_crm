from envparse import Env


env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://education_crm_user:education_crm_password@0.0.0.0:5432/education_crm_db"
)