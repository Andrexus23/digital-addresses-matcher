from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, Column, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Addresses(Base):
    __tablename__ = 'addresses'
    __table_args__ = (
        PrimaryKeyConstraint('addresses_id', name='addresses_pkey'),
    )

    addresses_id = mapped_column(BigInteger)
    epgu_id = mapped_column(BigInteger)
    is_from_priem = mapped_column(Boolean)
    epgu_address = mapped_column(Text)
    is_registration = mapped_column(Boolean)
    epgu_city = mapped_column(Text)
    kladr_1 = mapped_column(Text)
    kladr_2 = mapped_column(Text)
    kladr_3 = mapped_column(Text)
    kladr_4 = mapped_column(Text)
    kladr_5 = mapped_column(Text)
    post_index = mapped_column(Text)
    street = mapped_column(Text)
    house = mapped_column(Text)
    building = mapped_column(Text)
    letter = mapped_column(Text)
    building2 = mapped_column(Text)
    flat = mapped_column(Text)


class Kladr(Base):
    __tablename__ = 'kladr'
    __table_args__ = (
        ForeignKeyConstraint(['code'], ['kladr.code'], name='fk_parent_code'),
        ForeignKeyConstraint(['parent_code'], ['kladr.code'], ondelete='SET NULL', name='kladr_parent_code_fkey'),
        PrimaryKeyConstraint('code', name='kladr_pkey')
    )

    code = mapped_column(Text)
    name = mapped_column(Text)
    socr = mapped_column(Text)
    index = mapped_column(BigInteger)
    gninmb = mapped_column(BigInteger)
    uno = mapped_column(BigInteger)
    ocatd = mapped_column(BigInteger)
    status = mapped_column(Integer)
    parent_code = mapped_column(Text)

    kladr: Mapped[Optional['Kladr']] = relationship('Kladr', remote_side=[code], foreign_keys=[parent_code], back_populates='kladr_reverse')
    kladr_reverse: Mapped[List['Kladr']] = relationship('Kladr', uselist=True, remote_side=[parent_code], foreign_keys=[parent_code], back_populates='kladr')
