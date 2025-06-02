from dateutil import parser
from datetime import timezone, timedelta
from IPython.display import display
import pandas


class Dataread():
    def __init__(self) -> None:
        pass


    def iso_time(self, timedata, criteria=None):
        """
        iso 형식의 시간을 utc 형태로 변경
        criteria = none (utc)
        criteria = 'kst' (kst) 로 반환
        """
        try:
            dt_utc = parser.isoparse(timedata)
        except:
            print("ERROR : Can not be converted into utc type." \
            "Continue with type changing")
            try:
                timedata = timedata.astype(int)
            except:
                print("ERROR : Can not change type to int")
                try:
                    timedata = timedata.astype('Int64')
                except:
                    print("ERROR : Could not complete requested work : converting iso time to utc format ")
                    return
        
        dt_utc = parser.isoparse(timedata)
        
        if criteria == 'kst':
            dt_kst = dt_utc.astimezone(timezone(timedelta(hours=9)))
            return dt_kst
        
        return dt_utc
    
    def baseinfo(self, df):
        """
        데이터의 전체 행과 결측값, head(6)를 반환
        """
        print(df.shape)
        display(df.isna().sum())
        display(df.head(6))
        return
        
    def hackle_baseinfo(self, df):
        """
        hackle 추가 데이터에서 event_key의 종류와 user_id의 종류를 파악하는 기본 함수
        """
        display(df.head(6))
        print(df.shape)
        print('-' * 30)
        try:
            print('\nEvent_key')
            print(df['event_key'].nunique(), df['event_key'].unique())
        except:
            print('There is no "event_key" column.')

        try:
            print('\nuser_id')
            print(df['user_id'].nunique(), df['user_id'].unique())
        except:
            print('There is no "user_id" column.')
        return
    
