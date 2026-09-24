import pandas as pd


def reconcile(orders_csv, payments_csv):
    orders = pd.read_csv(orders_csv)
    payments = pd.read_csv(payments_csv)
    # Inner join drops unpaid orders and orphan payments; float sums can drift.
    return orders.merge(payments, on="order_id").groupby("order_id").sum()
