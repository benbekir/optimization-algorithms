int: n; % number of court members
set of int: COURT = 1..n;
int: emperor = 1;
array[COURT] of int: rank;
array[COURT] of int: ability;

int: m; % number of horses
set of int: HORSE = 1..m;
array[HORSE] of int: beauty;
array[HORSE] of int: speed;

array[COURT,HORSE] of int: enjoy;

array[COURT] of var 0..m: horse_of;
array[HORSE] of var 0..n: member_of;
var int: assignments_count;
var int: violations;
var int: objective;

% manually create inverse
constraint forall(i in COURT, j in HORSE)((horse_of[i] == j) <-> (member_of[j] == i));
% emperor must have most enjoyment
constraint forall(i in COURT where i > emperor /\ horse_of[i] != 0)(enjoy[i,horse_of[i]] < enjoy[emperor,horse_of[emperor]]);
% assign a horse to all court members (given that there are enough horses)
assignments_count = sum(i in COURT)(horse_of[i] != 0);
constraint assignments_count = min(n, m);
% higher-rank members have horses which are at least as beautiful as lower-rank members
constraint forall(i,j in COURT where i != j /\ horse_of[i] != 0 /\ horse_of[j] != 0)(
    (rank[i] > rank[j]) -> (beauty[horse_of[i]] >= beauty[horse_of[j]])
);
% if a higher-rank member does not have a horse, all lower-ranked members also can not have a horse
constraint forall(i, j in COURT where i != j)(
    (rank[i] > rank[j] /\ horse_of[i] == 0) -> (horse_of[j] == 0)
);
% faster horses have riders which are at least as skilled as riders on slower horses. otherwise, increase violation count.
constraint violations = sum(h1, h2 in HORSE where h1 < h2 /\ member_of[h1] != 0 /\ member_of[h2] != 0   )(
    bool2int(
        (speed[h1] > speed[h2] /\ ability[member_of[h1]] < ability[member_of[h2]]) \/
        (speed[h2] > speed[h1] /\ ability[member_of[h2]] < ability[member_of[h1]])
    )
);

objective = sum(i in COURT)(if horse_of[i] > 0 then enjoy[i,horse_of[i]] else 0 endif) - violations * 100;
solve maximize objective;

output["horse = \(horse_of)\nobjective = \(objective)"];