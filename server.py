from flask import Flask, request, redirect, make_response
import json
import urllib.parse

app = Flask(__name__)


@app.route('/restore_session')
def restore_session():
    encoded_session_data = request.args.get('data')

    # Декодируем данные из URL-формата в JSON
    session_data_json = urllib.parse.unquote(encoded_session_data)
    session_data = json.loads(session_data_json)

    url = session_data['url']
    cookies = session_data['cookies']

    response = make_response(redirect(url))

    for cookie in cookies:
        if not cookie.get('httpOnly'):
            response.set_cookie(cookie['name'], cookie['value'], domain=cookie.get('domain'),
                                path=cookie.get('path', '/'))

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

