"""Bounded refactor test profile. Lua 5.1, explicit clocks/events, no native game attachment."""
from contextlib import contextmanager
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

class Context:
    def __init__(self, name="Gameplay", missing=()):
        self.lua = NativeLua51(unpack_returned_tuples=True)
        self.name = name
        self.lua.execute(EVENTS)
        self.lua.globals().include = self.load
        for event in missing:
            self.lua.execute("Events[...] = false", event)
        RUN["contexts"].append({"name":name,"backend":"Lua 5.1","hidden_no_frame":True})
        assert self.lua.eval('_VERSION') == 'Lua 5.1'
    def load(self, module):
        path=ROOT/'Mod'/(module if module.endswith('.lua') else module+'.lua')
        text=path.read_text();key=str(path.relative_to(ROOT));digest=sha256(text.encode()).hexdigest()
        executed(key,digest)
        try:result=self.lua.execute(text)
        except Exception:
            completion(key,False);raise
        completion(key,True);return result
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
        result=Context(name or self.name);result.globals().retained=result.table(self.snapshot(retained));return result

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
    def __init__(self,*args,**kwargs):self._lua=NativeLua51(*args,**kwargs)
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
