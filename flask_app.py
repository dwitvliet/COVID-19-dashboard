from flask import Flask, request

from config import cloud_run_token
import update_database


app = Flask(__name__)


@app.route('/', methods=['GET'])
def run():
    # Ensure request is authenticated.
    request_token = request.args.get('token')
    if request_token != cloud_run_token:
        return

    update_database.main()

    return 'Completed'

    
if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=8080, debug=True)
