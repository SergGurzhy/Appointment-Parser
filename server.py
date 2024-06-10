from flask import Flask, request, redirect, make_response
import json
import urllib.parse

app = Flask(__name__)


@app.route('/restore_session')
def restore_session():
    url = request.args.get('url')
    encoded_cookies = request.args.get('cookies')
    encoded_local_storage = request.args.get('local_storage')
    encoded_session_storage = request.args.get('session_storage')

    # Декодируем данные из URL-формата в JSON
    cookies_json = urllib.parse.unquote(encoded_cookies)
    local_storage_json = urllib.parse.unquote(encoded_local_storage)
    session_storage_json = urllib.parse.unquote(encoded_session_storage)

    cookies = json.loads(cookies_json)
    local_storage = json.loads(local_storage_json)
    session_storage = json.loads(session_storage_json)

    response = make_response(redirect(url))

    # Устанавливаем куки
    for cookie in cookies:
        response.set_cookie(cookie['name'], cookie['value'], domain=cookie.get('domain'), path=cookie.get('path', '/'))

    # JavaScript для установки localStorage и sessionStorage
    set_storage_script = """
    <script>
    function setStorage(type, data) {
        for (const [key, value] of Object.entries(data)) {
            window[type].setItem(key, value);
        }
    }
    setStorage('localStorage', JSON.parse(decodeURIComponent('%s')));
    setStorage('sessionStorage', JSON.parse(decodeURIComponent('%s')));
    window.location.href = '%s';
    </script>
    """ % (urllib.parse.quote(local_storage_json), urllib.parse.quote(session_storage_json), url)

    response.data = set_storage_script
    response.headers['Content-Type'] = 'text/html'

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
