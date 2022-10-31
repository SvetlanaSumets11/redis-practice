"""
Hashes
HDEL, HEXISTS, HGET, HGETALL, HINCRBY,
HINCRBYFLOAT, HKEYS, HLEN, HMGET, HMSET,
HSCAN, HSET, HSETNX, HSTRLEN, HVALS

 - The HSET command adds a key-value pair to a hash. If the hash does not exist one will be created.
If a key already exists, the value for the key is set to the specified value. Time complexity: O(1) for each field/value
pair added, so O(N) to add N field/value pairs when the command is called with multiple field/value pairs.
 - The HGET command retrieves the value for a specific key in a hash. Time complexity: O(1)
 - The HGETALL retrieves all the keys and their values present in a hash. The redis-py returns the keys and values as
 a Python dictionary. Time complexity: O(N) where N is the size of the hash.
 - The HKEYS retrieves all the keys present in a hash. The redis-py returns the keys as a Python list. Time complexity:
O(N) where N is the size of the hash.
 - The HVALS retrieves all the keys present in a hash. The redis-py returns the values as a Python list.
Time complexity: O(N) where N is the size of the hash.
 - The HEXISTS command checks and return an integer whether a specified key exists on a Redis hash. In case of
redis-py it returns a Boolean value – TRUE or FALSE. Time complexity: O(1)
 - The HLEN command returns the number of fields defined for a key in a specific Redis hash. Time complexity: O(1)
 - The HDEL removes a key-value pair identified by a specific key. Time complexity:
 - The HINCRBY is about increments the number stored at field in the hash stored at key by increment.
Time complexity: O(1)
 - The HINCRBYFLOAT is increment the specified field of a hash stored at key, and representing a floating point number,
by the specified increment. Time complexity: O(1)
 - The HMGET returns the values associated with the specified fields in the hash stored at key.
Time complexity: O(N) where N is the number of fields being requested.
 - The HMSET sets the specified fields to their respective values in the hash stored at key.
Time complexity: O(N) where N is the number of fields being set.
 - The HSETNX sets field in the hash stored at key to value, only if field does not yet exist. Time complexity: O(1)
 - The HSTRLEN returns the string length of the value associated with field in the hash stored at key. If the key or
the field do not exist, 0 is returned. Time complexity: O(1)
"""
from client import redis


def redis_hash_example(test_hash: str):
    redis.hset(test_hash, 'first', 1)
    redis.hset(test_hash, 'second', 2)
    assert redis.hkeys(test_hash) == [b'first', b'second']
    assert redis.hvals(test_hash) == [b'1', b'2']
    assert redis.hgetall(test_hash) == {b'first': b'1', b'second': b'2'}
    assert redis.hget(test_hash, 'second') == b'2'
    assert redis.hlen(test_hash) == 2

    redis.hdel(test_hash, 'first')
    assert redis.hgetall(test_hash) == {b'second': b'2'}

    assert redis.hexists(test_hash, 'first') is False
    assert redis.hexists(test_hash, 'second') is True

    redis.hincrby(test_hash, 'third', 3)
    assert redis.hgetall(test_hash) == {b'second': b'2', b'third': b'3'}

    assert redis.hincrbyfloat(test_hash, 'second', 4.5) == 6.5
    assert redis.hgetall(test_hash) == {b'second': b'6.5', b'third': b'3'}

    assert redis.hmget(test_hash, 'second') == [b'6.5']

    redis.hsetnx(test_hash, 'seventh', 7)
    assert redis.hgetall(test_hash) == {b'second': b'6.5', b'third': b'3', b'seventh': b'7'}

    redis.hset(test_hash, 8, 'eighth')
    assert redis.hstrlen(test_hash, 8) == 6


redis_hash_example('test_hash')
