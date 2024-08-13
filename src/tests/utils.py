from factory.alchemy import SQLAlchemyModelFactory


def factory_to_dict(
    model_factory: SQLAlchemyModelFactory,
) -> dict:
    model_dict = {
        col.name: getattr(model_factory, col.name)
        for col in model_factory.__table__.columns
    }
    model_dict.pop("id", None)
    return model_dict
