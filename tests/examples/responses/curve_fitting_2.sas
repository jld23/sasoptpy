proc optmodel;
set POINTS;
num x {POINTS};
num y {POINTS};
read data None into POINTS=[_N_] x y;
num order init 2;
var beta {{0..order}};
impvar estimate {o8 in POINTS} = beta[0] + sum {k in 1..order} (beta[k] * (x[o8]) ^ (k));
var surplus {{POINTS}} >= 0;
var slack {{POINTS}} >= 0;
con abs_dev_con {o30 in POINTS} : y[o30] - estimate[o30] + surplus[o30] - slack[o30] = 0;

min L1obj = sum {i in POINTS} (surplus[i] + slack[i]);
solve;
print x y estimate surplus slack;
quit;