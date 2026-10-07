include('NetworkInput')
SPCInspirationReadout={}
local baseline
function SPCInspirationReadout.Render(P,view,token,action)
 local function tr(k,...)return Locale.Lookup('LOC_SPC_INSPIRE_'..k,...)end
 if not view or view.token~=token or view.owner~=Game.GetLocalPlayer()then baseline=nil;return tr('READ_UNKNOWN')end
 local c=Players[view.owner]:GetCities():FindID(view.city)
 if not c or SPCNetworkInput.Reference(c)~=view.reference then baseline=nil;return tr('READ_UNKNOWN')end
 local ok,rate=pcall(function()return Players[view.owner]:GetGreatPeoplePoints():GetPointsPerTurn(P.Info('GreatPersonClasses','GREAT_PERSON_CLASS_SCIENTIST').Index)end)
 if not ok or type(rate)~='number' or rate~=rate or math.abs(rate)==math.huge then return tr('READ_UNKNOWN')end
 local turn=Game.GetCurrentGameTurn()
 if view.stage==0 then baseline={rate=rate,turn=turn,reference=view.reference,session=view.session}end
 local text=tr('TURN',turn)..'\n'..tr('NATIVE',string.format('%.3f',rate))
 if baseline and baseline.turn==turn and baseline.reference==view.reference and (baseline.session==view.session or action=='INSPIRE_END')then
  text=text..'\n'..tr('DELTA',string.format('%.3f',rate-baseline.rate))
 else text=text..'\n'..tr('NO_BASELINE')end
 if view.stage<0 then baseline=nil end
 return text..'\n'..tr('SCOPE')
end
