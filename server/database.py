from flask_sqlalchemy import BaseQuery, Model, SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.exceptions import abort


# copied from https://github.com/Mari-W/auth-server/blob/master/server/database.py

class BaseQueryExtension(BaseQuery):
    """
    some extensions to flask sql alchemy
    """

    base_error = "Failed to lookup some database entry. An error message was not provided."

    def one_or_404(self, error_message="", **kwargs):
        """
        wraps first_or_404 with error message
        """
        return self.filter_by(**kwargs).first_or_404(error_message if error_message else self.base_error)

    def many_or_404(self, error_message="", **kwargs):
        """
        wraps all_or_404 with error message
        """
        if not kwargs:
            q = self.all()
            if not q:
                abort(404, error_message if error_message else self.base_error)
            return q
        else:
            return self.filter_by(**kwargs).all_or_404(error_message if error_message else self.base_error)

    def one(self, **kwargs):
        """
        wraps filter and first
        """
        return self.filter_by(**kwargs).first()

    def many(self, **kwargs):
        """
        wraps filter and all
        """
        return self.filter_by(**kwargs).all()

    def exists(self, error_message="", **kwargs):
        """
        true when models exists
        """
        return bool(self.filter_by(**kwargs).first())

    def delete_by(self, **kwargs):
        """
        true when models exists
        """
        self.filter_by(**kwargs).delete()


class BaseModel(Model):
    """
    extensions to all models
    """

    # prevents "unresolved reference" warnings
    query: BaseQueryExtension

    def to_json(self, id=False):
        """
        used in templates
        """
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_') and (id or key != "id")}


class Database:
    """
    wraps sql alchemy
    """
    sql_alchemy: SQLAlchemy
    Model: DeclarativeMeta

    def __init__(self):
        self.sql_alchemy: SQLAlchemy = SQLAlchemy(query_class=BaseQueryExtension, model_class=BaseModel)
        self.Model = self.sql_alchemy.Model

    def __iadd__(self, other):
        self.sql_alchemy.session.add(other)

    def __isub__(self, other):
        self.sql_alchemy.session.delete(other)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        commits changes made on database objects
        """
        self.sql_alchemy.session.commit()

    @property
    def alchemy(self):
        """
        returns sql alchemy object
        """
        return self.sql_alchemy

    @property
    def session(self):
        """
        returns sql alchemy session object
        """
        return self.sql_alchemy.session


database = Database()
