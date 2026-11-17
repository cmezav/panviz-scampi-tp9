"""Cuentas de demostración y sesiones locales PANVIZ. Solo biblioteca estándar."""
import hashlib
import hmac
import json
import secrets
import time
from http.cookies import SimpleCookie
from urllib.parse import urlsplit

USERS = {'lector': {'role': 'lector', 'salt': '7a0640be472a006bbddbb2be7c16ecc3', 'digest': '9390447a8baad6aae84be14678b22f1996b4c4abbdff2fc465f1281a15c550a2'}, 'publicador': {'role': 'publicador', 'salt': '6fc0954a83abd4897c7c1ae5e641b1a9', 'digest': 'dada1c7eef809795259b3e8c06820b7606ba23830c8f7b287c54347a90ecb91f'}}
COOKIE = 'panviz_session'
SESSION_SECONDS = 3600


def protect(base, pilot, here):
    sessions = {}
    failures = {}

    class AuthenticatedHandler(base):
        def session(self):
            try:
                cookies = SimpleCookie(self.headers.get('Cookie', ''))
                token = cookies[COOKIE].value if COOKIE in cookies else ''
            except Exception:
                token = ''
            now = time.monotonic()
            for key in [key for key, value in sessions.items() if value['expires'] <= now]:
                del sessions[key]
            return token, sessions.get(token)

        def reply(self, code, data=None, cookie=None, location=None):
            body = b'' if data is None else json.dumps(data, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            if cookie is not None:
                self.send_header('Set-Cookie', cookie)
            if location:
                self.send_header('Location', location)
            self.end_headers()
            self.wfile.write(body)

        def valid_host(self):
            try:
                return urlsplit('//'+self.headers.get('Host', '')).hostname in {'localhost', '127.0.0.1', '::1'}
            except ValueError:
                return False

        def do_GET(self):
            if not self.valid_host():
                return self.reply(403, {'mensaje':'Servidor reservado para acceso local.'})
            route = urlsplit(self.path).path
            token, user = self.session()
            if route == '/login':
                if user:
                    return self.reply(303, location='/')
                return self.respond(200, (here/'login.html').read_bytes(), 'text/html; charset=utf-8')
            if route == '/api/session':
                if not user:
                    return self.reply(401, {'mensaje':'Inicia sesión para continuar.'})
                return self.reply(200, {'usuario':user['username'], 'rol':user['role']})
            if not user:
                if route.startswith('/api/'):
                    return self.reply(401, {'mensaje':'Inicia sesión para continuar.'})
                return self.reply(303, location='/login')
            return super().do_GET()

        def do_POST(self):
            if not self.valid_host():
                return self.reply(403, {'mensaje':'Servidor reservado para acceso local.'})
            origin = self.headers.get('Origin')
            if self.headers.get('X-PANVIZ-Request') != '1' or (origin and urlsplit(origin).netloc.lower() != self.headers.get('Host','').lower()):
                return self.reply(403, {'mensaje':'Origen de solicitud no permitido.'})
            route = urlsplit(self.path).path
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 <= length <= 250000:
                    return self.reply(413, {'mensaje':'Tamaño no permitido.'})
            except ValueError:
                return self.reply(400, {'mensaje':'Solicitud inválida.'})
            if route in {'/api/login', '/api/logout', '/api/publicar'}:
                raw = self.rfile.read(length)
            if route == '/api/login':
                now = time.monotonic()
                key = self.client_address[0]
                recent = [t for t in failures.get(key, []) if now-t < 60]
                if len(recent) >= 8:
                    return self.reply(429, {'mensaje':'Demasiados intentos. Espera un minuto.'})
                try:
                    data = json.loads(raw)
                    if not isinstance(data, dict):raise ValueError()
                    username = data.get('usuario', '')
                    password = data.get('clave', '')
                    if not isinstance(username,str) or not isinstance(password,str) or len(username)>64 or len(password)>128:raise ValueError()
                    username = username.strip().lower()
                except (ValueError, UnicodeDecodeError):
                    return self.reply(400, {'mensaje':'Completa usuario y contraseña.'})
                account = USERS.get(username)
                # Always perform a hash, including for unknown usernames.
                check = account or next(iter(USERS.values()))
                digest = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(check['salt']), 240000).hex()
                if not account or not hmac.compare_digest(digest, check['digest']):
                    failures[key] = recent+[now]
                    return self.reply(401, {'mensaje':'Usuario o contraseña incorrectos.'})
                failures.pop(key, None)
                previous, _ = self.session()
                sessions.pop(previous, None)
                token = secrets.token_urlsafe(32)
                sessions[token] = {'username':username, 'role':account['role'], 'expires':now+SESSION_SECONDS}
                return self.reply(200, {'usuario':username, 'rol':account['role']}, cookie=f'{COOKIE}={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={SESSION_SECONDS}')
            token, user = self.session()
            if not user:
                return self.reply(401, {'mensaje':'Inicia sesión para continuar.'})
            if route == '/api/logout':
                sessions.pop(token, None)
                return self.reply(200, {'mensaje':'Sesión cerrada.'}, cookie=f'{COOKIE}=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0')
            if route == '/api/publicar':
                # Ignore any role sent by the browser. Only the server session grants permissions.
                code, body = pilot.publish('publicador_simulado' if user['role']=='publicador' else 'lector')
                if code == 403:
                    body={'mensaje':'Tu cuenta de lector no tiene permiso para publicar.'}
                return self.reply(code, body)
            if route == '/api/importar' and user['role'] != 'publicador':
                return self.reply(403, {'mensaje':'Tu cuenta de lector no tiene permiso para importar ni corregir registros.'})
            return super().do_POST()

    return AuthenticatedHandler
