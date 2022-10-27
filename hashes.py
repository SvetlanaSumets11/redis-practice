"""
Hashes
HDEL, HEXISTS, HGET, HGETALL, HINCRBY,
HINCRBYFLOAT, HKEYS, HLEN, HMGET, HMSET,
HSCAN, HSET, HSETNX, HSTRLEN, HVALS

 - The HSET command adds a key-value pair to a hash. If the hash does not exist one will be created.
If a key already exists, the value for the key is set to the specified value.
 - The HGET command retrieves the value for a specific key in a hash.
 - The Redis command HGETALL retrieves all the keys and their values present in a hash. The redis-py returns
the keys and values as a Python dictionary.
 - The HKEYS retrieves all the keys present in a hash. The redis-py returns the keys as a Python list.
 - The HVALS retrieves all the keys present in a hash. The redis-py returns the values as a
Python list.
 - The HEXISTS command checks and return an integer whether a specified key exists on a Redis hash. In case of
redis-py it returns a Boolean value – TRUE or FALSE.
 - The HLEN command returns the number of fields defined for a key in a specific Redis hash.
 - The HDEL removes a key-value pair identified by a specific key.
 - The HINCRBY is about increments the number stored at field in the hash stored at key by increment.
 - The HINCRBYFLOAT is increment the specified field of a hash stored at key, and representing a floating point number,
by the specified increment.
 - The HMGET returns the values associated with the specified fields in the hash stored at key.
 - The HMSET sets the specified fields to their respective values in the hash stored at key.
 - The HSETNX sets field in the hash stored at key to value, only if field does not yet exist.
 - The HSTRLEN returns the string length of the value associated with field in the hash stored at key. If the key or
the field do not exist, 0 is returned.
"""
from client import redis


def redis_hash_example(array):
    redis.hset(array, 'first', 1)
    redis.hset(array, 'second', 2)
    assert redis.hkeys(array) == [b'first', b'second']
    assert redis.hvals(array) == [b'1', b'2']
    assert redis.hgetall(array) == {b'first': b'1', b'second': b'2'}
    assert redis.hget(array, 'second') == b'2'
    assert redis.hlen(array) == 2

    redis.hdel(array, 'first')
    assert redis.hgetall(array) == {b'second': b'2'}

    assert redis.hexists(array, 'first') is False
    assert redis.hexists(array, 'second') is True

    redis.hincrby(array, 'third', 3)
    assert redis.hgetall(array) == {b'second': b'2', b'third': b'3'}

    assert redis.hincrbyfloat(array, 'second', 4.5) == 6.5
    assert redis.hgetall(array) == {b'second': b'6.5', b'third': b'3'}

    assert redis.hmget(array, 'second') == [b'6.5']

    redis.hsetnx(array, 'seventh', 7)
    assert redis.hgetall(array) == {b'second': b'6.5', b'third': b'3', b'seventh': b'7'}

    redis.hset(array, 8, 'eighth')
    assert redis.hstrlen(array, 8) == 6


redis_hash_example('test_hash')
