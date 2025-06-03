import pandas as pd
import gcsfs
import pyarrow.parquet as pq

JSON_KEY_PATH = "./sprintda05-soomin.json"
BUCKET_NAME = "final-project-soomin/final_project"
storage_options = {'token':JSON_KEY_PATH}

class DatasetType:
    def __init__(self, dataset_type: str):
        self.dataset_type = dataset_type.lower()
        self.fs = gcsfs.GCSFileSystem(token=JSON_KEY_PATH)

    # 파일 이름 목록 확인하기
    def file_list(self):
        folder = f"{BUCKET_NAME}/{self.dataset_type}"
        
        try:
            files = self.fs.ls(folder)
        except Exception as e:
            print(f"Error accessing GCS folder: {folder}: {e}")
            return []
        
        parquet_files = [
            f.split('/')[-1].replace('.parquet', '') 
            for f in files 
            if f.endswith('.parquet')
            ]
        
        json_files = [ 
            f.split('/')[-1].replace('.json', '') 
            for f in files 
            if f.endswith('.json')
            ]
        
        return sorted(parquet_files + json_files)
    
    # 데이터 읽어서 DataFrame으로 반환하기
    def _read_parquet(self, filename: str):
        try:
            path = f"gs://{BUCKET_NAME}/{self.dataset_type}/{filename}.parquet"
            df = pd.read_parquet(
            path,
            storage_options={"token": JSON_KEY_PATH},
            engine='pyarrow'
            )
        except:
            path = f"gs://{BUCKET_NAME}/{self.dataset_type}/{filename}.json"
            df = pd.read_json(
            path_or_buf = path,
            storage_options={"token": JSON_KEY_PATH}
            )
        
        return df
    
    # 경로를 직접 입력하여 데이터의 컬럼만 읽어오기
    def column_list(self, filename : str, file_type: str = 'parquet'):
        path = f"gs://{BUCKET_NAME}/{self.dataset_type}/{filename}.{file_type}"

        try:
            column_table = pq.read_table(path)
            return (column_table.schema)
        
        except:
            print('JSON 파일은 현재 지원하지 않습니다.')
            return
        


    # 도움말
    def help(self):
        print("""
다음과 같은 방식으로 사용합니다.
Dataset().hackle.device_properties()
              혹은
ds = Dataset()
ds.votes.accounts_user()

ds.votes.file_list()  와 같은 방법으로 호출에 필요한 파일 이름을 확인할 수 있습니다. 
ds.additional_hackle.column_list(file_name, file_type(default:parquet)) 와 같은 방법으로 컬럼명을 호출할 수 있습니다.
ds.additional_hackle은 파일 읽어오기를 아직 지원하지 않습니다.           
""")
        
    ## hackle 데이터셋 읽어오기
    def device_properties(self):
        return self._read_parquet("device_properties")

    def hackle_events(self):
        return self._read_parquet("hackle_events")
    
    def hackle_properties(self):
        return self._read_parquet("hackle_properties")
    
    def user_properties(self):
        return self._read_parquet("user_properties")
    
    ## vote 데이터셋 읽어오기
    def accounts_attendance(self):
        return self._read_parquet("accounts_attendance")
    
    def accounts_blockrecord(self):
        return self._read_parquet("accounts_blockrecord")
    
    def accounts_failpaymenthistory(self):
        return self._read_parquet("accounts_failpaymenthistory")
    
    def accounts_friendrequest(self):
        return self._read_parquet("accounts_friendrequest")
    
    def accounts_group(self):
        return self._read_parquet("accounts_group") 
    
    def accounts_nearbyschool(self):
        return self._read_parquet("accounts_nearbyschool")

    def accounts_school(self):
        return self._read_parquet("accounts_school")
    
    def accounts_paymenthistory(self):
        return self._read_parquet("accounts_paymenthistory")
    
    def accounts_pointhistory(self):
        return self._read_parquet("accounts_pointhistory")
    
    def accounts_timelinereport(self):
        return self._read_parquet("accounts_timelinereport")
    
    def accounts_user(self):
        return self._read_parquet("accounts_user")
    
    def accounts_user_contacts(self):
        return self._read_parquet("accounts_user_contacts")
    
    def accounts_userquestionrecord(self):
        return self._read_parquet("accounts_userquestionrecord")
    
    def accounts_userwithdraw(self):
        return self._read_parquet("accounts_userwithdraw")
    
    def event_receipts(self):
        return self._read_parquet("event_receipts")
    
    def events(self):
        return self._read_parquet("events")
    
    def polls_question(self):
        return self._read_parquet("polls_question")
    
    def polls_questionpiece(self):
        return self._read_parquet("polls_questionpiece")
    
    def polls_questionreport(self):
        return self._read_parquet("polls_questionreport")
    
    def polls_questionset(self):    
        return self._read_parquet("polls_questionset")
    
    def polls_usercandidate(self):
        return self._read_parquet("polls_usercandidate")

class Dataset:
    def __init__(self):
        self.hackle = DatasetType("hackle")
        self.votes = DatasetType("votes")
        self.vote = DatasetType("votes")
        self.additional_hackle = DatasetType("additional_hackle")
        
            # 도움말
    def help(self):
        print("""
다음과 같은 방식으로 사용합니다.
Dataset().hackle.device_properties()
              혹은
ds = Dataset()
ds.votes.accounts_user()

ds.votes.file_list()  와 같은 방법으로 호출에 필요한 파일 이름을 확인할 수 있습니다.
ds.additional_hackle.column_list(file_name, file_type(default:parquet)) 와 같은 방법으로 컬럼명을 호출할 수 있습니다.
ds.additional_hackle은 파일 읽어오기를 아직 지원하지 않습니다.                       
""")
    