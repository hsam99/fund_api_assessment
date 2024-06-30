"""Endpoints for fund related operations."""
from flask import Blueprint, request, jsonify

from funds_api.database import get_db
from funds_api.services import exceptions, services


bp = Blueprint('funds', __name__)
HTTP_OK_CODE = 200
HTTP_CREATED_CODE = 201
HTTP_NO_CONTENT_CODE = 204
HTTP_INPUT_ERROR_CODE = 400
HTTP_NOT_FOUND_CODE = 404

@bp.route('/funds', methods=['POST'])
def add_fund():
    db = get_db()

    try:
        response = services.add_fund(db, request.json)
    except exceptions.InvalidInputError as exc:
        return jsonify({'error': str(exc)}), HTTP_INPUT_ERROR_CODE

    return jsonify(response), HTTP_CREATED_CODE


@bp.route('/funds', methods=['GET'])
def get_all_funds():
    db = get_db()
    return jsonify(db.get_all()), HTTP_OK_CODE


@bp.route('/funds/<int:fund_id>', methods=['GET'])
def get_fund(fund_id):
    db = get_db()

    try:
        response = services.get_fund(db, fund_id)
    except exceptions.NotFoundError as exc:
        return jsonify({'error': str(exc)}), HTTP_NOT_FOUND_CODE

    return jsonify(response), HTTP_OK_CODE


@bp.route('/funds/<int:fund_id>', methods=['PATCH'])
def update_performance(fund_id):
    db = get_db()

    try:
        response = services.update_performance(db, fund_id, request.json)
    except exceptions.InvalidInputError as exc:
        return jsonify({'error': str(exc)}), HTTP_INPUT_ERROR_CODE
    except exceptions.NotFoundError as exc:
        return jsonify({'error': str(exc)}), HTTP_NOT_FOUND_CODE

    return jsonify(response), HTTP_OK_CODE


@bp.route('/funds/<int:fund_id>', methods=['DELETE'])
def delete_fund(fund_id):
    db = get_db()
    try:
        response = services.delete_fund(db, fund_id)
    except exceptions.NotFoundError as exc:
        return jsonify({'error': str(exc)}), HTTP_NOT_FOUND_CODE

    return jsonify(response), HTTP_NO_CONTENT_CODE
