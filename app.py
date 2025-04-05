from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/shell-pakistan-prices', methods=['GET'])
def get_prices():
    url = "https://www.shell.com.pk/motorists/shell-fuels/shell-station-price-board.html"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    price_table = soup.find('table')

    if not price_table:
        return jsonify({"error": "Table not found"}), 404

    prices = []
    for row in price_table.find_all('tr')[1:]:  # Skip header
        cols = row.find_all('td')
        if len(cols) >= 2:
            product = cols[0].get_text(strip=True)
            price = cols[1].get_text(strip=True)
            prices.append({
                "product": product,
                "price": price
            })

    return jsonify(prices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
