import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, key):
        self.redis.delete(key)

    def keys(self, pattern='*'):
        return self.redis.keys(pattern)

# 示例用法
if __name__ == "__main__":
    # 创建 RedisClient 实例
    client = RedisClient()

    # 设置键值对
    client.set('name', 'John')

    # 获取键对应的值
    name = client.get('name')
    print(name)  # 输出: b'John'

    # 删除键
   # client.delete('name')

    # 查找所有键
    keys = client.keys()
    print(keys)  # 输出: []

