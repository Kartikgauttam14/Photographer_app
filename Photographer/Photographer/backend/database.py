from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Index, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration from environment variables
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'photohire')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)  # 'customer' or 'photographer'
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # Relationships with cascade delete
    photographer_profile = relationship("PhotographerModel", back_populates="user", uselist=False, cascade="all, delete-orphan")
    bookings_as_customer = relationship("BookingModel", foreign_keys="[BookingModel.customer_id]", back_populates="customer", cascade="all, delete-orphan")
    bookings_as_photographer = relationship("BookingModel", foreign_keys="[BookingModel.photographer_id]", back_populates="photographer", cascade="all, delete-orphan")
    sent_messages = relationship("ChatMessageModel", foreign_keys="[ChatMessageModel.sender_id]", backref="sender", cascade="all, delete-orphan")
    received_messages = relationship("ChatMessageModel", foreign_keys="[ChatMessageModel.receiver_id]", backref="receiver", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_user_email_active', 'email', 'is_active'),
        Index('idx_user_type_active', 'user_type', 'is_active')
    )

class PhotographerModel(BaseModel):
    __tablename__ = "photographers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    portfolio_urls = Column(JSON, nullable=False, default=list)
    specialties = Column(JSON, nullable=False, default=list)
    hourly_rate = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    current_location = Column(JSON)
    rating = Column(Float)
    total_bookings = Column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("UserModel", back_populates="photographer_profile")

    # Indexes
    __table_args__ = (
        Index('idx_photographer_city', 'city'),
        Index('idx_photographer_rating', 'rating')
    )

class BookingModel(BaseModel):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    photographer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    booking_date = Column(DateTime, nullable=False)
    duration_hours = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # 'pending', 'confirmed', 'completed', 'cancelled'
    location = Column(JSON, nullable=False)
    total_amount = Column(Float, nullable=False)
    notes = Column(String)

    # Relationships
    customer = relationship("UserModel", foreign_keys=[customer_id], back_populates="bookings_as_customer")
    photographer = relationship("UserModel", foreign_keys=[photographer_id], back_populates="bookings_as_photographer")

    # Indexes
    __table_args__ = (
        Index('idx_booking_customer', 'customer_id', 'status'),
        Index('idx_booking_photographer', 'photographer_id', 'status'),
        Index('idx_booking_date_status', 'booking_date', 'status')
    )

class ChatMessageModel(BaseModel):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)

    # Indexes
    __table_args__ = (
        Index('idx_chat_sender_receiver', 'sender_id', 'receiver_id', 'created_at'),
        Index('idx_chat_unread', 'receiver_id', 'is_read')
    )

@event.listens_for(BookingModel, 'after_insert')
def update_photographer_booking_count(mapper, connection, target):
    if target.status == 'completed':
        photographer = connection.execute(
            f"UPDATE photographers SET total_bookings = total_bookings + 1 "
            f"WHERE user_id = {target.photographer_id}"
        )

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()