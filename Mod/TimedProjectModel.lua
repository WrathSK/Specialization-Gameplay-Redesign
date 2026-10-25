-- Pure queue facts only; each project retains qualification/completion policy.
SPCTimedProjectModel={}
function SPCTimedProjectModel.ClassifyQueue(target,size,project)
 if type(target)=='string'and target~=''and target~=project then return 'OTHER'end
 if target==project then
  if size==1 then return 'CURRENT'end
  if type(size)=='number'and size>1 and size%1==0 then return 'MULTIPLE'end
 elseif target==nil or target==''then
  if size==0 then return 'EMPTY'end
 end
 return 'UNKNOWN'
end

-- Shared clock facts only. Each owner decides writes, cancellation and proof.
function SPCTimedProjectModel.Boundary(start,ended,now,ending)
 if ending then return now==start and 'END'or 'WAIT'end
 if now>start then return now==start+1 and ended and 'DUE'or 'MISSED'end
 return 'WAIT'
end
