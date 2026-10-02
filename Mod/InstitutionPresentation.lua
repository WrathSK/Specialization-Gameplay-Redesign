-- U1 bounded Research display model. No gameplay calls or mutations.
SPCInstitutionPresentation={}
local M=SPCInstitutionPresentation
M.Rows={
{level=1,name="学者结社",text="学者在此结成稳定的研究共同体，构成城市科研专业化的基础。[NEWLINE][NEWLINE]基础专家支持[NEWLINE]每名工作的科研专家额外获得3食物、3生产力。"},
{level=2,name="研修院",text="系统的研修与人才培养，使科研从个人志业成为城市的长期事业。[NEWLINE][NEWLINE]人才培养[NEWLINE]每名正在工作的科研专家额外提供2点基础大科学家点数，并受到其它伟人点数百分比加成。本城学院区域及其每一级建筑各提供1点住房。[NEWLINE][NEWLINE]"},
{level=3,name="学术联合会",text="不同专业领域在此交流，使研究成果与城市实践相互促进。[NEWLINE][NEWLINE]跨学科研究[NEWLINE]本城学院以外的合格专业区域，将基础相邻产出总和的50%转化为科技值。只计算已完成且未被掠夺的区域；不计政策等相邻倍率或其它非相邻产出。适用区域见专业领域表。 当前测试版：汇总后向下取整。[NEWLINE][NEWLINE]学以致用[NEWLINE]每名正在工作的科研专家，从本城每个合格的其它专业领域获得对应产出。该领域每有1点基础设施深度，便提供0.5份对应产出；金币每份为3点，其它产出每份为1点。同产出领域分别计算并相加，同领域多个区域取最高单基础设施深度。 当前测试版：每名专家的各项收益先向下取整，再按人数结算。[NEWLINE][NEWLINE]"},
{level=4,name="学术总署",text="完善的科研设施、学术组织与长期传统，共同支撑深入研究。[NEWLINE][NEWLINE]科研基础设施[NEWLINE]学院每有1点基础设施深度，每名正在工作的科研专家额外提供1点基础科技值。基础设施深度最高10点；达到10点时，5名专家共增加50点基础科技值。[NEWLINE][NEWLINE]学术主持[NEWLINE]每名正在工作的科研专家，使本城每座普通学院一至四级建筑额外提供1点基础科技值。被掠夺的建筑不计入，也不接受此收益。这些额外科技不会提高基础设施深度。[NEWLINE][NEWLINE]学术传统[NEWLINE]本城首次达到科研专业潜力4级后，学术传统开始积累：起始使本城科技值提高5%；标准速度下，满10、20、30、40回合分别提高至10%、15%、20%、25%，最高25%。其它速度按游戏速度同比缩放各阶段回合数并向下取整。仍保有科研专业身份时，即使暂未启用4级能力，传统仍继续积累。转出科研后停止积累但保留已累计年限；重新成为科研时继续积累，不补算离开期间的回合。启用4级能力后按保留的传统年限生效。[NEWLINE][NEWLINE]"}
}
function M.Matches(v,pid,cid,x,y)
 return type(v)=='table' and not v.error and v.owner==pid and v.cityID==cid and v.x==x and v.y==y
  and v.specialization=='RESEARCH' and type(v.potential)=='number' and v.potential>=1 and v.potential<=4
end
function M.Filter(data,owned)
 -- Copy only display tables we change; never edit CitySupport's shared data.
 local out={};for k,v in pairs(data) do out[k]=v end
 out.BuildingsAndDistricts={}
 for _,d in ipairs(data.BuildingsAndDistricts or {}) do
  local nd={};for k,v in pairs(d) do nd[k]=v end;nd.Buildings={}
  for _,b in ipairs(d.Buildings or {}) do if not owned[b.Type] then nd.Buildings[#nd.Buildings+1]=b end end
  out.BuildingsAndDistricts[#out.BuildingsAndDistricts+1]=nd
 end
 return out
end
function M.Tooltip(level,v)
 local state='ACTIVE暂不可确认'
 if type(v.active)=='number' and v.activeStatus~='UNKNOWN' then state=v.active>=(M.Rows[level].level or level) and '已达到本阶段启用等级；实际收益仍按各能力条件结算' or '本阶段能力暂未激活；机构仍保留' end
 return M.Rows[level].name..'[NEWLINE]'..state..'[NEWLINE][NEWLINE]'..M.Rows[level].text
end
