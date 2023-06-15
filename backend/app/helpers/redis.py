import redis
import json


def redis_get_list(r:redis.Redis,key:str)->list:
    r_range = r.llen(key)
    data = r.lrange(key,0,r_range)
    return [i.decode('utf-8') for i in data]

def redis_add_list(r:redis.Redis,key:str,values:list)->bool:
    try:
        for item in values:
            r.lpush(key,item)
    except Exception as e:
        print(str(e))
        return False
    return True

def redis_pop_list(r:redis.Redis,key:str,value:str)->bool:
    try:
        r.lrem(key,0,value=value)
    except Exception as e:
        print(str(e))
        return False
    return True


def redis_store_json(r:redis.Redis,key:str,value:dict|str|list)->bool:
    store_value = None
    if isinstance(value,dict) or isinstance(value,list):
        store_value = json.dumps(value)
    elif isinstance(value,str):
        try:
            json.loads(value)
        except Exception:
            raise ValueError("Not a valid json")
        store_value = value
    try:
        r.set(key,store_value)
    except Exception as e:
        print("REDIS_ERROR : ",str(e))
        return False
    return True


def redis_get_json(r:redis.Redis,key:str)->dict:
    data = r.get(key)
    if data == None:
        return {}
    return json.loads(data)

def redis_get_key(r:redis.Redis,key_pattern:str)->list:
    keys = r.keys(pattern=key_pattern)
    keys_str = [i.decode('utf-8') for i in keys]
    return keys_str

