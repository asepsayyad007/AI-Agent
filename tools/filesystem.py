from pathlib import Path
from config import WORKSPACE

def _resolve(path:str):
 p=(WORKSPACE/path).resolve(); w=WORKSPACE.resolve();
 try:p.relative_to(w);return True,p
 except ValueError:return False,p

def _err(msg): return {"success":False,"error":msg}

def read_file(path):
 ok,p=_resolve(path)
 if not ok:return _err("Access denied")
 try:return {"success":True,"content":p.read_text(encoding="utf-8")}
 except Exception as e:return _err(str(e))

def write_file(path,content):
 ok,p=_resolve(path)
 if not ok:return _err("Access denied")
 try:p.parent.mkdir(parents=True,exist_ok=True); existed=p.exists(); p.write_text(content,encoding="utf-8"); return {"success":True,"created":not existed}
 except Exception as e:return _err(str(e))

def delete_file(path):
 ok,p=_resolve(path)
 if not ok:return _err("Access denied")
 try:p.unlink(); return {"success":True}
 except Exception as e:return _err(str(e))

def list_directory(path=""):
 ok,p=_resolve(path)
 if not ok:return _err("Access denied")
 try:return {"success":True,"items":[i.name for i in p.iterdir()]}
 except Exception as e:return _err(str(e))

def exists(path):
 ok,p=_resolve(path)
 if not ok:return _err("Access denied")
 return {"success":True,"exists":p.exists()}
