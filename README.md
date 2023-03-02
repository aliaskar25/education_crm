# education_crm
Non-commercial education crm-system with FastAPI  


1. Make migrations:
    in terminal run: alembic init migrations
    in migrations/env.py in 19 str paste "from main import Base"
    in migrations/env.py in 20 str paste "target_metadata = Base.metadata"
    in alembic.ini find "sqlalchemy.url" and as value paste "postgresql://postgres:postgres@0.0.0.0:5432/postgres"

2. Run migrations:
    alembic revision --autogenerate -m "some comment for migration"
    alembic upgrade head
    --------------------
    alembic stamp head
    alembic revision --autogenerate -m "New revision"
    alembic upgrade head
    alembic stamp head
