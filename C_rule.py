import pandas as pd
import os

# import

def C_rule(finance_data_path,stock_code,buy_date,disclosure_result_path):
    # disclosure_result_path = 'D:/pydir/Raw Data/Tushare_pro/disclosure_date/'
    disclosure_result_data = pd.read_csv(disclosure_result_path + 'total_disclosure.csv')
    # report_date = disclosure_result_data[(disclosure_result_data['stock_code'] == int(stock_code)) and ]
    # print('--------------'+stock_code+'----------------')
    if os.path.exists(finance_data_path + stock_code + '.csv'):
        select_df = disclosure_result_data[disclosure_result_data['stock_code'] == int(stock_code)]
        select_df = select_df.reset_index(drop=True)
        for index in range(len(select_df)-1):
            if (int(select_df['actual_date'].tolist()[index]) < int(buy_date)) and \
                    (int(select_df['actual_date'].tolist()[index+1]) >= int(buy_date)):
                end_date = select_df['end_date'].tolist()[index]
                break
        if int(buy_date) >= int(select_df['actual_date'].tolist()[len(select_df)-1]):
            end_date = select_df['end_date'].tolist()[len(select_df)-1]
        stock_finance_data = pd.read_csv(finance_data_path + stock_code + '.csv')
        select_index = stock_finance_data['end_date'].tolist().index(int(end_date))
        # print(select_index)
        eps_yoy_list = stock_finance_data['basic_eps_yoy'].tolist()
        eps_current = eps_yoy_list[select_index]
        eps_pre_1 = eps_yoy_list[select_index+1]
        eps_pre_2 = eps_yoy_list[select_index+2]
        eps_pre_3 = eps_yoy_list[select_index+3]

        diff_eps_current = eps_current - eps_pre_1
        diff_eps_1 = eps_pre_1 - eps_pre_2
        diff_eps_2 = eps_pre_2 - eps_pre_3

        if (eps_current > 40) and (diff_eps_current - diff_eps_1) > 0 and (diff_eps_1-diff_eps_2) > 0:
            satisfy_c_rule = 'True'
            # print('True')
        else:
            satisfy_c_rule = 'False'
    else:
        satisfy_c_rule = 'N'

    return satisfy_c_rule

