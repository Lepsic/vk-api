from app.internal.repository.repository import Repository
from app.pkg import models
from app.internal.repository.postgresql.connection import get_connection
import sqlalchemy


class UserRepository(Repository):

	async def create(self, cmd: models.app.user_schema.CreateUserCommand) -> models.app.user_schema.User:
		async with get_connection() as connection:
			user = await connection.execute(
				sqlalchemy.insert(
					models.app.user_sql.User
				).values(
					**cmd.to_dict(show_secrets=True)
				).returning(
					models.app.user_sql.User
				)
			)
			await connection.commit()
			return models.app.user_schema.User.from_orm(user.scalar_one())

	async def read_by_login(self, cmd: models.app.user_schema.ReadUserByLoginCommand) -> models.app.user_schema.User:

		async with get_connection() as connection:
			user = await connection.execute(
				sqlalchemy.select(
					models.app.user_sql.User
				).filter(
					sqlalchemy.and_(
						models.app.user_sql.User.username == cmd.login,
						models.app.user_sql.User.status == cmd.status
					)
				)
			)
			return models.app.user_schema.User.from_orm(user.scalar_one())


	async def read_by_id(self, cmd: models.app.user_schema.ReadUserByIdCommand) -> models.app.user_schema.User:

		async with get_connection() as connection:
			user = await connection.execute(
				sqlalchemy.select(
					models.app.user_sql.User
				).filter(
					sqlalchemy.and_(
						models.app.user_sql.User.id == cmd.id,
						models.app.user_sql.User.status == cmd.status
					)
				)
			)
			return models.app.user_schema.User.from_orm(user.scalar_one())
