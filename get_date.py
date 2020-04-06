import pandas as pd

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

def get_first_observe_date(single_stock_data,first_week_date):
    date_list_in_daily = single_stock_data['trade_date'].tolist()
    if first_week_date in date_list_in_daily:
        first_observe_date = first_week_date
    else:
        for single_date_index in range(len(date_list_in_daily)-1):
            if first_week_date > date_list_in_daily[single_date_index] \
                    and first_week_date < date_list_in_daily[single_date_index +1]:
                first_observe_date = date_list_in_daily[single_date_index + 1]
    return first_observe_date