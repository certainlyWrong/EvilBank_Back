import sqlalchemy as sa

from . import Base


class LogEntity(Base):
    __tablename__ = 'log'

    log_id = sa.Column(sa.CHAR(36), primary_key=True)

    account_id = sa.Column(
        sa.CHAR(36),
        sa.ForeignKey('account.account_id'),
    )

    log_date = sa.Column(sa.DateTime, nullable=False)
    log_type = sa.Column(sa.String(255), nullable=False)
    log_message = sa.Column(sa.String(255), nullable=False)
