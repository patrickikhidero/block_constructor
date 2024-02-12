import csv
from typing import List

class MempoolTransaction:
    def __init__(self, txid, fee, weight, parents):
        self.Txid = txid
        self.Fee = fee
        self.Weight = weight
        self.Parents = parents

def parse_mempool_csv(csv_filename):
    transactions = []

    try:
        with open(csv_filename, 'r') as file:
            reader = csv.reader(file)
            lines = list(reader)

            for line in lines:
                txid = line[0]
                fee = int(line[1])
                weight = int(line[2])
                parents = set()

                if len(line) > 3 and len(line[3]) != 0:
                    parent_txids = line[3].split(";")
                    parents = set(parent_txids)

                transactions.append(MempoolTransaction(txid, fee, weight, parents))
    except (IOError, csv.Error) as e:
        print(f"Error reading CSV file: {e}")
        return None

    return transactions

def calculate_max_fee(transactions: List[MempoolTransaction]) -> List[str]:
    transactions.sort(key=lambda x: x.Fee, reverse=True)

    included_transactions = []
    included_set = set()
    total_weight = 0

    for transaction in transactions:
        parents_included = all(parent in included_set for parent in transaction.Parents)

        if parents_included:
            included_set.add(transaction.Txid)
            included_transactions.append(transaction.Txid)
            total_weight += transaction.Weight

            if total_weight >= 4000000:
                break

    return included_transactions, total_weight

if __name__ == "__main__":
    filename = './bloc_list.csv'
    transactions = parse_mempool_csv(filename)

    if transactions is not None:
        result, total_size = calculate_max_fee(transactions)
        print("\n".join(result))
