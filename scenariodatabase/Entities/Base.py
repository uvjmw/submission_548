# define a base object
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

meta = MetaData(naming_convention={
    "ix": "ix-%(column_0_label)s",
    "uq": "uq-%(table_name)s-%(column_0_name)s",
    "ck": "ck-%(table_name)s-%(constraint_name)s",
    "fk": "fk-%(table_name)s-%(column_0_name)s-%(referred_table_name)s",
    "pk": "pk-%(table_name)s"
})

"""
This is based on the accepted answer in http://stackoverflow.com/questions/12032260/
"""


class ORMBase(object):
    """
    This class is a superclass of SA-generated Base class,
    which in turn is the superclass of all db-aware classes
    so we can define common functions here
    """

    def __setattr__(self, name, value):
        """
        Raise an exception if attempting to assign to an atribute which does not exist in the model.
        We're not checking if the attribute is an SQLAlchemy-mapped column because we also want it to work with properties etc.
        """
        if name != "_sa_instance_state" and not hasattr(self, name):
            raise AttributeError("Attribute %s is not a mapped column of object %s" % (name, self))
        super(ORMBase, self).__setattr__(name, value)


# define a base object
Base = declarative_base(cls=ORMBase, metadata=meta)
