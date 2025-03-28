from app.pkg.models.app.schema.user import UserStatus
from app.pkg.models.app.sqlalchemy import Base
import uuid
import sqlalchemy


class User(Base):
	__tablename__ = "users"

	id = sqlalchemy.Column(
		sqlalchemy.UUID(as_uuid=True),
		primary_key=True,
		index=True,
		default=uuid.uuid4,
	)
	login = sqlalchemy.Column(sqlalchemy.String(65), unique=True, nullable=False)
	password = sqlalchemy.Column(sqlalchemy.LargeBinary(), nullable=False)
	vk_username = sqlalchemy.Column(sqlalchemy.String(65), unique=True, nullable=False)
	status = sqlalchemy.Column(sqlalchemy.Enum(UserStatus))

