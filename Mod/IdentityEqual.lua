-- Object identity without optional Lua raw helpers. Table keys bypass __eq.
-- No registry, retained references, native reads, saved state or global overrides.
SPCIdentityEqual={}
function SPCIdentityEqual.Same(a,b)
 local kind=type(a)
 if kind~=type(b)then return false end
 if kind=='table'or kind=='userdata'then
  return ({[a]=true})[b]==true
 end
 return a==b
end
