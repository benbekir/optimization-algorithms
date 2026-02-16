% Problem:
%"Three married couple come to a river. The only vessel available is a small boat
%that can carry at most two of them. How can they cross the river, if at any time,
%no woman is in the company of any man unless her own husband is present?"

% background knowledge
boat.
person(m1;m2;m3;w1;w2;w3).
man(m1;m2;m3).
woman(w1;w2;w3).
married(m1,w1).
married(m2,w2).
married(m3,w3).
time(0..10).
side(left;right).

% initial state
at_bank(left,m1,0).
at_bank(left,w1,0).
at_bank(left,m2,0).
at_bank(left,w2,0).
at_bank(left,m3,0).
at_bank(left,w3,0).
at_bank(left,boat,0).

% intertia of at_bank
at_bank(B,X,T+1) :- at_bank(B,X,T), time(T), not -at_bank(B,X,T+1).

% one action at a time, but two people fit into the boat
{ cross(P,T): person(P) } <= 2 :- time(T).

% a person can only cross the river when the boat is on their side
:- cross(P,T), at_bank(B,P,T), not at_bank(B,boat,T).

% a man and woman cannot cross the river at the same time unless they are married
:- cross(M,T), cross(W,T), man(M), woman(W), not married(M,W).

% a woman cannot be on the same side of the river with any man, unless her husband is also there
:- at_bank(B,W,T), woman(W), man(M), married(M,W), not at_bank(B,M,T), man(M2), at_bank(B,M2,T), M != M2.

% effects of action cross
at_bank(B,X,T+1) :- cross(X,T), at_bank(A,X,T), side(B), side(A), A != B.
-at_bank(B,X,T+1) :- at_bank(B,X,T), cross(X,T).
at_bank(B,boat,T+1) :- cross(_,T), at_bank(A,boat,T), side(B), side(A), A != B.
-at_bank(B,boat,T+1) :- at_bank(B,boat,T), cross(_,T).

% goal state
goal_reached :- at_bank(right,m1,T), at_bank(right,w1,T), at_bank(right,m2,T), at_bank(right,w2,T), at_bank(right,m3,T), at_bank(right,w3,T), at_bank(right,boat,T).
:- not goal_reached.

#show cross/2.