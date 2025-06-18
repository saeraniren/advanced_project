from IPython.display import display
import pandas as pd


class Dataread():
    def __init__(self) -> None:
        pass
    
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
    
    
    def create_startend_dataframe(self, df):
        """
        start와 end 기록이 동시에 존재하는 session을 선별한 후
        start, end가 순서대로 이어지도록 구성한 DataFrame을 반환하는 함수
        """
        # session 선별
        try:
            session_events_count = df.groupby('session_id')['event_key'].nunique()
            valid_session = session_events_count[session_events_count == 2].index
            valid_df = df[df['session_id'].isin(valid_session)].copy()
        except:
            print("Wrong DataFrame input: check dataframe has 'session_id','event_key'")
            return

        # 시간 순으로 정렬
        try:
            valid_df = valid_df.sort_values(by=['session_id','Asia/Seoul'])
        except:
            print("Wrong DataFrame input: check df has 'Asia/Seoul' which records timestamp")

        rows = []
        session_id = None
        start_time = None
        start_error = False



        for idx, row in valid_df.iterrows():
            current_id = row['session_id']
            current_event = row['event_key']
            current_time = row['Asia/Seoul']

            # 첫 행 세션 아이디 기록
            if session_id is None:
                # 예외 상황 (end로 시작)
                if current_event != '$session_start':
                    # 에러 기록 후 다음 행으로
                    start_error = True
                    continue
                
                # 정상 상황 (start로 시작)
                session_id = current_id
                start_time = current_time
                continue 

            
            # session_id가 다른 경우 초기화
            # (session이 비정상적으로 종료된 경우, start - ... end없이 -> 새로운 세션 start or end한 경우)
            if current_id != session_id:
                if start_time:
                    rows.append({
                            'session_id' : session_id,
                            'start_time' : start_time,
                            'end_time' : None,
                            'end_error' : True
                        })
                
                # 새로운 세션 시작    
                session_id = current_id
                start_time = None
                
                # 새로운 세션의 스타트 여부 판단
                if current_event == '$session_start':
                    start_time = current_time
                    start_error = False
                
                # 새로운 세션이 비정상 시작 (end로 시작)한 경우
                else:
                    start_error = True
                
                # 다음행으로
                continue


            # 다음 행과 이전행의 session_id가 동일한 경우. (동일하지 않은 경우를 if로 분기했기 때문에, 자연스럽게 else와 의미가 같음)
            
            # 해당 session이 end_session으로 데이터가 시작된 경우 = start_error == True
            if start_error:
                # end_session으로 시작했으나, 그 다음이 정상적으로 start인 경우
                if current_event == '$session_start':
                    start_time = current_time
                    start_error = False
                
                # end_session으로 시작했으며, 그 다음도 end_session인 경우
                continue
                
                
            
            # start session으로 시작하고, end세션으로 끝난 경우, rows에 추가
            if current_event == '$session_end':
                rows.append({
                        'session_id' : session_id,
                        'start_time' : start_time,
                        'end_time' : current_time,
                        'end_error' : False
                    })
                
                # 초기화
                session_id = None
                start_time = None
                start_error = False
                # 다음행으로
                continue
            
            # start후 end 없이 동일한 세션이 start한 경우
            rows.append({
                        'session_id' : session_id,
                        'start_time' : start_time,
                        'end_time' : None,
                        'end_error' : True          # end없이 start했기 때문
                    })

            # 세션의 새로운 start 기록
            start_time = current_time
            continue
            

        # 마지막에 end없이 끝났다면
        if session_id is not None and start_time is not None:
            rows.append({
                'session_id': session_id,
                'start_time': start_time,
                'end_time': None,
                'end_error': True
            })
        
        rows_df = pd.DataFrame(rows)
        rows_df['start_time'] = pd.to_datetime(rows_df['start_time'], utc=True, errors='coerce')
        rows_df['end_time'] = pd.to_datetime(rows_df['end_time'], utc=True, errors='coerce')
        return rows_df
    
    def culmulative_count(self, df):
        '''
        5~7월 'created_at'을 활용한 누적 합 dict을 반환
        '''
        result = {}
        mask1 = df['created_at'] >= '2023-05-01'
        week = pd.to_datetime('2023-05-01')
        while True:
            mask2 = df['created_at'] < week
            result[week] = df.loc[(mask1) & (mask2)].shape[0]
            if week > pd.to_datetime('2023-08-01'):
                break
            week = week + pd.Timedelta(days=7)
        result_df = pd.DataFrame(list(result.items()), columns=['week', 'count'])
        return result_df

    def weekly_count(self, df):
        '''
        5~7월 'created_at'을 활용한 주간 계 dict을 반환
        '''
        week0 = pd.to_datetime('2023-05-01')
        week1 = pd.to_datetime('2023-05-01') + pd.Timedelta(days=7)
        result = {}

        while True:
            mask1 = df['created_at'] > week0
            mask2 = df['created_at'] < week1
            result[week0.strftime('%Y-%m-%d')] = df.loc[(mask1) & (mask2)].shape[0]
            if week1 > pd.to_datetime('2023-08-01'):
                break
            week0 = week0 + pd.Timedelta(days=7)
            week1 = week1 + pd.Timedelta(days=7)
            
        result_df = pd.DataFrame(list(result.items()), columns=['week', 'count'])
        return result_df
            


