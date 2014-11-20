function booleanres = isPointinEdge(pid,eid)
    global Edge Point
    
    if Edge(eid,1) == pid || Edge(eid,2) == pid
        booleanres = true;
    else
        booleanres = false;
    endif
end %function