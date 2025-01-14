## 1/14

### 无源 API

检查发现 `S-S_eval.json` （原始文件）第 91 行存在问题：

```json
[
    "candidate_apis":[
        {
            "name": "ReserveHotel",
            "description": "Reserve rooms at a selected place for given dates",
            "required_parameters": [
            "place_name", "check_in_date", "stay_length", "location"]
            "optional_parameters": {
            "number_of_rooms": "1"},
            "result_parameters": [
            "location", "number_of_rooms", "check_in_date", "stay_length", "star_rating", "place_name", "street_address", "phone_number", "price_per_night", "smoking_allowed"]
        },
        {
            "name": "SearchHotel",
            "description": "Look for accommodation in a city of choice",
            "required_parameters": ["location"],
            "optional_parameters": {
            "smoking_allowed": "dontcare",
            "star_rating": "dontcare",
            "number_of_rooms": "dontcare"},
            "result_parameters": [
            "location", "number_of_rooms", "star_rating", "place_name", "street_address", "phone_number", "price_per_night", "smoking_allowed"]
        }
    ]
  {
    "id": "S-S_90",
    "answer": {
      "FindRestaurants": {
        "city": "Campbell",
        "cuisine": "Italian",
        "price_range": "moderate"}
    }
  },
]
```
`FindRestaurants` 不属于被提供的 API 列表 ["ReserveHotel","SearchHotel"]，对各包进行检查:

1. S-S, 30 mistakes
2. S-M, 0 mistake
3. M-S, 1 mistake
4. M-M, 34 mistakes

新 eval 存储在各自的文件夹中， 命名为 `eval_new.json`

### 相关文件

#### 旧文件更新

##### MTU-Bench/25.1.8/X-X/to_standard.py

`Version` 参数由 1.0 变更为 2.0， `eval_standard_Ver2.0` 相比 `eval_standard_Ver1.0` 新增 ID 属性

##### check_eval.py

检查 `eval.json` 中 response 违法的条目，并输出错误条目至 `response_invalid.json`.

#### 新增文件

##### update_eval.py

读取 `eval.json` 并删除 response 违法的条目，将合法条目输出至 `eval_new.json`.


