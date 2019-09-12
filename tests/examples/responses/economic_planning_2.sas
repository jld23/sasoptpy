proc optmodel;
var production {{'coal','steel','transport'}, {0,1,2,3,4,5,6}} >= 0;
production['coal', 0].ub = 0;
production['steel', 0].ub = 0;
production['transport', 0].ub = 0;
var stock {{'coal','steel','transport'}, {0,1,2,3,4,5,6}} >= 0;
stock['coal', 0].lb = 150;
stock['coal', 0].ub = 150;
stock['steel', 0].lb = 80;
stock['steel', 0].ub = 80;
stock['transport', 0].lb = 100;
stock['transport', 0].ub = 100;
var extra_capacity {{'coal','steel','transport'}, {2,3,4,5,6,7}} >= 0;
extra_capacity['coal', 6].ub = 0;
extra_capacity['coal', 7].ub = 0;
extra_capacity['steel', 6].ub = 0;
extra_capacity['steel', 7].ub = 0;
extra_capacity['transport', 6].ub = 0;
extra_capacity['transport', 7].ub = 0;
con continuity_con_coal_0 : stock['coal', 0] + production['coal', 0] - 0.1 * production['coal', 1] - 0.5 * production['steel', 1] - 0.7 * extra_capacity['steel', 2] - 0.4 * production['transport', 1] - 0.9 * extra_capacity['transport', 2] - stock['coal', 1] = 0.0;
con continuity_con_coal_1 : stock['coal', 1] + production['coal', 1] - 0.1 * production['coal', 2] - 0.5 * production['steel', 2] - 0.7 * extra_capacity['steel', 3] - 0.4 * production['transport', 2] - 0.9 * extra_capacity['transport', 3] - stock['coal', 2] = 0;
con continuity_con_coal_2 : stock['coal', 2] + production['coal', 2] - 0.1 * production['coal', 3] - 0.5 * production['steel', 3] - 0.7 * extra_capacity['steel', 4] - 0.4 * production['transport', 3] - 0.9 * extra_capacity['transport', 4] - stock['coal', 3] = 0;
con continuity_con_coal_3 : stock['coal', 3] + production['coal', 3] - 0.1 * production['coal', 4] - 0.5 * production['steel', 4] - 0.7 * extra_capacity['steel', 5] - 0.4 * production['transport', 4] - 0.9 * extra_capacity['transport', 5] - stock['coal', 4] = 0;
con continuity_con_coal_4 : stock['coal', 4] + production['coal', 4] - 0.1 * production['coal', 5] - 0.5 * production['steel', 5] - 0.7 * extra_capacity['steel', 6] - 0.4 * production['transport', 5] - 0.9 * extra_capacity['transport', 6] - stock['coal', 5] = 0;
con continuity_con_coal_5 : stock['coal', 5] + production['coal', 5] - 0.1 * production['coal', 6] - 0.5 * production['steel', 6] - 0.7 * extra_capacity['steel', 7] - 0.4 * production['transport', 6] - 0.9 * extra_capacity['transport', 7] - stock['coal', 6] = 0;
con continuity_con_steel_0 : stock['steel', 0] + production['steel', 0] - 0.1 * production['coal', 1] - 0.1 * extra_capacity['coal', 2] - 0.1 * production['steel', 1] - 0.1 * extra_capacity['steel', 2] - 0.2 * production['transport', 1] - 0.2 * extra_capacity['transport', 2] - stock['steel', 1] = 0.0;
con continuity_con_steel_1 : stock['steel', 1] + production['steel', 1] - 0.1 * production['coal', 2] - 0.1 * extra_capacity['coal', 3] - 0.1 * production['steel', 2] - 0.1 * extra_capacity['steel', 3] - 0.2 * production['transport', 2] - 0.2 * extra_capacity['transport', 3] - stock['steel', 2] = 0;
con continuity_con_steel_2 : stock['steel', 2] + production['steel', 2] - 0.1 * production['coal', 3] - 0.1 * extra_capacity['coal', 4] - 0.1 * production['steel', 3] - 0.1 * extra_capacity['steel', 4] - 0.2 * production['transport', 3] - 0.2 * extra_capacity['transport', 4] - stock['steel', 3] = 0;
con continuity_con_steel_3 : stock['steel', 3] + production['steel', 3] - 0.1 * production['coal', 4] - 0.1 * extra_capacity['coal', 5] - 0.1 * production['steel', 4] - 0.1 * extra_capacity['steel', 5] - 0.2 * production['transport', 4] - 0.2 * extra_capacity['transport', 5] - stock['steel', 4] = 0;
con continuity_con_steel_4 : stock['steel', 4] + production['steel', 4] - 0.1 * production['coal', 5] - 0.1 * extra_capacity['coal', 6] - 0.1 * production['steel', 5] - 0.1 * extra_capacity['steel', 6] - 0.2 * production['transport', 5] - 0.2 * extra_capacity['transport', 6] - stock['steel', 5] = 0;
con continuity_con_steel_5 : stock['steel', 5] + production['steel', 5] - 0.1 * production['coal', 6] - 0.1 * extra_capacity['coal', 7] - 0.1 * production['steel', 6] - 0.1 * extra_capacity['steel', 7] - 0.2 * production['transport', 6] - 0.2 * extra_capacity['transport', 7] - stock['steel', 6] = 0;
con continuity_con_transport_0 : stock['transport', 0] + production['transport', 0] - 0.2 * production['coal', 1] - 0.2 * extra_capacity['coal', 2] - 0.1 * production['steel', 1] - 0.1 * extra_capacity['steel', 2] - 0.2 * production['transport', 1] - 0.2 * extra_capacity['transport', 2] - stock['transport', 1] = 0.0;
con continuity_con_transport_1 : stock['transport', 1] + production['transport', 1] - 0.2 * production['coal', 2] - 0.2 * extra_capacity['coal', 3] - 0.1 * production['steel', 2] - 0.1 * extra_capacity['steel', 3] - 0.2 * production['transport', 2] - 0.2 * extra_capacity['transport', 3] - stock['transport', 2] = 0;
con continuity_con_transport_2 : stock['transport', 2] + production['transport', 2] - 0.2 * production['coal', 3] - 0.2 * extra_capacity['coal', 4] - 0.1 * production['steel', 3] - 0.1 * extra_capacity['steel', 4] - 0.2 * production['transport', 3] - 0.2 * extra_capacity['transport', 4] - stock['transport', 3] = 0;
con continuity_con_transport_3 : stock['transport', 3] + production['transport', 3] - 0.2 * production['coal', 4] - 0.2 * extra_capacity['coal', 5] - 0.1 * production['steel', 4] - 0.1 * extra_capacity['steel', 5] - 0.2 * production['transport', 4] - 0.2 * extra_capacity['transport', 5] - stock['transport', 4] = 0;
con continuity_con_transport_4 : stock['transport', 4] + production['transport', 4] - 0.2 * production['coal', 5] - 0.2 * extra_capacity['coal', 6] - 0.1 * production['steel', 5] - 0.1 * extra_capacity['steel', 6] - 0.2 * production['transport', 5] - 0.2 * extra_capacity['transport', 6] - stock['transport', 5] = 0;
con continuity_con_transport_5 : stock['transport', 5] + production['transport', 5] - 0.2 * production['coal', 6] - 0.2 * extra_capacity['coal', 7] - 0.1 * production['steel', 6] - 0.1 * extra_capacity['steel', 7] - 0.2 * production['transport', 6] - 0.2 * extra_capacity['transport', 7] - stock['transport', 6] = 0;
con manpower_con_1 : 0.6 * production['coal', 1] + 0.4 * extra_capacity['coal', 2] + 0.3 * production['steel', 1] + 0.2 * extra_capacity['steel', 2] + 0.2 * production['transport', 1] + 0.1 * extra_capacity['transport', 2] <= 470.0;
con manpower_con_2 : 0.6 * production['coal', 2] + 0.4 * extra_capacity['coal', 3] + 0.3 * production['steel', 2] + 0.2 * extra_capacity['steel', 3] + 0.2 * production['transport', 2] + 0.1 * extra_capacity['transport', 3] <= 470.0;
con manpower_con_3 : 0.6 * production['coal', 3] + 0.4 * extra_capacity['coal', 4] + 0.3 * production['steel', 3] + 0.2 * extra_capacity['steel', 4] + 0.2 * production['transport', 3] + 0.1 * extra_capacity['transport', 4] <= 470.0;
con manpower_con_4 : 0.6 * production['coal', 4] + 0.4 * extra_capacity['coal', 5] + 0.3 * production['steel', 4] + 0.2 * extra_capacity['steel', 5] + 0.2 * production['transport', 4] + 0.1 * extra_capacity['transport', 5] <= 470.0;
con manpower_con_5 : 0.6 * production['coal', 5] + 0.4 * extra_capacity['coal', 6] + 0.3 * production['steel', 5] + 0.2 * extra_capacity['steel', 6] + 0.2 * production['transport', 5] + 0.1 * extra_capacity['transport', 6] <= 470.0;
con manpower_con_6 : 0.6 * production['coal', 6] + 0.4 * extra_capacity['coal', 7] + 0.3 * production['steel', 6] + 0.2 * extra_capacity['steel', 7] + 0.2 * production['transport', 6] + 0.1 * extra_capacity['transport', 7] <= 470.0;
con capacity_con_coal_1 : production['coal', 1] <= 300;
con capacity_con_coal_2 : production['coal', 2] - extra_capacity['coal', 2] <= 300;
con capacity_con_coal_3 : production['coal', 3] - extra_capacity['coal', 2] - extra_capacity['coal', 3] <= 300;
con capacity_con_coal_4 : production['coal', 4] - extra_capacity['coal', 2] - extra_capacity['coal', 3] - extra_capacity['coal', 4] <= 300;
con capacity_con_coal_5 : production['coal', 5] - extra_capacity['coal', 2] - extra_capacity['coal', 3] - extra_capacity['coal', 4] - extra_capacity['coal', 5] <= 300;
con capacity_con_coal_6 : production['coal', 6] - extra_capacity['coal', 2] - extra_capacity['coal', 3] - extra_capacity['coal', 4] - extra_capacity['coal', 5] - extra_capacity['coal', 6] <= 300;
con capacity_con_steel_1 : production['steel', 1] <= 350;
con capacity_con_steel_2 : production['steel', 2] - extra_capacity['steel', 2] <= 350;
con capacity_con_steel_3 : production['steel', 3] - extra_capacity['steel', 2] - extra_capacity['steel', 3] <= 350;
con capacity_con_steel_4 : production['steel', 4] - extra_capacity['steel', 2] - extra_capacity['steel', 3] - extra_capacity['steel', 4] <= 350;
con capacity_con_steel_5 : production['steel', 5] - extra_capacity['steel', 2] - extra_capacity['steel', 3] - extra_capacity['steel', 4] - extra_capacity['steel', 5] <= 350;
con capacity_con_steel_6 : production['steel', 6] - extra_capacity['steel', 2] - extra_capacity['steel', 3] - extra_capacity['steel', 4] - extra_capacity['steel', 5] - extra_capacity['steel', 6] <= 350;
con capacity_con_transport_1 : production['transport', 1] <= 280;
con capacity_con_transport_2 : production['transport', 2] - extra_capacity['transport', 2] <= 280;
con capacity_con_transport_3 : production['transport', 3] - extra_capacity['transport', 2] - extra_capacity['transport', 3] <= 280;
con capacity_con_transport_4 : production['transport', 4] - extra_capacity['transport', 2] - extra_capacity['transport', 3] - extra_capacity['transport', 4] <= 280;
con capacity_con_transport_5 : production['transport', 5] - extra_capacity['transport', 2] - extra_capacity['transport', 3] - extra_capacity['transport', 4] - extra_capacity['transport', 5] <= 280;
con capacity_con_transport_6 : production['transport', 6] - extra_capacity['transport', 2] - extra_capacity['transport', 3] - extra_capacity['transport', 4] - extra_capacity['transport', 5] - extra_capacity['transport', 6] <= 280;
max total_production = production['coal', 4] + production['coal', 5] + production['steel', 4] + production['steel', 5] + production['transport', 4] + production['transport', 5];
solve;
quit;