from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uuid
import json
from db_control import crud, mymodels_MySQL


#MySQLのテーブル作成
from db_control.create_tables_MySQL import init_db

# アプリケーション初期化時にテーブルを作成
init_db()


class Customer(BaseModel):
    customer_id: str
    customer_name: str
    age: int
    gender: str

class CustomerCreate(BaseModel):
    #customer_id: str
    customer_name: str
    age: int
    gender: str

app = FastAPI()


# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "FastAPI top page!"}


@app.post("/customers")
def create_customer(customer: CustomerCreate):
    MAX_ATTEMPT =10
    attempts =0
    while attempts < MAX_ATTEMPT:
        attempts += 1

    generated_id = str(uuid.uuid4())
    print(f"Attempt {attempts}: generated_id: {generated_id}")

    #IDが存在しない場合のみ処理を実行
    if generated_id != crud.myselect(mymodels_MySQL.Customers, generated_id):
        # 受け取ったデータにcustomer_idを追加
        values = customer.dict()
        values["customer_id"] =generated_id
        #print("values:", values)

    #データベースに保存
        tmp = crud.myinsert(mymodels_MySQL.Customers,values)
        result = crud.myselect(mymodels_MySQL.Customers, generated_id)

        if result:
                result_obj = json.loads(result)
                return result_obj[0] if result_obj else None
        return None

@app.get("/customers")
def read_one_customer(customer_id: str = Query(...)):
    result = crud.myselect(mymodels_MySQL.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None


@app.get("/allcustomers")
def read_all_customer():
    result = crud.myselectAll(mymodels_MySQL.Customers)
    # 結果がNoneの場合は空配列を返す
    if not result:
        return []
    # JSON文字列をPythonオブジェクトに変換
    return json.loads(result)


@app.put("/customers")
def update_customer(customer: CustomerCreate):
    # クライアントから受け取ったデータを辞書形式に変換
    values = customer.dict()

    # customer_idをクライアントからではなくサーバー側で生成
    generated_id = str(uuid.uuid4())  # もしくはリクエストからIDを受け取る方法も可能

    # 受け取ったデータにcustomer_idを追加
    values["customer_id"] = generated_id

    # DBに保存
    tmp = crud.myupdate(mymodels_MySQL.Customers, values)
    
    # DBから顧客情報を取得
    result = crud.myselect(mymodels_MySQL.Customers, generated_id)
    
    # 顧客が存在しない場合は404エラー
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")

    # 顧客情報をJSON形式に変換
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None



@app.delete("/customers")
def delete_customer(customer_id: str = Query(...)):
    result = crud.mydelete(mymodels_MySQL.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer_id": customer_id, "status": "deleted"}


@app.get("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json()

@app.put("/customers/{customer_id}")
def update_customer(customer_id: str, customer: CustomerCreate):
    # 受け取ったデータを辞書形式に変換
    values = customer.dict()
    
    # URLパラメータから取得した customer_id を使って更新
    values["customer_id"] = customer_id

    # 顧客情報をDBで更新
    tmp = crud.myupdate(mymodels_MySQL.Customers, values)
    
    # 更新された顧客情報をDBから取得
    result = crud.myselect(mymodels_MySQL.Customers, customer_id)
    
    # 顧客が存在しない場合は404エラー
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")

    # 顧客情報をJSON形式に変換して返す
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

