from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()

class PickingLog(Base):
    __tablename__ = 'picking_logs'

    id = Column(Integer, primary_key=True)
    order_id = Column(String(50), nullable=False)
    box_id = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float)
    status = Column(String(20))  # 'success', 'failed', 'in_progress'

    def __repr__(self):
        return f"<PickingLog(order_id='{self.order_id}', box_id='{self.box_id}', timestamp='{self.timestamp}')>"

# Create database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(engine)

def add_picking_log(order_id: str, box_id: str, confidence: float, status: str = 'in_progress'):
    """Add a new picking log entry."""
    session = Session()
    try:
        log = PickingLog(
            order_id=order_id,
            box_id=box_id,
            confidence=confidence,
            status=status
        )
        session.add(log)
        session.commit()
        return log
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_picking_logs(order_id: str = None, limit: int = 100):
    """Retrieve picking logs, optionally filtered by order_id."""
    session = Session()
    try:
        query = session.query(PickingLog)
        if order_id:
            query = query.filter(PickingLog.order_id == order_id)
        return query.order_by(PickingLog.timestamp.desc()).limit(limit).all()
    finally:
        session.close()

def update_picking_status(log_id: int, status: str):
    """Update the status of a picking log."""
    session = Session()
    try:
        log = session.query(PickingLog).filter(PickingLog.id == log_id).first()
        if log:
            log.status = status
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close() 