import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Set up the database connection and session factory
engine = sqlalchemy.create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)

# Define the unit of work class
class UnitOfWork:
    def __init__(self):
        self.session = None
    
    def __enter__(self):
        self.session = Session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    @contextmanager
    def get_session(self):
        """Helper function to manage sessions"""
        session = Session()
        try:
            yield session
        except:
            session.rollback()
            raise
        finally:
            session.close()

# Example usage
with UnitOfWork() as uow:
    with uow.get_session() as session:
        # Perform database operations within the session context
        # e.g. create, read, update, delete (CRUD) operations
        user1 = User(name="John Doe", email="john@example.com")
        session.add(user1)
        session.commit()
