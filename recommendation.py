import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


class RecommendationEngine:

    def __init__(self, dataset_path="dataset.csv"):

        self.dataset_path = dataset_path
        self.transactions = []
        self.rules = None

        self.load_dataset()
        self.train_model()

    # -----------------------------
    # Load Dataset
    # -----------------------------
    def load_dataset(self):

        data = pd.read_csv(self.dataset_path)

        self.transactions = []

        for items in data["items"]:
            self.transactions.append(items.split(","))

    # -----------------------------
    # Train Apriori Model
    # -----------------------------
    def train_model(self):

        te = TransactionEncoder()

        te_array = te.fit(self.transactions).transform(self.transactions)

        basket = pd.DataFrame(
            te_array,
            columns=te.columns_
        )

        frequent_itemsets = apriori(
            basket,
            min_support=0.20,
            use_colnames=True
        )

        self.rules = association_rules(
            frequent_itemsets,
            metric="confidence",
            min_threshold=0.50
        )

    # -----------------------------
    # Recommend Products
    # -----------------------------
    def recommend(self, product):

        recommendations = []

        product = product.strip().lower()

        for _, row in self.rules.iterrows():

            antecedent = [
                str(item).lower()
                for item in row["antecedents"]
            ]

            consequent = list(row["consequents"])

            if product in antecedent:

                for item in consequent:

                    if item not in recommendations:
                        recommendations.append(item)

        return recommendations

    # -----------------------------
    # Get Available Products
    # -----------------------------
    def get_all_products(self):

        products = set()

        for transaction in self.transactions:

            for item in transaction:

                products.add(item)

        return sorted(products)

    # -----------------------------
    # Display Association Rules
    # -----------------------------
    def get_rules(self):

        return self.rules[
            [
                "antecedents",
                "consequents",
                "support",
                "confidence",
                "lift"
            ]
        ]
