import sqlalchemy as sa

from . import Base


class PersonEntity(Base):
    __tablename__ = 'person'
    person_id = sa.Column(sa.VARCHAR(36), primary_key=True)
    person_first_name = sa.Column(sa.String(255), nullable=False)
    person_last_name = sa.Column(sa.String(255), nullable=False)
    person_age = sa.Column(sa.Integer(), nullable=False)
    person_cpf = sa.Column(sa.String(11), nullable=False, unique=True)
