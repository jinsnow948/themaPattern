import re
import pandas as pd
from pykrx import stock

directory = "D:/OneDrive/문서/주식/"


def read_file(path):
    f = open(path, 'rt', encoding='UTF8')
    regex = "\(.*\)|\s-\s.*"
    lines = f.readlines()
    df = pd.DataFrame()

    for line in lines:
        first_word = line[:12]
        second_word = line[13:]
        regex = "\(.*\)|\s-\s.*"
        내용 = re.sub(regex, '', second_word)
        날짜 = re.sub(r'[^0-9]', '', first_word)
        종목리스트 = re.findall('\((주도주[^)]+)', second_word)

        전체시세 = stock.get_market_price_change(날짜, 날짜, market="ALL")
        코스피 = stock.get_index_price_change(날짜, 날짜, "KOSPI")
        코스닥 = stock.get_index_price_change(날짜, 날짜, "KOSDAQ")

        # 코스닥 = 코스닥.loc[(코스닥['지수명'] == '코스닥지수')]
        코스닥 = 코스닥.iloc[0]
        # print(코스닥)
        코스닥등락률 = 코스닥['등락률']
        # print(코스닥등락률)
        # 코스피 = 코스피.loc[(코스피['지수명'] == '코스피')]
        코스피 = 코스피.iloc[0]
        # print(코스피)
        코스피등락률 = 코스피['등락률']
        # print(전체시세)
        print(f'날짜 {날짜} 코스닥등락률 {코스닥등락률}, 코스피등락률 {코스피등락률}')

        if 종목리스트:
            max_per = 1
            종목리스트 = 종목리스트[0].split(':')
            print(f'날짜 : {날짜} \n종목 : ')
            print(f'종목리스트 {종목리스트}')

            for 종목 in 종목리스트[1].split(','):
                print(f'종목 {종목}')
                종목 = 종목.strip()
                종목시세 = 전체시세.loc[(전체시세['종목명'] == 종목)]
                print(f'종목시세 {종목시세}')
                if 종목시세.empty:
                    continue
                일일등락률 = 종목시세['등락률'][0]
                종가 = 종목시세['종가'][0]

                # df1 = pd.DataFrame([{'{}'.format(종목): 일일등락률}], index=[날짜])
                # df = pd.concat([df, df1], axis=0)
                print(f'일일등락률 : {일일등락률}')
                print(f'종가 : {종가}')

                if 일일등락률 > max_per:
                    # 대장주 = 종목
                    # if 종목 not in df.columns:
                    #     df['{}'.format(종목)] = ''
                    max_per = 일일등락률
                    max_dict = {'{}'.format(종목): 일일등락률}
                # print(f'종목 = {종목}, {locals()["{}_df".format(종목)]}')

                # 등락률 = 전체시세.loc[전체시세['종목명'] == 종목]['등락률']
            df1 = pd.DataFrame([max_dict], index=[날짜])
            df1['기사'] = 내용
            df1['코스피'] = 코스피등락률
            df1['코스닥'] = 코스닥등락률
            df = pd.concat([df, df1], axis=0)

        else:
            print(f'종목없음!!')
            print(f'날짜 : {날짜}')
            df1 = pd.DataFrame([{}], index=[날짜])
            df1['기사'] = 내용
            df1['코스피'] = 코스피등락률
            df1['코스닥'] = 코스닥등락률
            df = pd.concat([df, df1], axis=0)

    print(df)
    with pd.ExcelWriter(directory + "테마.xlsx") as writer:
        df.to_excel(writer, sheet_name='원숭이두창')


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    file_path = directory + '원숭이두창.txt'
    read_file(file_path)
