"""Roundtrip/rollback safety in temporary directories only; never touches game runtime."""
import sys,tempfile,subprocess,shutil,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
import temporary_playtest as t

def rejected(f):
 try:f()
 except (ValueError,RuntimeError):return
 raise AssertionError('unsafe switch accepted')
with tempfile.TemporaryDirectory(prefix='spc-temp-playtest-test-') as td:
 p=Path(td).resolve();stable=p/'main';dev=p/'develop';target=p/'Game/Mods/SpecializationP0'
 for root,branch in [(stable,'main'),(dev,'develop')]:
  shutil.copytree(R/'Mod',root/'Mod')
  def git(*args):subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
  git('init','-b',branch);git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid')
  if branch=='develop':(root/'Mod/develop-only.txt').write_text('roundtrip must remove this')
  git('add','.');git('commit','-m','fixture')
 shutil.copytree(stable/'Mod',target);original=t.d.snapshot(target)
 current=t.d.snapshot(dev/'Mod');archive=target.parent.parent/'SpecializationDeploymentBackups'
 receipt=archive/'test.json'
 def activate(**kw):return t.switch(dev/'Mod',target,receipt,stable,current['digest'],original['digest'],**kw)
 rejected(lambda:activate())
 def fail():raise RuntimeError('injected after runtime rename')
 rejected(lambda:activate(authorized=True,failpoint=fail))
 assert t.d.snapshot(target)==original and not (target.parent/'.specialization-deploy-pending.json').exists()
 receipt=archive/'test2.json';record=activate(authorized=True)
 assert record['phase']=='DEVELOP_ACTIVE' and t.d.snapshot(target)==current
 backup=Path(record['stable_backup']);assert t.d.snapshot(backup)==original
 assert target.parent not in backup.parents
 (target/'unexpected.txt').write_text('preserve')
 rejected(lambda:t.switch(backup,target,receipt,stable,original['digest'],current['digest'],restore=True,authorized=True))
 assert (target/'unexpected.txt').exists();(target/'unexpected.txt').unlink()
 restored=t.switch(backup,target,receipt,stable,original['digest'],current['digest'],restore=True,authorized=True)
 assert restored['phase']=='STABLE_RESTORED' and t.d.snapshot(target)==original
 assert not (target/'develop-only.txt').exists() and t.d.snapshot(backup)==original
 assert len(list(target.parent.rglob('*.modinfo')))==1
print('LOCAL_SIMULATION_PASS temporary switch: authorization, stable match, hash gates, rollback, exact restore including develop-only removal, retained backups outside Mods.')
