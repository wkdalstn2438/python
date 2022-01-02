from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.sql.sqltypes import INTEGER, String, DateTime
from connect.db import meta, engine


persons = Table('person', meta,
                Column('ssn', String(255), primary_key=True),
                Column('name', String(255), nullable=False),
                Column('age', INTEGER(), nullable=False),
                Column('tel', String(255), nullable=False),
                )

commutes = Table('commute', meta,
                 Column('id', String(255), primary_key=True, autoincrement=True),
                 Column('ssn', String(255), ForeignKey("person.ssn", ondelete="cascade"), nullable=False),
                 Column('st', DateTime),
                 Column('et', DateTime),
                 )

payments = Table('payment', meta,
                 Column('id', INTEGER(), primary_key=True),
                 Column('ssn', String(255), ForeignKey("person.ssn", ondelete="cascade"), nullable=False),
                 Column('money', INTEGER(), nullable=False),
                 Column('date', DateTime, nullable=False),
                 )

meta.create_all(engine)
