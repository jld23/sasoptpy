proc optmodel;
var flow {{<'source','crude1'>,<'source','crude2'>,<'crude1','light_naphtha'>,<'crude1','medium_naphtha'>,<'crude1','heavy_naphtha'>,<'crude1','light_oil'>,<'crude1','heavy_oil'>,<'crude1','residuum'>,<'crude2','light_naphtha'>,<'crude2','medium_naphtha'>,<'crude2','heavy_naphtha'>,<'crude2','light_oil'>,<'crude2','heavy_oil'>,<'crude2','residuum'>,<'light_naphtha','regular_petrol'>,<'light_naphtha','premium_petrol'>,<'medium_naphtha','regular_petrol'>,<'medium_naphtha','premium_petrol'>,<'heavy_naphtha','regular_petrol'>,<'heavy_naphtha','premium_petrol'>,<'light_naphtha','reformed_gasoline'>,<'medium_naphtha','reformed_gasoline'>,<'heavy_naphtha','reformed_gasoline'>,<'light_oil','jet_fuel'>,<'light_oil','fuel_oil'>,<'heavy_oil','jet_fuel'>,<'heavy_oil','fuel_oil'>,<'light_oil','light_oil_cracked'>,<'light_oil_cracked','cracked_oil'>,<'light_oil_cracked','cracked_gasoline'>,<'heavy_oil','heavy_oil_cracked'>,<'heavy_oil_cracked','cracked_oil'>,<'heavy_oil_cracked','cracked_gasoline'>,<'cracked_oil','jet_fuel'>,<'cracked_oil','fuel_oil'>,<'reformed_gasoline','regular_petrol'>,<'reformed_gasoline','premium_petrol'>,<'cracked_gasoline','regular_petrol'>,<'cracked_gasoline','premium_petrol'>,<'residuum','lube_oil'>,<'residuum','jet_fuel'>,<'residuum','fuel_oil'>,<'premium_petrol','sink'>,<'regular_petrol','sink'>,<'jet_fuel','sink'>,<'fuel_oil','sink'>,<'lube_oil','sink'>}} >= 0;
max totalProfit = 7.0 * flow['premium_petrol', 'sink'] + 6.0 * flow['regular_petrol', 'sink'] + 4.0 * flow['jet_fuel', 'sink'] + 3.5 * flow['fuel_oil', 'sink'] + 1.5 * flow['lube_oil', 'sink'];
con flow_balance_cracked_gasoline : flow['cracked_gasoline', 'regular_petrol'] + flow['cracked_gasoline', 'premium_petrol'] - 0.28 * flow['light_oil_cracked', 'cracked_gasoline'] - 0.2 * flow['heavy_oil_cracked', 'cracked_gasoline'] = 0.0;
con flow_balance_cracked_oil : flow['cracked_oil', 'jet_fuel'] + flow['cracked_oil', 'fuel_oil'] - 0.68 * flow['light_oil_cracked', 'cracked_oil'] - 0.75 * flow['heavy_oil_cracked', 'cracked_oil'] = 0.0;
con flow_balance_crude1 : flow['crude1', 'light_naphtha'] + flow['crude1', 'medium_naphtha'] + flow['crude1', 'heavy_naphtha'] + flow['crude1', 'light_oil'] + flow['crude1', 'heavy_oil'] + flow['crude1', 'residuum'] - 6.0 * flow['source', 'crude1'] = 0.0;
con flow_balance_crude2 : flow['crude2', 'light_naphtha'] + flow['crude2', 'medium_naphtha'] + flow['crude2', 'heavy_naphtha'] + flow['crude2', 'light_oil'] + flow['crude2', 'heavy_oil'] + flow['crude2', 'residuum'] - 6.0 * flow['source', 'crude2'] = 0.0;
con flow_balance_fuel_oil : flow['fuel_oil', 'sink'] - flow['light_oil', 'fuel_oil'] - flow['heavy_oil', 'fuel_oil'] - flow['cracked_oil', 'fuel_oil'] - flow['residuum', 'fuel_oil'] = 0.0;
con flow_balance_heavy_naphtha : flow['heavy_naphtha', 'regular_petrol'] + flow['heavy_naphtha', 'premium_petrol'] + flow['heavy_naphtha', 'reformed_gasoline'] - 0.2 * flow['crude1', 'heavy_naphtha'] - 0.18 * flow['crude2', 'heavy_naphtha'] = 0.0;
con flow_balance_heavy_oil : flow['heavy_oil', 'jet_fuel'] + flow['heavy_oil', 'fuel_oil'] + flow['heavy_oil', 'heavy_oil_cracked'] - 0.2 * flow['crude1', 'heavy_oil'] - 0.19 * flow['crude2', 'heavy_oil'] = 0.0;
con flow_balance_heavy_oil_cracked : flow['heavy_oil_cracked', 'cracked_oil'] + flow['heavy_oil_cracked', 'cracked_gasoline'] - 2.0 * flow['heavy_oil', 'heavy_oil_cracked'] = 0.0;
con flow_balance_jet_fuel : flow['jet_fuel', 'sink'] - flow['light_oil', 'jet_fuel'] - flow['heavy_oil', 'jet_fuel'] - flow['cracked_oil', 'jet_fuel'] - flow['residuum', 'jet_fuel'] = 0.0;
con flow_balance_light_naphtha : flow['light_naphtha', 'regular_petrol'] + flow['light_naphtha', 'premium_petrol'] + flow['light_naphtha', 'reformed_gasoline'] - 0.1 * flow['crude1', 'light_naphtha'] - 0.15 * flow['crude2', 'light_naphtha'] = 0.0;
con flow_balance_light_oil : flow['light_oil', 'jet_fuel'] + flow['light_oil', 'fuel_oil'] + flow['light_oil', 'light_oil_cracked'] - 0.12 * flow['crude1', 'light_oil'] - 0.08 * flow['crude2', 'light_oil'] = 0.0;
con flow_balance_light_oil_cracked : flow['light_oil_cracked', 'cracked_oil'] + flow['light_oil_cracked', 'cracked_gasoline'] - 2.0 * flow['light_oil', 'light_oil_cracked'] = 0.0;
con flow_balance_lube_oil : flow['lube_oil', 'sink'] - 0.5 * flow['residuum', 'lube_oil'] = 0.0;
con flow_balance_medium_naphtha : flow['medium_naphtha', 'regular_petrol'] + flow['medium_naphtha', 'premium_petrol'] + flow['medium_naphtha', 'reformed_gasoline'] - 0.2 * flow['crude1', 'medium_naphtha'] - 0.25 * flow['crude2', 'medium_naphtha'] = 0.0;
con flow_balance_premium_petrol : flow['premium_petrol', 'sink'] - flow['light_naphtha', 'premium_petrol'] - flow['medium_naphtha', 'premium_petrol'] - flow['heavy_naphtha', 'premium_petrol'] - flow['reformed_gasoline', 'premium_petrol'] - flow['cracked_gasoline', 'premium_petrol'] = 0.0;
con flow_balance_reformed_gasoline : flow['reformed_gasoline', 'regular_petrol'] + flow['reformed_gasoline', 'premium_petrol'] - 0.6 * flow['light_naphtha', 'reformed_gasoline'] - 0.52 * flow['medium_naphtha', 'reformed_gasoline'] - 0.45 * flow['heavy_naphtha', 'reformed_gasoline'] = 0.0;
con flow_balance_regular_petrol : flow['regular_petrol', 'sink'] - flow['light_naphtha', 'regular_petrol'] - flow['medium_naphtha', 'regular_petrol'] - flow['heavy_naphtha', 'regular_petrol'] - flow['reformed_gasoline', 'regular_petrol'] - flow['cracked_gasoline', 'regular_petrol'] = 0.0;
con flow_balance_residuum : flow['residuum', 'lube_oil'] + flow['residuum', 'jet_fuel'] + flow['residuum', 'fuel_oil'] - 0.13 * flow['crude1', 'residuum'] - 0.12 * flow['crude2', 'residuum'] = 0.0;
var crudesDistilled {{'crude1','crude2'}} >= 0;
crudesDistilled['crude1'].ub = 20000;
crudesDistilled['crude2'].ub = 30000;
con distillation_crude1_light_naphtha : flow['crude1', 'light_naphtha'] - crudesDistilled['crude1'] = 0;
con distillation_crude1_medium_naphtha : flow['crude1', 'medium_naphtha'] - crudesDistilled['crude1'] = 0;
con distillation_crude1_heavy_naphtha : flow['crude1', 'heavy_naphtha'] - crudesDistilled['crude1'] = 0;
con distillation_crude1_light_oil : flow['crude1', 'light_oil'] - crudesDistilled['crude1'] = 0;
con distillation_crude1_heavy_oil : flow['crude1', 'heavy_oil'] - crudesDistilled['crude1'] = 0;
con distillation_crude1_residuum : flow['crude1', 'residuum'] - crudesDistilled['crude1'] = 0;
con distillation_crude2_light_naphtha : flow['crude2', 'light_naphtha'] - crudesDistilled['crude2'] = 0;
con distillation_crude2_medium_naphtha : flow['crude2', 'medium_naphtha'] - crudesDistilled['crude2'] = 0;
con distillation_crude2_heavy_naphtha : flow['crude2', 'heavy_naphtha'] - crudesDistilled['crude2'] = 0;
con distillation_crude2_light_oil : flow['crude2', 'light_oil'] - crudesDistilled['crude2'] = 0;
con distillation_crude2_heavy_oil : flow['crude2', 'heavy_oil'] - crudesDistilled['crude2'] = 0;
con distillation_crude2_residuum : flow['crude2', 'residuum'] - crudesDistilled['crude2'] = 0;
var oilCracked {{'light_oil_cracked','heavy_oil_cracked'}} >= 0;
con cracking_light_oil_cracked_cracked_oil : flow['light_oil_cracked', 'cracked_oil'] - oilCracked['light_oil_cracked'] = 0;
con cracking_light_oil_cracked_cracked_gasoline : flow['light_oil_cracked', 'cracked_gasoline'] - oilCracked['light_oil_cracked'] = 0;
con cracking_heavy_oil_cracked_cracked_oil : flow['heavy_oil_cracked', 'cracked_oil'] - oilCracked['heavy_oil_cracked'] = 0;
con cracking_heavy_oil_cracked_cracked_gasoline : flow['heavy_oil_cracked', 'cracked_gasoline'] - oilCracked['heavy_oil_cracked'] = 0;
con blending_petrol_regular_petrol : 6.0 * flow['light_naphtha', 'regular_petrol'] - 4.0 * flow['medium_naphtha', 'regular_petrol'] - 14.0 * flow['heavy_naphtha', 'regular_petrol'] + 31.0 * flow['reformed_gasoline', 'regular_petrol'] + 21.0 * flow['cracked_gasoline', 'regular_petrol'] >= 0.0;
con blending_petrol_premium_petrol : - 4.0 * flow['light_naphtha', 'premium_petrol'] - 14.0 * flow['medium_naphtha', 'premium_petrol'] - 24.0 * flow['heavy_naphtha', 'premium_petrol'] + 21.0 * flow['reformed_gasoline', 'premium_petrol'] + 11.0 * flow['cracked_gasoline', 'premium_petrol'] >= 0.0;
con blending_jet_fuel : - 0.4 * flow['heavy_oil', 'jet_fuel'] + 0.5 * flow['cracked_oil', 'jet_fuel'] - 0.95 * flow['residuum', 'jet_fuel'] <= 0.0;
con blending_fuel_oil_light_oil_fuel_oil : 8 * flow['light_oil', 'fuel_oil'] - 10 * flow['cracked_oil', 'fuel_oil'] - 10 * flow['heavy_oil', 'fuel_oil'] - 10 * flow['residuum', 'fuel_oil'] = 0;
con blending_fuel_oil_heavy_oil_fuel_oil : 15 * flow['heavy_oil', 'fuel_oil'] - 3 * flow['cracked_oil', 'fuel_oil'] - 3 * flow['light_oil', 'fuel_oil'] - 3 * flow['residuum', 'fuel_oil'] = 0;
con blending_fuel_oil_cracked_oil_fuel_oil : 14 * flow['cracked_oil', 'fuel_oil'] - 4 * flow['heavy_oil', 'fuel_oil'] - 4 * flow['light_oil', 'fuel_oil'] - 4 * flow['residuum', 'fuel_oil'] = 0;
con blending_fuel_oil_residuum_fuel_oil : 17 * flow['residuum', 'fuel_oil'] - flow['cracked_oil', 'fuel_oil'] - flow['heavy_oil', 'fuel_oil'] - flow['light_oil', 'fuel_oil'] = 0;
con crude_total_ub : crudesDistilled['crude1'] + crudesDistilled['crude2'] <= 45000;
con naphtba_ub : flow['light_naphtha', 'reformed_gasoline'] + flow['medium_naphtha', 'reformed_gasoline'] + flow['heavy_naphtha', 'reformed_gasoline'] <= 10000;
con cracked_oil_ub : flow['light_oil_cracked', 'cracked_oil'] + flow['heavy_oil_cracked', 'cracked_oil'] <= 8000;
con lube_oil_range : 500 <= flow['lube_oil', 'sink'] <= 1000;
con premium_ratio : flow['premium_petrol', 'sink'] - 0.4 * flow['regular_petrol', 'sink'] >= 0.0;
solve;
quit;