# configs/crud.py

from sqlalchemy.orm import Session
from typing import TypeVar, Type, Generic, List, Any

ModelType = TypeVar("ModelType")


class BaseCrud(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """The flexible base initialization for all models to share common
        crud functionality. By passsing the model, the context required
        is provided to preform each operation without specifying the model
        every time.

        Args:
            model: The model to initialize."""
        self.model = model

    def get_records(
        self, db: Session, skip: int = 0, total_records: int = 0
    ) -> List[ModelType]:
        """Dumps all records within the database for the provided model if no
        limit is provided.
        Args:
            db: The database session to query records for.
            skip: The number of records to skip from the beginning of the query.
            total_records: The total number of records to return. If 0, the entire table is returned.
        Returns:
            List of records within the database for the provided model."""
        records = db.query(self.model).offset(skip)
        if total_records != 0:
            records = records.limit(total_records)
        return records.all()

    def get_by_id(self, db: Session, id: int) -> ModelType:
        """Grabs a specific record based on the provided id.
        Args:
            db: The database session to query records for.
            id: The id of the record being requested
        Returns:
            A single model record based on the provided id.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def new_record(
        self, db: Session, data: dict, commit: bool = True, return_record=False
    ) -> Any:
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
        except Exception:
            return False
        return True

    def get_filtered_records(
        self, db: Session, filters: dict, skip: int = 0, total_records: int = 0
    ) -> List[ModelType]:
        """Dumps all records within the database fitting the provided filters if no limit is
            provided.
        Args:
            db: The database session to query records for.
            filters: The filters to apply to the query.
            skip: The number of records to skip from the beginning of the query.
            total_records: The total number of records to return. If 0, the entire table is
                returned.
        Returns:
            List of records within the database fitting the provided fitlers."""
        records = db.query(self.model).filter_by(**filters).offset(skip)
        if total_records != 0:
            records = records.limit(total_records)
        return records.all()
