from flask import Flask, render_template, request
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

app = Flask(__name__)

# -----------------------------
# Load Dataset
# -----------------------------
data = pd.read_csv("dataset.csv")

transactions = []

for items in data["items"]:
    transactions.append(items.split(","))

# -----------------------------
# Transaction Encoding
# -----------------------------
te = TransactionEncoder()
te_array = te.fit(transactions).transform(transactions)

basket = pd.DataFrame(te_array, columns=te.columns_)

# -----------------------------
# Frequent Itemsets
# -----------------------------
frequent_itemsets = apriori(
    basket,
    min_support=0.20,
    use_colnames=True
)

# -----------------------------
# Association Rules
# -----------------------------
rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=0.50
)

# -----------------------------
# Recommendation Function
# -----------------------------
def recommend_product(product):

    recommendations = []

    product = product.strip().lower()

    for _, row in rules.iterrows():

        antecedent = [str(i).lower() for i in row["antecedents"]]

        consequent = list(row["consequents"])

        if product in antecedent:

            for item in consequent:
                if item not in recommendations:
                    recommendations.append(item)

    return recommendations


# -----------------------------
# Home Page
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []

    searched_product = ""

    if request.method == "POST":

        searched_product = request.form["product"]

        recommendations = recommend_product(searched_product)

    return render_template(
        "index.html",
        recommendations=recommendations,
        product=searched_product
    )


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
