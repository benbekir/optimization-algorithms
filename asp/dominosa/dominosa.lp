% vertically adjacent cells
adj(R1,C1,R2,C2) :- cell(R1,C1,_), cell(R2,C2,_), R2 = R1 + 1, C1 = C2.
% horizontally adjacent cells
adj(R1,C1,R2,C2) :- cell(R1,C1,_), cell(R2,C2,_), C2 = C1 + 1, R1 = R2.

% GUESS which adjacent cells are pairs.
{ pair(R1,C1,R2,C2) : adj(R1,C1,R2,C2) }.
% if R1,C1,R2,C2 is a pair, then R2,C2,R1,C1 is also a pair
pair(R2,C2,R1,C1) :- pair(R1,C1,R2,C2). 
% CHECK that one cell is part of at most one pair
:- pair(R1,C1,R2,C2), pair(R1,C1,R3,C3), (R2,C2) != (R3,C3).
% CHECK that one cell is part of at least one pair 
:- cell(R,C,_), not pair(R,C,_,_).
% CHECK that for every distinct pair, the values are unique 
:- pair(R1,C1,R2,C2), pair(R3,C3,R4,C4), 
    (R1,C1,R2,C2) != (R3,C3,R4,C4), (R1,C1,R2,C2) != (R4,C4,R3,C3), 
    cell(R1,C1,V1), cell(R2,C2,V2), cell(R3,C3,V3), cell(R4,C4,V4), 
    (V1,V2) = (V3,V4).
% AND chech that their reverse is also unique
:- pair(R1,C1,R2,C2), pair(R3,C3,R4,C4), 
    (R1,C1,R2,C2) != (R3,C3,R4,C4), (R1,C1,R2,C2) != (R4,C4,R3,C3), 
    cell(R1,C1,V1), cell(R2,C2,V2), cell(R3,C3,V3), cell(R4,C4,V4), 
    (V1,V2) = (V4,V3).

#show pair/4.