"""Bounded refactor test profile. Lua 5.1, explicit clocks/events, no native game attachment."""
from contextlib import contextmanager
from collections import deque
from dataclasses import dataclass
import re
import xml.etree.ElementTree as ET
from hashlib import sha256
from pathlib import Path
import json
from lupa.lua51 import LuaRuntime as NativeLua51

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {}
RUN = {"executed": {}, "fixture_prefixes": {}, "measurements": {}, "contexts": []}

def executed(key,digest,mode='complete_module',**extra):
    item=RUN['executed'].setdefault(key,{'sha256':digest,'mode':mode,'tests':[]})
    assert item['sha256']==digest, 'SOURCE_CHANGED_DURING_RUN'
    test=RUN.get('active_test')
    if test and test not in item['tests']:item['tests'].append(test)
    item.update(extra)

def completion(key,ok):
    item=RUN['executed'][key]
    item.setdefault('execution_by_test',{})[RUN.get('active_test') or 'fixture']='COMPLETED' if ok else 'FAILED_PARTWAY'

EVENTS = r"""
function eventSource(missing)
 return setmetatable({}, {__index=function(t,name)
  if missing and missing[name] then return nil end
  local callbacks={};local order=nil
  local e={}
  e.Add=function(fn) assert(type(fn)=='function');callbacks[#callbacks+1]=fn end
  e.Remove=function(fn) for i=#callbacks,1,-1 do if callbacks[i]==fn then table.remove(callbacks,i) end end end
  e.Order=function(indices) order=indices end
  e.Count=function() return #callbacks end
  e.Fire=function(...)
   local snapshot={};for i,fn in ipairs(callbacks)do snapshot[i]=fn end
   if order then for _,i in ipairs(order)do assert(snapshot[i],'FIXTURE_LISTENER_ORDER');snapshot[i](...)end
   else for _,fn in ipairs(snapshot)do fn(...)end end
  end
  setmetatable(e,{__call=function(_,...)return e.Fire(...)end});rawset(t,name,e);return e
 end})
end
Events=eventSource();GameEvents=eventSource();LuaEvents=eventSource()
turn=1;Game={GetCurrentGameTurn=function()return turn end,GetLocalPlayer=function()return 0 end}
ExposedMembers={};shared={};counts={};frames=0
ContextPtr={SetUpdate=function()error('HIDDEN_CONTEXT_NO_FRAME',0)end,SetShutdown=function(self,fn)shutdown=fn or self end,SetInitHandler=function(self,fn)init=fn or self end}
function publish()Events.GameCoreEventPublishComplete.Fire()end
"""

def module_path(module):
    """Exact project-relative Lua names, not a model of external include search."""
    if not isinstance(module,str) or not re.fullmatch(r'[A-Za-z0-9_/-]+(?:\.lua)?',module):
        raise ValueError('INVALID_PACKAGE_MODULE')
    parts=module.split('/')
    if any(not part or part in ('.','..') for part in parts):
        raise ValueError('INVALID_PACKAGE_MODULE')
    return module if module.endswith('.lua') else module+'.lua'

@dataclass(frozen=True,init=False)
class PackageVFS:
    """Opt-in package facts plus explicit simulated missing-include behavior.

    Does not claim native include caching, basename aliases, external HD/official
    search or actual native throw/nil semantics. Entry files use Files; include
    files also require ImportFiles. Never changes the package on disk.
    """
    files: frozenset
    imports: frozenset
    absent: frozenset
    missing_include: str
    forbidden_globals: tuple
    manifest_sha256: str

    def __init__(self,absent=(),missing_include='throw',forbidden_globals=(),manifest=None):
        if missing_include not in ('throw','silent_nil'):
            raise ValueError('INVALID_MISSING_INCLUDE_MODE')
        raw=Path(manifest or ROOT/'Mod/SpecializationP0.modinfo').read_bytes()
        doc=ET.fromstring(raw)
        files=frozenset(n.text.strip() for n in doc.findall('./Files/File'))
        imports=frozenset(n.text.strip() for n in doc.findall('./InGameActions/ImportFiles/File'))
        if not files or not imports.issubset(files):raise ValueError('INVALID_PACKAGE_MANIFEST')
        missing=frozenset(module_path(n) for n in absent)
        if not missing.issubset(files):raise ValueError('ABSENT_MODULE_NOT_IN_PACKAGE')
        guards=tuple(forbidden_globals)
        if any(not isinstance(n,str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',n) for n in guards):
            raise ValueError('INVALID_GLOBAL_GUARD')
        guards=tuple(sorted(set(guards)))
        for k,v in dict(files=files,imports=imports,absent=missing,missing_include=missing_include,
                        forbidden_globals=guards,manifest_sha256=sha256(raw).hexdigest()).items():
            object.__setattr__(self,k,v)

    def reason(self,path,included):
        if path not in self.files:return 'NOT_PACKAGED'
        if path in self.absent:return 'ABSENT'
        if included and path not in self.imports:return 'NOT_IMPORTED'
        return None

class Context:
    def __init__(self, name="Gameplay", missing=(), vfs=None, history=None):
        if vfs is not None and not isinstance(vfs,PackageVFS):raise TypeError("INVALID_VFS_PROFILE")
        self.vfs=vfs
        self.history=history
        self.root=history[0] if history else ROOT
        self.loads=deque(maxlen=64)
        self.load_counts={"attempts":0,"missing":0,"completed":0,"failed":0}
        self._load_stack=[]
        self.lua = NativeLua51(unpack_returned_tuples=True)
        self.name = name
        self.lua.execute(EVENTS)
        self.lua.globals().include = self.load if vfs is None else lambda module:self.load(module,included=True)
        if vfs is None:self.load("IdentityEqual")  # Pure production dependency; legacy fixtures may stub include.
        for event in missing:
            self.lua.execute("Events[...] = false", event)
        RUN["contexts"].append({"name":name,"backend":"Lua 5.1","hidden_no_frame":True,**({"package_vfs":vfs.manifest_sha256,"missing_include":vfs.missing_include,"absent":sorted(vfs.absent),"forbidden_globals":list(vfs.forbidden_globals)} if vfs else {})})
        assert self.lua.eval('_VERSION') == 'Lua 5.1'
    def _check_globals(self):
        if self.vfs:
            for name in self.vfs.forbidden_globals:
                if self.lua.globals()[name] is not None:
                    raise AssertionError('FORBIDDEN_PREINJECTED_GLOBAL:'+name)
    def load(self, module, *, included=False):
        if self.vfs:
            self._check_globals()
            relative=module_path(module)
            self.load_counts['attempts']+=1
            row={'module':relative,'included':included,'parent':self._load_stack[-1] if self._load_stack else None}
            self.loads.append(row)
            reason=self.vfs.reason(relative,included)
            if reason:
                self.load_counts['missing']+=1;row['status']=reason
                if included and self.vfs.missing_include=='silent_nil':return None
                raise FileNotFoundError('PACKAGE_'+reason+':'+relative)
            path=self.root/'Mod'/relative
            if not path.resolve().is_relative_to((self.root/'Mod').resolve()):
                row['status']='OUTSIDE_MOD';raise ValueError('PACKAGE_PATH_OUTSIDE_MOD')
        else:
            path=self.root/'Mod'/(module if module.endswith('.lua') else module+'.lua')
        try:text=path.read_text()
        except OSError:
            if self.vfs:self.load_counts['failed']+=1;row['status']='FILE_READ_FAILED'
            raise
        key=str(path.relative_to(self.root))
        if self.history:key='historical/'+self.history[1]+'/'+key
        digest=sha256(text.encode()).hexdigest()
        executed(key,digest)
        self._load_stack.append(key)
        try:
            result=self.lua.execute(text)
            self._check_globals()
        except Exception:
            completion(key,False)
            if self.vfs:self.load_counts['failed']+=1;row['status']='FAILED_PARTWAY'
            raise
        finally:self._load_stack.pop()
        completion(key,True)
        if self.vfs:self.load_counts['completed']+=1;row['status']='COMPLETED'
        return result
    def fragment(self,path,start,end):
        text=(ROOT/path).read_text();assert text.count(start)==1 and text.count(end)==1
        fragment=text[text.index(start):text.index(end)]
        executed(path+':'+start,sha256(text.encode()).hexdigest(),'source_fragment',fragment_sha256=sha256(fragment.encode()).hexdigest(),start=start,end=end)
        return fragment
    def prefix(self, path, boundary):
        path=ROOT/path;text=path.read_text();assert text.count(boundary)==1
        source=text.split(boundary)[0]
        RUN['fixture_prefixes'][str(path.relative_to(ROOT))]={'sha256':sha256(source.encode()).hexdigest(),'boundary':boundary,'mode':'fixture_prefix_not_full_test'}
        return source
    def execute(self, source, *args):return self.lua.execute(source,*args)
    def eval(self, source):return self.lua.eval(source)
    def globals(self):return self.lua.globals()
    def table(self, value):
        if isinstance(value,dict):return self.lua.table_from({k:self.table(v) for k,v in value.items()})
        if isinstance(value,list):return self.lua.table_from([self.table(v) for v in value])
        assert value is None or isinstance(value,(bool,int,float,str)), 'FIXTURE_NATIVE_OBJECT_RETAINED'
        return value
    def snapshot(self, value):
        # A host JSON round-trip copies only explicitly retained fixture scalars/tables.
        return json.loads(json.dumps(value,allow_nan=False))
    def reload(self, retained, name=None):
        result=Context(name or self.name,vfs=self.vfs,history=self.history);result.globals().retained=result.table(self.snapshot(retained));return result

def measure(name, values):
    assert name not in RUN['measurements'], 'DUPLICATE_MEASUREMENT'
    RUN['measurements'][name]=json.loads(json.dumps(values,allow_nan=False))

@contextmanager
def legacy_source_observation():
    """Track source reads separately; never mislabel a read as executed Lua."""
    from unittest.mock import patch
    original=Path.read_text
    def read(path,*a,**kw):
        value=original(path,*a,**kw)
        if path.is_relative_to(ROOT/'Mod'):
            key=str(path.relative_to(ROOT));digest=sha256(value.encode()).hexdigest();SOURCES[digest]=key
            RUN.setdefault('inherited_source_reads',{})[key]=digest
        return value
    with patch.object(Path,'read_text',read):yield

class TrackedLua51:
    def __init__(self,*args,**kwargs):
        self._lua=NativeLua51(*args,**kwargs)
        self.execute((ROOT/"Mod/IdentityEqual.lua").read_text()) # Explicit dependency for frozen include stubs.
    def __getattr__(self,key):return getattr(self._lua,key)
    def execute(self,source,*args,**kwargs):
        digest=sha256(source.encode() if isinstance(source,str) else source).hexdigest()
        key=SOURCES.get(digest)
        if key:executed(key,digest)
        try:result=self._lua.execute(source,*args,**kwargs)
        except Exception:
            if key:completion(key,False)
            raise
        if key:completion(key,True)
        return result


def separate_legacy_event_namespaces(source):
    """Explicit native-double profile only; real Events/GameEvents are distinct.
    Frozen fixture source and every property assertion remain unchanged.
    """
    assert source.count('GameEvents=Events')==1,'FIXTURE_NAMESPACE_PROFILE_CHANGED'
    RUN.setdefault('fixture_profiles',{})['separate_legacy_event_namespaces']='Replace historical alias with distinct GameEvents callback storage; no assertion/runtime-source changes.'
    return source.replace('GameEvents=Events',"GameEvents=setmetatable({},{__index=function(t,k)local e={Add=function(f)local key='GameEvents.'..k;hooks[key]=hooks[key]or{};table.insert(hooks[key],f)end};rawset(t,k,e);return e end})")
