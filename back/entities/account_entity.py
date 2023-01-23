import sqlalchemy as sa

from . import Base


class AccountEntity(Base):
    __tablename__ = 'account'

    account_id = sa.Column(sa.CHAR(36), primary_key=True)

    person_id = sa.Column(
        sa.CHAR(36),
        sa.ForeignKey('person.person_id'),
    )

    account_name = sa.Column(sa.String(255), nullable=False, unique=True)
    account_hash = sa.Column(sa.CHAR(64), nullable=False)
    account_balance = sa.Column(sa.Float, nullable=False)
    account_limit = sa.Column(sa.Float, nullable=False)
