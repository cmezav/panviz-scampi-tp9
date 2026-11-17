"""Regresión de acceso local; no modifica v1.json ni v2.json."""
import importlib.util
import json
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from http.server import HTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, build_opener, HTTPCookieProcessor, HTTPRedirectHandler

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'04_prototipo'))
import panviz

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args):return None

class AccessTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.pilot=panviz.Pilot('v2',Path(self.tmp.name))
        self.server=HTTPServer(('127.0.0.1',0),panviz.handler(self.pilot))
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.url='http://127.0.0.1:'+str(self.server.server_port)
        self.jar=CookieJar();self.client=build_opener(HTTPCookieProcessor(self.jar),NoRedirect())
        self.sample=(ROOT/'04_prototipo/datos/muestra.csv').read_bytes()
    def tearDown(self):
        self.server.shutdown();self.thread.join();self.server.server_close();self.tmp.cleanup()
    def call(self,path,body=None,headers=None,client=None):
        data=json.dumps(body).encode() if isinstance(body,dict) else body
        hdr={'X-PANVIZ-Request':'1',**(headers or {})}
        request=Request(self.url+path,data=data,headers=hdr)
        try:r=(client or self.client).open(request,timeout=5)
        except HTTPError as e:r=e
        with r:return r.code,r.read(),r.headers
    def login(self,user,password):
        code,body,headers=self.call('/api/login',{'usuario':user,'clave':password})
        self.assertEqual(code,200,body);return headers
    def test_01_anonymous(self):
        self.assertEqual(self.call('/')[0],303)
        self.assertEqual(self.call('/login')[0],200)
        self.assertEqual(self.call('/api/resumen')[0],401)
        self.assertEqual(self.call('/artefacto/04_prototipo/datos/muestra.csv')[0],303)
    def test_02_credentials_and_cookie(self):
        self.assertEqual(self.call('/api/login',{'usuario':'lector','clave':'incorrecta'})[0],401)
        headers=self.login('lector','LecturaPANVIZ!26')
        cookie=headers['Set-Cookie'];self.assertIn('HttpOnly',cookie);self.assertIn('SameSite=Strict',cookie)
        self.assertEqual(json.loads(self.call('/api/session')[1])['rol'],'lector')
    def test_03_reader_cannot_write_or_forge_role(self):
        self.pilot.load(self.sample.decode());before=(self.pilot.state/'importacion.json').read_bytes()
        self.login('lector','LecturaPANVIZ!26')
        self.assertEqual(self.call('/api/resumen')[0],200)
        self.assertEqual(self.call('/api/importar',self.sample)[0],403)
        self.assertEqual(self.call('/api/publicar',{'rol':'publicador_simulado'})[0],403)
        self.assertEqual((self.pilot.state/'importacion.json').read_bytes(),before)
        self.assertFalse((self.pilot.state/'publicado.json').exists())
    def test_04_publisher_can_write(self):
        self.login('publicador','PublicaPANVIZ!26')
        code,raw,_=self.call('/api/importar',self.sample);self.assertEqual(code,200)
        self.assertEqual(len(json.loads(raw)['aceptados']),24)
        self.assertEqual(self.call('/api/publicar',{'rol':'lector'})[0],200)
        self.assertTrue((self.pilot.state/'publicado.json').is_file())
    def test_05_logout_invalidates_session(self):
        self.login('publicador','PublicaPANVIZ!26')
        stolen='; '.join(c.name+'='+c.value for c in self.jar)
        self.assertEqual(self.call('/api/logout',{})[0],200)
        self.assertEqual(self.call('/api/session')[0],401)
        plain=build_opener(NoRedirect())
        self.assertEqual(self.call('/api/session',headers={'Cookie':stolen},client=plain)[0],401)
    def test_06_origin_and_invalid_session(self):
        self.assertEqual(self.call('/api/login',{'usuario':'lector','clave':'LecturaPANVIZ!26'},headers={'Origin':'http://otro.example'})[0],403)
        self.assertEqual(self.call('/api/login',{'usuario':'lector','clave':'LecturaPANVIZ!26'},headers={'X-PANVIZ-Request':''})[0],403)
        plain=build_opener(NoRedirect())
        self.assertEqual(self.call('/api/session',headers={'Cookie':'panviz_session=invalid'},client=plain)[0],401)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(AccessTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    data={'fecha_utc':datetime.now(timezone.utc).isoformat(),'alcance':'Acceso local con sesiones; pruebas adicionales, separadas del corte histórico v1/v2','ejecutadas':result.testsRun,'fallidas':len(result.failures),'errores':len(result.errors),'aprobadas':result.testsRun-len(result.failures)-len(result.errors)}
    output=ROOT/'05_pruebas/resultados/acceso_local.json';output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
