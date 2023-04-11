import requests
import pandas as pd
import json
import datetime

def power(x,y):
    if y == 0:
        return 1
    t = power(x,y // 2)
    if y % 2 == 0:
        return t*t
    else :
        return x*t*t
    
def split_datatime(datatime):
    times = datatime.split()
    
    # Split ngày
    days = times[0]
    splitdays = days.split('-')
    day = splitdays[2]
    month = splitdays[1]
    year = splitdays[0]

    # Split giờ
    time = times[1]
    splittime = time.split(':')
    hour = splittime[0]
    minutes = splittime[1]
    second = splittime[2]

    dict = {}
    dict["datatime"] = datatime
    dict["day"] = int(day)
    dict["month"] = int(month)
    dict["year"] = int(year)
    dict["hour"] = int(hour)
    dict["minutes"] = int(minutes)
    dict["second"] = int(second)
    return dict

def ProcessingData(address, page, offset, apiKey):
    # Gọi api để trả vể data
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&page={page}&offset={offset}&startblock=0&endblock=27025780&sort=desc&apikey={apiKey}"
    response = requests.request("GET", url)
    data = response.json()
    results = data["result"]
    # final list quản lý thông tin chung của các token và từng giao dịch được tải về 
    final_list = []
    # list_token_name quản lí xme những token nào đã được đưa vào final_list để quản lý
    list_token_name = []

    # Xử lý data
    for result in results:
        token_Name = result["tokenName"]
        token_Symbol = result["tokenSymbol"]
        token_Decimal = result["tokenDecimal"]
        token_From = result["from"]
        token_To = result["to"]
        token_Value = int(result["value"])/power(10,int(token_Decimal))
        token_time = split_datatime(str(datetime.datetime.fromtimestamp(int(result["timeStamp"]))))
        token_BlockNumber = result["blockNumber"]
        token_Hash = result["hash"]
        if token_Name not in list_token_name:
            list_token_name.append(token_Name)
            token_dict = {}
            token_dict["tokenName"] = token_Name
            token_dict["tokenSymbol"] = token_Symbol
            token_dict["tokenDecimal"] = token_Decimal
            token_dict["tokenTrans"] = []
            tmp = {}
            tmp["from"] = token_From
            tmp["to"] = token_To
            tmp["value"] = token_Value
            tmp["time"] = token_time
            # Tính lượng Coin ra vào ví sàn của mỗi giao dịch
            if token_From == address:
                tmp["value_out"] = int(token_Value)
                tmp["value_in"] = 0
            else:
                if token_To == address:
                    tmp["value_out"] = 0
                    tmp["value_in"] = int(token_Value)
            tmp["blockNumber"] = token_BlockNumber
            tmp["hash"] = token_Hash
            token_dict["tokenTrans"].append(tmp)
            final_list.append(token_dict)

        else:
            for token in final_list:
                if token_Name == token["tokenName"]:
                    tmp = {}
                    tmp["from"] = token_From
                    tmp["to"] = token_To
                    tmp["value"] = token_Value
                    tmp["time"] = token_time
                    # Tính lượng Coin ra vào ví sàn của mỗi giao dịch
                    if token_From == address:
                        tmp["value_out"] = int(token_Value)
                        tmp["value_in"] = 0
                    else:
                        if token_To == address:
                            tmp["value_out"] = 0
                            tmp["value_in"] = int(token_Value)
                    tmp["blockNumber"] = token_BlockNumber
                    tmp["hash"] = token_Hash
                    token["tokenTrans"].append(tmp)
    # Lưu lại vào file response_format
    with open('response_format.json', 'w') as f:
                json.dump(final_list, f, indent=4)
    return final_list

if __name__ == "__main__":
    apiKey = "PSI4IFEFAUF8USVB6M5BSEAM1VB9CX7FJZ"
    data = pd.read_csv('src/input.csv')
    test_address = data['address'].values
    address = test_address[0]
    page = 1
    offset = 10000
    list = ProcessingData(address, page, offset,apiKey)
    ProcessingData(address,page,offset,apiKey)


