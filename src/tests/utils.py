from factory import SubFactory
from factory.alchemy import SQLAlchemyModelFactory


def factory_to_dict(
    model_factory: SQLAlchemyModelFactory | SubFactory,
) -> dict:
    """
    Converting a factory model to a dictionary.
    :param model_factory: Model of factory.
    :return: Factory fields in dictionary format.
    """
    model_dict = {
        col.name: getattr(model_factory, col.name)
        for col in model_factory.__table__.columns
    }
    model_dict.pop("id", None)
    return model_dict
