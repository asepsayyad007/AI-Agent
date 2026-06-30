import subprocess

def run(command:str,cwd=None,timeout=300):
 try:
  r=subprocess.run(command,shell=True,capture_output=True,text=True,cwd=cwd,timeout=timeout)
  return {"success":r.returncode==0,"stdout":r.stdout,"stderr":r.stderr,"returncode":r.returncode}
 except subprocess.TimeoutExpired:
  return {"success":False,"stderr":"Command timed out","returncode":-1}
