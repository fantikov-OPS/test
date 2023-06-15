import uvicorn
import re
import redis
from functools import lru_cache
from fastapi import FastAPI, HTTPException

app = FastAPI()


#можно конечно делать через aioredis и роуты тоде асинхронными, но это по желанию

redis_client = redis.Redis(host='redis', port=6379)


#регулярочка для номера, по идее надо как то и адресс валидить, но как - мало входных
PHONE_REGEX = r'^375\d{2}\d{3}\d{2}\d{2}$'


#ситуативно, я бы кешировал
@lru_cache(maxsize=128)
def get_address_from_cache(phone):
    address = redis_client.get(phone)
    return address.decode() if address else None

@app.post("/write_data")
def write_data(phone: str, address: str):
    #номер не норме, как пример открыдваем 400
    if not re.match(PHONE_REGEX, phone.strip()):
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    try:
        redis_client.set(phone, address)
    except redis.RedisError:
        #что то с редисом
        raise HTTPException(status_code=500, detail="Cannot write data to Redis")
    return {"message": "Data updated successfully"}

#аналогично предыдущему
@app.get("/check_data")
def check_data(phone: str):
    # print(phone.strip())
    if not re.match(PHONE_REGEX, phone.strip()):
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    try:
        address = get_address_from_cache(phone)
        if not address:
            address = redis_client.get(phone)
            if address:
                redis_client.set(phone, address)
                address = address.decode()
            else:
                raise HTTPException(status_code=404, detail="Data not found")
    except redis.RedisError:
        raise HTTPException(status_code=500, detail="Cannot read data from Redis")
    return {"address": address}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)