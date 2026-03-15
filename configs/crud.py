# configs/crud.py

from sqlalchemy.orm import Session
from typing import TypeVar, Type, Generic, List, Any
from sqlalchemy.exc import SQLAlchemyError

ModelType = TypeVar("ModelType")


class BaseCrud(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """The flexible base initialization for all models to share common
        crud functionality. By passing the model, the context required
        is provided to preform each operation without specifying the model
        every time.

        Args:
            model: The model to initialize."""
        self.model = model

    def get_records(
        self,
        db: Session,
        filters: dict = None,
        skip: int = None,
        total_records: int = None,
    ) -> List[ModelType] | bool:
        """Dumps all records within the database for the provided model if no limit is provided.
        Args:
            db: The database session to query records for.
            filters: Metrics to narrow query results by.
            skip: The number of records to skip from the beginning of the query.
            total_records: The total number of records to return. If 0, the entire table is returned.
        Returns:
            List of records within the database for the provided model."""
        try:
            records = db.query(self.model)
            if filters is not None:
                records = records.filter_by(**filters)
            if skip is not None:
                records = records.offset(skip)
            if total_records is not None:
                records = records.limit(total_records)
            return records.all()
        except SQLAlchemyError:
            return False

    def get_by_id(self, db: Session, record_id: Any) -> ModelType:
        """Grabs a specific record based on the provided id.
        Args:
            db: The database session to query records for.
            record_id: The id of the record being requested
        Returns:
            A single model record based on the provided id.
        """
        try:
            record = db.query(self.model).filter(self.model.id == record_id).first()
            if record:
                return record
            else:
                return False
        except SQLAlchemyError:
            return False

    def new_record(
        self, db: Session, data: dict, commit: bool = True, return_record=False
    ) -> bool | ModelType:
        """Adds a new record to the database and returns the record is requested.
        Args:
            db: The database session to query records for.
            data: The data to insert into the database.
            commit: Whether or not to commit the record within the function
            return_record: Whether or not to return the record created.
        Returns:
              Returns a boolean to signify successful save or the new record created if requested.
        """
        db_obj = self.model(**data)
        try:
            db.add(db_obj)
            if commit:
                db.commit()
            if return_record:
                db.refresh(db_obj)
                return db_obj
        except SQLAlchemyError:
            db.rollback()
            return False
        return True

    def remove_records(
        self, db: Session, record_id: Any, deactivate: bool = True, col: str = None
    ) -> bool | ModelType:
        try:
            record = self.get_by_id(db, record_id)
            if not record:
                return False
            if deactivate and col is not None:
                setattr(record, col, False)
            elif deactivate and col is None:
                return False
            else:
                db.delete(record)
            db.commit()
            return True
        except SQLAlchemyError:
            db.rollback()
            return False

    def update_record(
        self, db: Session, record_id: int, new_data: dict, commit: bool = True
    ) -> ModelType | bool:
        """
        Look for record based on the provided record id. If found, update the record with newly provided information
        Args:
            db: The database session to query records for.
            record_id: The id of the record being requested
            new_data: The data to update the record with.
            commit: Whether or not to commit the record within the function
        """
        try:
            record = self.get_by_id(db, record_id)
            if not record:
                return False
            for key, value in new_data.items():
                setattr(record, key, value)
            if commit:
                db.commit()
                db.refresh(record)
                return record
        except SQLAlchemyError:
            db.rollback()
            return False
