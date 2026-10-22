-- B268 presentation only. Native district pixels stay owned by the engine.
SPCClaimIconOverlay={}
local claims={}
for _,key in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do claims['ICON_PROJECT_SPC_CLAIM_'..key]=true end
function SPCClaimIconOverlay.New()
 local entries=setmetatable({},{__mode='k'})
 local function apply(parent,icon)
  if not parent then return end
  local e=entries[parent]
  if not claims[icon]then if e then e.Root:SetHide(true)end;return end
  if not e then
   e={};ContextPtr:BuildInstanceForControl('SPCClaimIconInstance',e,parent);entries[parent]=e
  end
  local size=math.max(10,math.floor(math.min(parent:GetSizeX(),parent:GetSizeY())*.48+.5))
  -- B256 native regression: the selected atlas cell and Image must match.
  -- Quantize the decorative mark, never crop a larger cell into a smaller Image.
  local source=12
  for _,n in ipairs({12,16,20,22,24,30,32,38,40,48,50,64,70,80,95,128,200,256})do
   if math.abs(n-size)<math.abs(source-size)then source=n end
  end
  e.Root:SetSizeVal(source,source);e.Mark:SetIcon('ICON_SPC_RAW_CLAIM_MARK',source);e.Mark:SetSizeVal(source,source)
  e.Root:SetHide(false)
 end
 LuaEvents.SPC_ClaimIconDecorate.Add(apply)
 return {Stop=function()
  LuaEvents.SPC_ClaimIconDecorate.Remove(apply)
  -- Cross-context children may outlive their creator. Expired parents are guarded.
  for parent,e in pairs(entries)do pcall(function()parent:DestroyChild(e.Root)end)end
  entries=setmetatable({},{__mode='k'})
 end}
end
