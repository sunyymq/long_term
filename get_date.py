import pandas as pd
import numpy as np

def get_week_start_date(last_week_end,daily_stock_path):
    data_orgin_1 = pd.read_csv(daily_stock_path + '/000001.csv')
    data_orgin_1_date_list = data_orgin_1['trade_date'].tolist()
    data_orgin_2 = pd.read_csv(daily_stock_path + '/600519.csv')
    data_orgin_2_date_list = data_orgin_2['trade_date'].tolist()
    # print(last_week_end)
    if last_week_end not in data_orgin_1_date_list:
        current_date_index = data_orgin_2_date_list.index(last_week_end)
        week_start_date = data_orgin_2_date_list[current_date_index+1]
    else:
        current_date_index = data_orgin_1_date_list.index(last_week_end)
        week_start_date = data_orgin_1_date_list[current_date_index+1]
    return week_start_date


def get_week_date_list(week_start_date,week_end_date,daily_stock_path):
    #读取数据源，
    data_orgin_1 = pd.read_csv(daily_stock_path + '/000001.csv')
    data_orgin_1_date_list = data_orgin_1['trade_date'].tolist()
    data_orgin_2 = pd.read_csv(daily_stock_path + '/600519.csv')
    data_orgin_2_date_list = data_orgin_2['trade_date'].tolist()
    data_orgin_3 = pd.read_csv(daily_stock_path + '/600030.csv')
    data_orgin_3_date_list = data_orgin_3['trade_date'].tolist()

    total_data_list = list(set(data_orgin_1_date_list) | set(data_orgin_2_date_list) | set(data_orgin_3_date_list))
    total_data_list.sort()
    # print(total_data_list)
    start_index = total_data_list.index(week_start_date)
    end_index = total_data_list.index(week_end_date)
    week_date_list = total_data_list[start_index:end_index+1]
    return week_date_list

def get_first_observe_date(single_stock_data,week_end_date):
    date_list_in_daily = single_stock_data['trade_date'].tolist()
    first_observe_date = 0xffff
    if week_end_date in date_list_in_daily[:-1]:
        week_end_date_index = date_list_in_daily.index(week_end_date)
        first_observe_date = date_list_in_daily[week_end_date_index+1]
    else:
        for single_date_index in range(len(date_list_in_daily)-1):
            if week_end_date > date_list_in_daily[single_date_index] \
                    and week_end_date < date_list_in_daily[single_date_index +1]:
                first_observe_date = date_list_in_daily[single_date_index + 1]
    if first_observe_date == 0xffff:
        first_observe_date = np.nan
    return first_observe_date

def get_buy_date_10(single_stock_data,single_stock_week_data,first_observe_date):
    single_stock_week_list = single_stock_week_data['trade_date'].tolist()
    # first_observe_date_index = single_stock_week_list.index(first_observe_date)
    first_observe_date_index = single_stock_data['trade_date'].tolist().index(first_observe_date)
    # print(first_observe_date_index)
    # print(single_stock_data['trade_date'].tolist()[first_observe_date_index-1])
    if single_stock_data['trade_date'].tolist()[first_observe_date_index-1] in single_stock_week_list:
        first_pre_weekend_index = single_stock_week_list.index\
            (single_stock_data['trade_date'].tolist()[first_observe_date_index-1])
    else:
        for index in range(len(single_stock_data)-first_observe_date_index-1):
            if single_stock_data['trade_date'].tolist()[first_observe_date_index+index] in single_stock_week_list:
                first_pre_weekend_index = single_stock_week_list.index \
                    (single_stock_data['trade_date'].tolist()[first_observe_date_index+index])
                break
    # print(first_pre_weekend_index+1)
    # print(len(single_stock_week_list)-1)
    # print('--------------')
    buy_date = 0xffff
    if first_observe_date < single_stock_week_list[-1]:
        for week_index in range(first_pre_weekend_index+1, len(single_stock_week_list)-1):
            pre_week_highest_price = single_stock_week_data['high'].tolist()[week_index]
            pre_week_10k_ma = single_stock_week_data['ma5'].tolist()[week_index]
            pre_weekend_date = single_stock_week_data['trade_date'].tolist()[week_index]

            if pre_week_10k_ma >= pre_week_highest_price:
                if pre_weekend_date in single_stock_data['trade_date'].tolist():
                    pre_weekend_index_in_daily = single_stock_data['trade_date'].tolist().index(pre_weekend_date)
                    buy_date = single_stock_data['trade_date'].tolist()[pre_weekend_index_in_daily+1]
                    break
                else:
                    for index in range(first_observe_date_index,len(single_stock_data)-1):
                        if single_stock_data['trade_date'].tolist()[index] < pre_weekend_date and \
                                single_stock_data['trade_date'].tolist()[index+1] > pre_weekend_date:
                            pre_weekend_index_in_daily = index
                            break
                    buy_date = single_stock_data['trade_date'].tolist()[pre_weekend_index_in_daily + 1]
                    break
            # if week_index == len(single_stock_week_list)-2:
            #     buy_date = np.nan
    if buy_date == 0xffff:
        buy_date = np.nan
    return buy_date

def get_buy_date_x(single_stock_data,single_stock_x_data,first_observe_date,x):
    single_stock_date_list = single_stock_x_data['trade_date'].tolist()
    # first_observe_date_index = single_stock_week_list.index(first_observe_date)
    first_observe_date_index = single_stock_data['trade_date'].tolist().index(first_observe_date)
    # print(first_observe_date_index)
    # print(single_stock_data['trade_date'].tolist()[first_observe_date_index-1])
    if single_stock_data['trade_date'].tolist()[first_observe_date_index-1] in single_stock_date_list:
        first_pre_index = single_stock_date_list.index\
            (single_stock_data['trade_date'].tolist()[first_observe_date_index-1])
    else:
        for index in range(len(single_stock_data)-first_observe_date_index-1):
            if single_stock_data['trade_date'].tolist()[first_observe_date_index+index] in single_stock_date_list:
                first_pre_index = single_stock_date_list.index \
                    (single_stock_data['trade_date'].tolist()[first_observe_date_index+index])
                break
    # print(first_pre_weekend_index+1)
    # print(len(single_stock_week_list)-1)
    # print('--------------')
    buy_date = 0xffff
    if first_observe_date < single_stock_date_list[-1]:
        for week_index in range(first_pre_index+1, len(single_stock_date_list)-1):
            pre_week_highest_price = single_stock_x_data['high'].tolist()[week_index]
            x_ma = 'ma'+str(x)
            pre_x_ma = single_stock_x_data[x_ma].tolist()[week_index]
            pre_weekend_date = single_stock_x_data['trade_date'].tolist()[week_index]

            if pre_x_ma >= pre_week_highest_price:
                if pre_weekend_date in single_stock_data['trade_date'].tolist():
                    pre_weekend_index_in_daily = single_stock_data['trade_date'].tolist().index(pre_weekend_date)
                    buy_date = single_stock_data['trade_date'].tolist()[pre_weekend_index_in_daily+1]
                    break
                else:
                    for index in range(first_observe_date_index,len(single_stock_data)-1):
                        if single_stock_data['trade_date'].tolist()[index] < pre_weekend_date and \
                                single_stock_data['trade_date'].tolist()[index+1] > pre_weekend_date:
                            pre_weekend_index_in_daily = index
                            break
                    buy_date = single_stock_data['trade_date'].tolist()[pre_weekend_index_in_daily + 1]
                    break
            # if week_index == len(single_stock_week_list)-2:
            #     buy_date = np.nan
    if buy_date == 0xffff:
        buy_date = np.nan
    return buy_date