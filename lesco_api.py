from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_bill_details(reference_number):
    url = f"https://bill.pitc.com.pk/lescobill?ref={reference_number}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Bill details extract karna
        bill_info = {}
        bill_data = soup.find_all("td")  # Modify karna hoga website structure ke mutabiq

        if len(bill_data) > 10:  
            bill_info["Reference Number"] = reference_number
            bill_info["Consumer Name"] = bill_data[1].text.strip()
            bill_info["Billing Month"] = bill_data[3].text.strip()
            bill_info["Due Date"] = bill_data[5].text.strip()
            bill_info["Bill Amount"] = bill_data[7].text.strip()
            bill_info["Payable Amount"] = bill_data[9].text.strip()
        else:
            return {"error": "Invalid Reference Number or No Bill Found"}

        return bill_info
    else:
        return {"error": "Failed to fetch data from LESCO"}

@app.route('/lesco-bill', methods=['GET'])
def lesco_bill():
    reference_number = request.args.get('ref')
    if not reference_number:
        return jsonify({"error": "Reference number is required"}), 400

    bill_details = get_bill_details(reference_number)
    return jsonify(bill_details)

if __name__ == '__main__':
    app.run(debug=True)
