from flask import Flask, render_template, request
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

app = Flask(__name__)

dataset = [
    ['Laptop', 'Mouse', 'Keyboard'],
    ['Laptop', 'Mouse'],
    ['Mobile', 'Earphones'],
    ['Laptop', 'Mouse', 'Headphones'],
    ['Mobile', 'Charger'],
    ['Laptop', 'Keyboard'],
    ['Mobile', 'Earphones', 'Charger'],
    ['Laptop', 'Mouse', 'Keyboard', 'Headphones']
]

te = TransactionEncoder()
df = pd.DataFrame(te.fit(dataset).transform(dataset), columns=te.columns_)

frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)

rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=0.6
)

def recommend(product):
    recommendations = []

    for _, row in rules.iterrows():
        if product in row['antecedents']:
            recommendations.extend(list(row['consequents']))

    return list(set(recommendations))


@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    product = ""

    if request.method == "POST":
        product = request.form["product"]
        recommendations = recommend(product)

    return render_template(
        "index.html",
        product=product,
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)
