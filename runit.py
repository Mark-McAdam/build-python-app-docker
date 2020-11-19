"""
Parse binary log file according to instructions in README.MD
Answer the following questions about the data in the txnlog.dat file 
What is the total amount in dollars of debits?
What is the total amount in dollars of credits?
How many autopays were started?
How many autopays were ended?
What is balance of user ID 2456938384156277127?
"""

# import numpy as np
import pandas as pd
import struct

# filepath for mounted directory in docker
FILENAME = "app/txnlog.dat"
USERID = 2456938384156277127
txn_type = {
    b"\x00": "Debit",
    b"\x01": "Credit",
    b"\x02": "StartAutopay",
    b"\x03": "EndAutopay",
}
header_length = 9
record_length = 13
dollar_length = 8
df_column_names = ["Transaction_Type", "Unix_Timestamp", "User_ID", "Amount"]
all_transactions = pd.DataFrame(columns=df_column_names)


# Skip header
# start at first record
start_byte = header_length

with open(FILENAME, "rb") as binary:
    txns = binary.read()

# unpack header
magic_string = struct.unpack(">4s", txns[0:4])
version_no = struct.unpack(">B", txns[4:5])
total_records = struct.unpack(">I", txns[5:9])


for i in range(total_records[0]):
    stop_byte = start_byte + record_length
    (txns_type, timestamp, user) = struct.unpack(">cIQ", txns[start_byte:stop_byte])

    # set start to where last txn stopped
    start_byte = stop_byte
    transaction_amount = None  # records that do not contain an amount

    transaction_type = txn_type[txns_type]

    if transaction_type == "Debit" or transaction_type == "Credit":
        stop_byte = start_byte + dollar_length
        transaction_amount = struct.unpack(">d", txns[start_byte:stop_byte])[0]
        start_byte = stop_byte

    # print(transaction_type, timestamp, user, transaction_amount)
    all_transactions.loc[i] = [transaction_type, timestamp, user, transaction_amount]


def calc_total_credits(txns_to_parse):
    total_credits = round(
        txns_to_parse.loc[
            txns_to_parse["Transaction_Type"] == "Credit", "Amount"
        ].sum(),
        2,
    )
    return total_credits


def calc_total_debits(txns_to_parse):
    total_debits = round(
        txns_to_parse.loc[txns_to_parse["Transaction_Type"] == "Debit", "Amount"].sum(),
        2,
    )
    return total_debits


def calc_autopay_started(txns_to_parse):
    is_started = txns_to_parse["Transaction_Type"] == "StartAutopay"
    return txns_to_parse[is_started]["Transaction_Type"].count()


def calc_autopay_ended(txns_to_parse):
    is_ended = txns_to_parse["Transaction_Type"] == "EndAutopay"
    return txns_to_parse[is_ended]["Transaction_Type"].count()


def calc_user_balance(txns_to_parse, user_id):

    is_user = txns_to_parse["User_ID"] == user_id

    user_transactions = txns_to_parse[is_user]
    user_transactions.head()

    user_credits = round(
        user_transactions.loc[
            user_transactions["Transaction_Type"] == "Credit", "Amount"
        ].sum(),
        2,
    )

    user_debits = round(
        user_transactions.loc[
            user_transactions["Transaction_Type"] == "Debit", "Amount"
        ].sum(),
        2,
    )

    balance_for_user = user_credits - user_debits

    return balance_for_user


def runit():
    """
    puts it all together to:
    Answer the following questions about the data in the txnlog.dat file 
    What is the total amount in dollars of debits?
    What is the total amount in dollars of credits?
    How many autopays were started?
    How many autopays were ended?
    What is balance of user ID 2456938384156277127?
    """
    total_credits = calc_total_credits(all_transactions)
    print(f"total credit amount = {total_credits}")

    total_debits = calc_total_debits(all_transactions)
    print(f"total debit amount = {total_debits}")

    is_started = calc_autopay_started(all_transactions)
    print(f"autopays started = {is_started}")

    is_ended = calc_autopay_ended(all_transactions)
    print(f"autopays ended = {is_ended}")

    balance_for_user = calc_user_balance(all_transactions, USERID)
    print(f"balance for user 2456938384156277127 = {balance_for_user:.2f}")


if __name__ == "__main__":
    runit()

