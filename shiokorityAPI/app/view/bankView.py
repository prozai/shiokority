from flask import Blueprint, request, jsonify
from ..controller.bankController import BankController

bankBlueprint = Blueprint('bankBlueprint', __name__)


@bankBlueprint.route("/view_transaction", methods=['GET'])
def viewTransaction():

    transaction = BankController().viewAllTransaction()
    return jsonify(transaction)

@bankBlueprint.route("/view_transactionHistory", methods=['GET'])
def viewTransactionHistory():

    transactionHistory = BankController().viewAllTransactionHistory()
    return jsonify(transactionHistory)

@bankBlueprint.route("/view_transactionRecord", methods=['GET'])
def viewTransactionRecord():

    transactionRecord = BankController().viewAllTransactionRecord()
    return jsonify(transactionRecord)