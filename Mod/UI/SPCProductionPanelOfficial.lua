-- The shipped Heroes mode replaces ProductionPanel when this Game setting is on.
local heroes=GameConfiguration.GetValue('GAMEMODE_HEROES')
if heroes==true or heroes==1 then
 include('ProductionPanel_Babylon_Heroes')
else
 include('ProductionPanel')
end
SPCOfficialProductionBase=true
include('CrewProjectOrder')
