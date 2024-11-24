from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    try:
        registration_no = request.json['numberrange']
        tree = ET.parse('data.xml')  # Path to your XML file
        root = tree.getroot()

        results = []
        for child in root:
            if child.attrib.get('registration_no') == registration_no:
                result = {
                    'name': child.find('name').text,
                    'phone_no': child.find('phone_no').text,
                    'address': child.find('address').text,
                    'registration_no': child.attrib.get('registration_no')
                }
                results.append(result)

        return jsonify(results)

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
