
-----------database foudation--------------------
python -c "from app.database import engine; print(engine.url)"

---------Security----------------------------
grep -E '^(SECRET_KEY|ALGORITHM|ACCESS_TOKEN_EXPIRE_MINUTES|DATABASE_URL)=' .env | sed 's/=.*/=<set>/'


python -c "from app.config import settings; print(settings.algorithm, settings.access_token_expire_minutes, settings.database_url)"

python -c "from app.utils.security import hash_password, verify_password; h=hash_password('TestPassword123'); print(verify_password('TestPassword123', h)); print(verify_password('wrong-password', h))"

 python -c "from app.utils.security import create_access_token; token=create_access_token({'sub':'1'}); print(token)"


------------Models----------------------------
python -c "from app.models.user import User; print(User.__tablename__)"

python -c "from app.models.task import Task; print(Task.__tablename__)"


python -c "from app.models.task import Task, Priority; print(Task.__tablename__); print(list(Priority))"

python -c "from app.models.user import User; from app.models.task import Task; print(Task.__table__.c.user_id.foreign_keys)"




python -c "from app.database import Base; import app.models; print(list(Base.metadata.tables.keys()))"

------------------schemas------------------------
python -c "from app.schemas.task import TaskResponse; print(TaskResponse.model_json_schema()['example']['title'])"

python -c "from app.schemas.auth import UserResponse; print(UserResponse.model_json_schema()['example']['email'])"
