"""Services modules for orchestration logic and handling use case scenarios."""
from . import exceptions
from funds_api.database import exceptions as db_exceptions
from funds_api.database.base import AbstractDb
from funds_api.database.model import Fund


def _is_fund_exists(db: AbstractDb, id: int):
    return id in db.get_all_ids()


def add_fund(db: AbstractDb, data: dict):
    if not data:
        raise exceptions.InvalidInputError('No data provided')

    try:
        fund = Fund(data) # Checks whether the input data follows the schema.
    except db_exceptions.InvalidFundDataInput as exc:
        raise exceptions.InvalidInputError(exc) from exc

    if _is_fund_exists(db, data['id']):
        raise exceptions.InvalidInputError(f'Fund {data["id"]} already exists')

    db.add_fund(fund.details)
    return data['id']


def get_fund(db: AbstractDb, id: int):
    if not _is_fund_exists(db, id):
        raise exceptions.NotFoundError(f'Fund {id} not found')

    fund = db.get_fund(id)
    return fund


def update_performance(db: AbstractDb, id: int, data: dict):
    if not _is_fund_exists(db, id):
        raise exceptions.NotFoundError(f'Fund {id} not found')

    if not data or 'performance' not in data or len(data) > 1:
        raise exceptions.InvalidInputError(
            'Input data must be sent in JSON and only with the performance value'
        )

    target_fund = db.get_fund(id)
    target_fund['performance'] = data['performance']

    try:
        # Validate the updated data against the model.
        fund = Fund(target_fund)
    except db_exceptions.InvalidFundDataInput as exc:
        raise exceptions.InvalidInputError(exc) from exc

    db.update_fund(id, fund.details)
    return target_fund


def delete_fund(db: AbstractDb, id: int):
    if not _is_fund_exists(db, id):
        raise exceptions.NotFoundError(f'Fund {id} not found')

    db.delete_fund(id)

    return ''
    