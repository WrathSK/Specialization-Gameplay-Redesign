"""Frozen B1/A-D2 suites, explicit B2 deltas only; never edit historical tests."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_p0_b1.py').read_text()
# Source guard now permits the eight B2 files; test_p0_b2 protects all others.
s=s.replace("allowed={", "allowed={'Lv2Housing.lua','Lv2GPP.lua','OrdinaryBuildingCatalog.lua',")
s=s.replace('区域完善度 / 科研影子','基础设施 / Lv2住房与专家')
s=s.replace('079.106','080.107').replace("=='106'", "=='107'")
# Nested historical P0-A source guard is a B1/B2 allowlist, not an old-byte oracle
# for writers intentionally cut over. Housing/GPP are compared by test_p0_b2.
s=s.replace('p0=p0.replace("\'ResearchSupport.lua\',",\'\')','p0=p0.replace("\'Lv2Housing.lua\',",\'\').replace("\'Lv2GPP.lua\',",\'\')\n p0=p0.replace("\'ResearchSupport.lua\',",\'\')')
# P0-A request fixture predates the combined Lv2 report: explicit read-only stubs.
s=s.replace("p0=p0.replace(\"'ResearchSupport.lua',\",'')", "p0=p0.replace(\"'ResearchSupport.lua',\",'')\n p0=p0.replace('shared.Version=P.VERSION', \"shared.Version=P.VERSION;shared.Lv2Housing={Describe=function() return 'housing fixture' end};shared.Lv2GPP={Describe=function() return 'gpp fixture' end}\")")
# Load the real existing UI rate renderer in the old panel fixture.
s=s.replace('p0=p0.replace("\'ResearchSupport.lua\',",\'\')','p0=p0.replace("\'ResearchSupport.lua\',",\'\')\n p0=p0.replace("u.execute((M/\'UI/P0Panel.lua\').read_text())", "u.execute((M/\'GPPReadout.lua\').read_text());u.execute((M/\'UI/P0Panel.lua\').read_text())")')
sys.argv=[__file__,'--regression']
exec(compile(s,'B1_B2_explicit_writer_contract_delta','exec'),{'__file__':str(R/'DevelopmentTests/test_p0_b1.py')})
