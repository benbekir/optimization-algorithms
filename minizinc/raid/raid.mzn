% select a set of raiding warrior
enum WARRIOR;
WARRIOR: dummy;
enum CLAN; % the clan they belong too

int: l; % minimum raid party size
int: u; % maximum raid party size
int: m; % limit of hatreds

array[WARRIOR] of int: strength;
array[WARRIOR] of CLAN: clan;

array[CLAN,CLAN] of 0..1: hates;

var set of WARRIOR: raid;
var int: obj;

constraint not (dummy in raid);

constraint card(raid) >= l;
constraint card(raid) <= u;

% iterate through all warrior tuples and sum number of hatreds + make sure they dont go over m
constraint (sum(w1 in raid)(sum(w2 in raid)(hates[clan[w1],clan[w2]] = 1 /\ enum2int(clan[w1]) < enum2int(clan[w2])))) <= m;

obj = sum(w in raid)(strength[w]);
solve maximize obj;

% use this for printing your solution to match the expected output format
output["raid = \(raid)\nobj = \(obj)"];
