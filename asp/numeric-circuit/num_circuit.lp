% circuit
input(x1;x2;x3;x4).
output(y1;y2).
comp(c1;c2;c3;c4;c5).
type(c1, mult).
type(c2, mult).
type(c3, mult).
type(c4, plus).
type(c5, plus).

% connections
conn(x1,in1(c1)).
conn(x2,in2(c1)).
conn(x2,in1(c2)).
conn(x3,in2(c2)).
conn(x3,in1(c3)).
conn(x4,in2(c3)).
conn(out(c1),in1(c4)).
conn(out(c2),in2(c4)).
conn(out(c2),in1(c5)).
conn(out(c3),in2(c5)).
conn(out(c4),y1).
conn(out(c5),y2).

int(0..100).
mult(X, Y, X*Y) :- int(X), int(Y).
plus(X, Y, X+Y) :- int(X), int(Y).

% multiplication gate logic
val(out(C), Z) :- type(C, mult), nab(C), val(in1(C), X), val(in2(C), Y), mult(X, Y, Z).

val(in1(C), 1) :- type(C, mult), nab(C), val(out(C), 1).
val(in2(C), 1) :- type(C, mult), nab(C), val(out(C), 1).

val(in1(C), X) :- type(C, mult), nab(C), val(in2(C), Y), val(out(C), Z), Z != 0, mult(X, Y, Z).
val(in2(C), Y) :- type(C, mult), nab(C), val(in1(C), X), val(out(C), Z), Z != 0, mult(X, Y, Z).

val(in1(C), 0) :- type(C, mult), nab(C), val(in2(C), Y), Y != 0, val(out(C), 0).
val(in2(C), 0) :- type(C, mult), nab(C), val(in1(C), X), X != 0, val(out(C), 0).

% addition gate logic
val(out(C), Z) :- type(C, plus), nab(C), val(in1(C), X), val(in2(C), Y), plus(X, Y, Z).

val(in1(C), 0) :- type(C, plus), nab(C), val(out(C), 0).
val(in2(C), 0) :- type(C, plus), nab(C), val(out(C), 0).

val(in1(C), X) :- type(C, plus), nab(C), val(in2(C), Y), val(out(C), Z), plus(X, Y, Z).
val(in2(C), Y) :- type(C, plus), nab(C), val(in1(C), X), val(out(C), Z), plus(X, Y, Z).

val(in1(C), 1) :- type(C, plus), nab(C), val(in2(C), Y), Y = 0, val(out(C), 1).
val(in2(C), 1) :- type(C, plus), nab(C), val(in1(C), X), X = 0, val(out(C), 1).

% value propagation
val(P2,V) :- conn(P1,P2), val(P1,V).
val(P1,V) :- conn(P1,P2), val(P2,V).

% integrity constraint
:- val(P,_), #count{ V: val(P, V) } > 1.

% search diagnoses
{ ab(C); nab(C) } = 1 :- comp(C).

% fixed size of diagnosis
#const n = 0.
no_ab(N) :- N = #count{C: ab(C)}.
:- no_ab(N), N!=n.

#show ab/1.