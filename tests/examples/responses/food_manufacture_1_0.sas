proc optmodel;
var buy {{'veg1','veg2','oil1','oil2','oil3'}, {1,2,3,4,5,6}} >= 0;
var use {{'veg1','veg2','oil1','oil2','oil3'}, {1,2,3,4,5,6}} >= 0;
impvar manufacture_1 = use['oil1', 1] + use['oil2', 1] + use['oil3', 1] + use['veg1', 1] + use['veg2', 1];
impvar manufacture_2 = use['oil1', 2] + use['oil2', 2] + use['oil3', 2] + use['veg1', 2] + use['veg2', 2];
impvar manufacture_3 = use['oil1', 3] + use['oil2', 3] + use['oil3', 3] + use['veg1', 3] + use['veg2', 3];
impvar manufacture_4 = use['oil1', 4] + use['oil2', 4] + use['oil3', 4] + use['veg1', 4] + use['veg2', 4];
impvar manufacture_5 = use['oil1', 5] + use['oil2', 5] + use['oil3', 5] + use['veg1', 5] + use['veg2', 5];
impvar manufacture_6 = use['oil1', 6] + use['oil2', 6] + use['oil3', 6] + use['veg1', 6] + use['veg2', 6];
var store {{'veg1','veg2','oil1','oil2','oil3'}, {0,1,2,3,4,5,6}} >= 0 <= 1000;
store['veg1', 0].lb = 500;
store['veg1', 0].ub = 500;
store['veg1', 6].lb = 500;
store['veg1', 6].ub = 500;
store['veg2', 0].lb = 500;
store['veg2', 0].ub = 500;
store['veg2', 6].lb = 500;
store['veg2', 6].ub = 500;
store['oil1', 0].lb = 500;
store['oil1', 0].ub = 500;
store['oil1', 6].lb = 500;
store['oil1', 6].ub = 500;
store['oil2', 0].lb = 500;
store['oil2', 0].ub = 500;
store['oil2', 6].lb = 500;
store['oil2', 6].ub = 500;
store['oil3', 0].lb = 500;
store['oil3', 0].ub = 500;
store['oil3', 6].lb = 500;
store['oil3', 6].ub = 500;
max profit = 150 * (use['oil1', 1] + use['oil2', 1] + use['oil3', 1] + use['veg1', 1] + use['veg2', 1]) + 150 * (use['oil1', 2] + use['oil2', 2] + use['oil3', 2] + use['veg1', 2] + use['veg2', 2]) + 150 * (use['oil1', 3] + use['oil2', 3] + use['oil3', 3] + use['veg1', 3] + use['veg2', 3]) + 150 * (use['oil1', 4] + use['oil2', 4] + use['oil3', 4] + use['veg1', 4] + use['veg2', 4]) + 150 * (use['oil1', 5] + use['oil2', 5] + use['oil3', 5] + use['veg1', 5] + use['veg2', 5]) + 150 * (use['oil1', 6] + use['oil2', 6] + use['oil3', 6] + use['veg1', 6] + use['veg2', 6]) - 110 * buy['veg1', 1] - 130 * buy['veg1', 2] - 110 * buy['veg1', 3] - 120 * buy['veg1', 4] - 100 * buy['veg1', 5] - 90 * buy['veg1', 6] - 120 * buy['veg2', 1] - 130 * buy['veg2', 2] - 140 * buy['veg2', 3] - 110 * buy['veg2', 4] - 120 * buy['veg2', 5] - 100 * buy['veg2', 6] - 130 * buy['oil1', 1] - 110 * buy['oil1', 2] - 130 * buy['oil1', 3] - 120 * buy['oil1', 4] - 150 * buy['oil1', 5] - 140 * buy['oil1', 6] - 110 * buy['oil2', 1] - 90 * buy['oil2', 2] - 100 * buy['oil2', 3] - 120 * buy['oil2', 4] - 110 * buy['oil2', 5] - 80 * buy['oil2', 6] - 115 * buy['oil3', 1] - 115 * buy['oil3', 2] - 95 * buy['oil3', 3] - 125 * buy['oil3', 4] - 105 * buy['oil3', 5] - 135 * buy['oil3', 6] - 5 * store['veg1', 1] - 5 * store['veg1', 2] - 5 * store['veg1', 3] - 5 * store['veg1', 4] - 5 * store['veg1', 5] - 5 * store['veg1', 6] - 5 * store['veg2', 1] - 5 * store['veg2', 2] - 5 * store['veg2', 3] - 5 * store['veg2', 4] - 5 * store['veg2', 5] - 5 * store['veg2', 6] - 5 * store['oil1', 1] - 5 * store['oil1', 2] - 5 * store['oil1', 3] - 5 * store['oil1', 4] - 5 * store['oil1', 5] - 5 * store['oil1', 6] - 5 * store['oil2', 1] - 5 * store['oil2', 2] - 5 * store['oil2', 3] - 5 * store['oil2', 4] - 5 * store['oil2', 5] - 5 * store['oil2', 6] - 5 * store['oil3', 1] - 5 * store['oil3', 2] - 5 * store['oil3', 3] - 5 * store['oil3', 4] - 5 * store['oil3', 5] - 5 * store['oil3', 6];
con veg_ub_1 : use['veg1', 1] + use['veg2', 1] <= 200;
con veg_ub_2 : use['veg1', 2] + use['veg2', 2] <= 200;
con veg_ub_3 : use['veg1', 3] + use['veg2', 3] <= 200;
con veg_ub_4 : use['veg1', 4] + use['veg2', 4] <= 200;
con veg_ub_5 : use['veg1', 5] + use['veg2', 5] <= 200;
con veg_ub_6 : use['veg1', 6] + use['veg2', 6] <= 200;

con nonveg_ub_1 : use['oil1', 1] + use['oil2', 1] + use['oil3', 1] <= 250;
con nonveg_ub_2 : use['oil1', 2] + use['oil2', 2] + use['oil3', 2] <= 250;
con nonveg_ub_3 : use['oil1', 3] + use['oil2', 3] + use['oil3', 3] <= 250;
con nonveg_ub_4 : use['oil1', 4] + use['oil2', 4] + use['oil3', 4] <= 250;
con nonveg_ub_5 : use['oil1', 5] + use['oil2', 5] + use['oil3', 5] <= 250;
con nonveg_ub_6 : use['oil1', 6] + use['oil2', 6] + use['oil3', 6] <= 250;

con flow_balance_veg1_1 : store['veg1', 0] + buy['veg1', 1] - use['veg1', 1] - store['veg1', 1] = 0;
con flow_balance_veg1_2 : store['veg1', 1] + buy['veg1', 2] - use['veg1', 2] - store['veg1', 2] = 0;
con flow_balance_veg1_3 : store['veg1', 2] + buy['veg1', 3] - use['veg1', 3] - store['veg1', 3] = 0;
con flow_balance_veg1_4 : store['veg1', 3] + buy['veg1', 4] - use['veg1', 4] - store['veg1', 4] = 0;
con flow_balance_veg1_5 : store['veg1', 4] + buy['veg1', 5] - use['veg1', 5] - store['veg1', 5] = 0;
con flow_balance_veg1_6 : store['veg1', 5] + buy['veg1', 6] - use['veg1', 6] - store['veg1', 6] = 0;
con flow_balance_veg2_1 : store['veg2', 0] + buy['veg2', 1] - use['veg2', 1] - store['veg2', 1] = 0;
con flow_balance_veg2_2 : store['veg2', 1] + buy['veg2', 2] - use['veg2', 2] - store['veg2', 2] = 0;
con flow_balance_veg2_3 : store['veg2', 2] + buy['veg2', 3] - use['veg2', 3] - store['veg2', 3] = 0;
con flow_balance_veg2_4 : store['veg2', 3] + buy['veg2', 4] - use['veg2', 4] - store['veg2', 4] = 0;
con flow_balance_veg2_5 : store['veg2', 4] + buy['veg2', 5] - use['veg2', 5] - store['veg2', 5] = 0;
con flow_balance_veg2_6 : store['veg2', 5] + buy['veg2', 6] - use['veg2', 6] - store['veg2', 6] = 0;
con flow_balance_oil1_1 : store['oil1', 0] + buy['oil1', 1] - use['oil1', 1] - store['oil1', 1] = 0;
con flow_balance_oil1_2 : store['oil1', 1] + buy['oil1', 2] - use['oil1', 2] - store['oil1', 2] = 0;
con flow_balance_oil1_3 : store['oil1', 2] + buy['oil1', 3] - use['oil1', 3] - store['oil1', 3] = 0;
con flow_balance_oil1_4 : store['oil1', 3] + buy['oil1', 4] - use['oil1', 4] - store['oil1', 4] = 0;
con flow_balance_oil1_5 : store['oil1', 4] + buy['oil1', 5] - use['oil1', 5] - store['oil1', 5] = 0;
con flow_balance_oil1_6 : store['oil1', 5] + buy['oil1', 6] - use['oil1', 6] - store['oil1', 6] = 0;
con flow_balance_oil2_1 : store['oil2', 0] + buy['oil2', 1] - use['oil2', 1] - store['oil2', 1] = 0;
con flow_balance_oil2_2 : store['oil2', 1] + buy['oil2', 2] - use['oil2', 2] - store['oil2', 2] = 0;
con flow_balance_oil2_3 : store['oil2', 2] + buy['oil2', 3] - use['oil2', 3] - store['oil2', 3] = 0;
con flow_balance_oil2_4 : store['oil2', 3] + buy['oil2', 4] - use['oil2', 4] - store['oil2', 4] = 0;
con flow_balance_oil2_5 : store['oil2', 4] + buy['oil2', 5] - use['oil2', 5] - store['oil2', 5] = 0;
con flow_balance_oil2_6 : store['oil2', 5] + buy['oil2', 6] - use['oil2', 6] - store['oil2', 6] = 0;
con flow_balance_oil3_1 : store['oil3', 0] + buy['oil3', 1] - use['oil3', 1] - store['oil3', 1] = 0;
con flow_balance_oil3_2 : store['oil3', 1] + buy['oil3', 2] - use['oil3', 2] - store['oil3', 2] = 0;
con flow_balance_oil3_3 : store['oil3', 2] + buy['oil3', 3] - use['oil3', 3] - store['oil3', 3] = 0;
con flow_balance_oil3_4 : store['oil3', 3] + buy['oil3', 4] - use['oil3', 4] - store['oil3', 4] = 0;
con flow_balance_oil3_5 : store['oil3', 4] + buy['oil3', 5] - use['oil3', 5] - store['oil3', 5] = 0;
con flow_balance_oil3_6 : store['oil3', 5] + buy['oil3', 6] - use['oil3', 6] - store['oil3', 6] = 0;

con hardness_ub_1 : 8.8 * use['veg1', 1] + 6.1 * use['veg2', 1] + 2.0 * use['oil1', 1] + 4.2 * use['oil2', 1] + 5.0 * use['oil3', 1] - 3 * (use['oil1', 1] + use['oil2', 1] + use['oil3', 1] + use['veg1', 1] + use['veg2', 1]) >= 0.0;
con hardness_ub_2 : 8.8 * use['veg1', 2] + 6.1 * use['veg2', 2] + 2.0 * use['oil1', 2] + 4.2 * use['oil2', 2] + 5.0 * use['oil3', 2] - 3 * (use['oil1', 2] + use['oil2', 2] + use['oil3', 2] + use['veg1', 2] + use['veg2', 2]) >= 0.0;
con hardness_ub_3 : 8.8 * use['veg1', 3] + 6.1 * use['veg2', 3] + 2.0 * use['oil1', 3] + 4.2 * use['oil2', 3] + 5.0 * use['oil3', 3] - 3 * (use['oil1', 3] + use['oil2', 3] + use['oil3', 3] + use['veg1', 3] + use['veg2', 3]) >= 0.0;
con hardness_ub_4 : 8.8 * use['veg1', 4] + 6.1 * use['veg2', 4] + 2.0 * use['oil1', 4] + 4.2 * use['oil2', 4] + 5.0 * use['oil3', 4] - 3 * (use['oil1', 4] + use['oil2', 4] + use['oil3', 4] + use['veg1', 4] + use['veg2', 4]) >= 0.0;
con hardness_ub_5 : 8.8 * use['veg1', 5] + 6.1 * use['veg2', 5] + 2.0 * use['oil1', 5] + 4.2 * use['oil2', 5] + 5.0 * use['oil3', 5] - 3 * (use['oil1', 5] + use['oil2', 5] + use['oil3', 5] + use['veg1', 5] + use['veg2', 5]) >= 0.0;
con hardness_ub_6 : 8.8 * use['veg1', 6] + 6.1 * use['veg2', 6] + 2.0 * use['oil1', 6] + 4.2 * use['oil2', 6] + 5.0 * use['oil3', 6] - 3 * (use['oil1', 6] + use['oil2', 6] + use['oil3', 6] + use['veg1', 6] + use['veg2', 6]) >= 0.0;

con hardness_lb_1 : 8.8 * use['veg1', 1] + 6.1 * use['veg2', 1] + 2.0 * use['oil1', 1] + 4.2 * use['oil2', 1] + 5.0 * use['oil3', 1] - 6 * (use['oil1', 1] + use['oil2', 1] + use['oil3', 1] + use['veg1', 1] + use['veg2', 1]) <= 0.0;
con hardness_lb_2 : 8.8 * use['veg1', 2] + 6.1 * use['veg2', 2] + 2.0 * use['oil1', 2] + 4.2 * use['oil2', 2] + 5.0 * use['oil3', 2] - 6 * (use['oil1', 2] + use['oil2', 2] + use['oil3', 2] + use['veg1', 2] + use['veg2', 2]) <= 0.0;
con hardness_lb_3 : 8.8 * use['veg1', 3] + 6.1 * use['veg2', 3] + 2.0 * use['oil1', 3] + 4.2 * use['oil2', 3] + 5.0 * use['oil3', 3] - 6 * (use['oil1', 3] + use['oil2', 3] + use['oil3', 3] + use['veg1', 3] + use['veg2', 3]) <= 0.0;
con hardness_lb_4 : 8.8 * use['veg1', 4] + 6.1 * use['veg2', 4] + 2.0 * use['oil1', 4] + 4.2 * use['oil2', 4] + 5.0 * use['oil3', 4] - 6 * (use['oil1', 4] + use['oil2', 4] + use['oil3', 4] + use['veg1', 4] + use['veg2', 4]) <= 0.0;
con hardness_lb_5 : 8.8 * use['veg1', 5] + 6.1 * use['veg2', 5] + 2.0 * use['oil1', 5] + 4.2 * use['oil2', 5] + 5.0 * use['oil3', 5] - 6 * (use['oil1', 5] + use['oil2', 5] + use['oil3', 5] + use['veg1', 5] + use['veg2', 5]) <= 0.0;
con hardness_lb_6 : 8.8 * use['veg1', 6] + 6.1 * use['veg2', 6] + 2.0 * use['oil1', 6] + 4.2 * use['oil2', 6] + 5.0 * use['oil3', 6] - 6 * (use['oil1', 6] + use['oil2', 6] + use['oil3', 6] + use['veg1', 6] + use['veg2', 6]) <= 0.0;

solve;
quit;