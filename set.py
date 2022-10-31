"""
Sets
SADD, SCARD, SDIFF, SDIFFSTORE, SINTER, SINTERSTORE,
SISMEMBER, SMEMBERS, SMOVE, SPOP, SRANDMEMBER, SREM,
SSCAN, SUNION, SUNIONSTORE

 - The SADD adds an element to a set. Time complexity: O(1) for each element added, so O(N) to add N elements
when the command is called with multiple arguments.
 - The SCARD returns the cardinality of the set. The cardinality of a set is the number of elements present in it.
Time complexity: O(1)
 - The SMEMBERS returns all the elements present in a set. Time complexity: O(N) where N is the set cardinality.
 - The SPOP removes an element from a Redis list and returns the value of the removed element. Time complexity:
Without the count argument O(1), otherwise O(N) where N is the value of the passed count.
 - The SREM removes an element with a specified value from the set. Time complexity: O(N) where N is the number
of members to be removed.
 - The SDIFF returns the members of the set resulting from the difference between the first set and all
the successive sets. Time complexity: O(N) where N is the total number of elements in all given sets.
 - The SDIFFSTORE is equal to SDIFF, but instead of returning the resulting set, it is stored in destination.
Time complexity: O(N) where N is the total number of elements in all given sets.
 - The SINTER returns the members of the set resulting from the intersection of all the given sets. Time complexity:
O(N*M) worst case where N is the cardinality of the smallest set and M is the number of sets.
 - The SINTERSTORE is equal to SINTER, but instead of returning the resulting set, it is stored in destination.
Time complexity: O(N*M) worst case where N is the cardinality of the smallest set and M is the number of sets.
 - The SISMEMBER returns if member is a member of the set stored at set. Time complexity: O(1)
 - The SMOVE move member from the set at source to the set at destination. Time complexity: O(1)
 - The SRANDMEMBER returns a random element from the set value stored at set, when called with just the key argument.
Time complexity: Without the count argument O(1), otherwise O(N) where N is the absolute value of the passed count.
 - The SUNION returns the members of the set resulting from the union of all the given sets. Time complexity:
O(N) where N is the total number of elements in all given sets.
 - The SUNIONSTORE is equal to SUNION, but instead of returning the resulting set, it is stored in destination.
Time complexity: O(N) where N is the total number of elements in all given sets.
"""
from client import redis


def redis_set_example(test_set: str):
    for i in range(5):
        redis.sadd(test_set, i)
    assert redis.smembers(test_set) == {b'0', b'1', b'2', b'3', b'4'}

    array_len = redis.scard(test_set)
    assert array_len == 5

    redis.srem(test_set, 2)
    assert redis.smembers(test_set) == {b'4', b'3', b'1', b'0'}

    for i in range(redis.scard(test_set)):
        redis.spop(test_set)
    assert redis.smembers(test_set) == set()

    additional_set = 'additional_set'
    for i in (4, 2, 5, 7):
        redis.sadd(additional_set, i)
    assert redis.smembers(additional_set) == {b'4', b'2', b'5', b'7'}

    for i in range(5):
        redis.sadd(test_set, i)

    difference = redis.sdiff(test_set, additional_set)
    assert difference == {b'1', b'0', b'3'}

    redis.sdiffstore(0, test_set, additional_set)
    assert redis.smembers(test_set) == {b'2', b'0', b'1', b'4', b'3'}

    intersection = redis.sinter(additional_set, test_set)
    assert intersection == {b'2', b'4'}

    redis.sinterstore('example', additional_set, test_set)
    assert redis.smembers('example') == {b'2', b'4'}

    assert redis.sismember(test_set, 2) is True
    assert redis.sismember(test_set, 78) is False

    redis.smove(test_set, additional_set, 0)
    assert redis.smembers(test_set) == {b'2', b'1', b'4', b'3'}
    assert redis.smembers(additional_set) == {b'0', b'4', b'2', b'5', b'7'}

    union = redis.sunion(test_set, additional_set)
    assert union == {b'2', b'1', b'4', b'3', b'0', b'5', b'7'}

    redis.sunionstore('temp', test_set, additional_set)
    assert redis.smembers('temp') == {b'2', b'1', b'4', b'3', b'0', b'5', b'7'}


redis_set_example('test_set')
