from flask import Flask, request
from functions import handle_messages
app = Flask(__name__)



@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        print('GET request traitement ...')
    else:
        # Incoming messages will trigger a POST request
        incoming_message = request.get_json()
        handle_messages(incoming_message)
        return 'Message received', 200


        
if __name__ == '__main__':
    app.run(port=5000)
