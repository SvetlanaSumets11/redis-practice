"""
Lists
BLPOP, BRPOP, BRPOPLPUSH, LINDEX, LINSERT,
LLEN, LPOP, LPUSH, LPUSHX, LRANGE, LREM,
LSET, LTRIM, RPOP, RPOPLPUSH, RPUSH, RPUSHX

 - The LPUSH command adds a value to the head of a Redis list. Time complexity: O(1).
 - The RPUSH command adds a value to the tail of a Redis list. Time complexity: O(1).
 - The LLEN command counts the length of a Redis list. Time complexity: O(1).
 - Tre LRANGE returns the specified elements of the Redis list stored at key. Time complexity: O(S + N) where S is
the distance of start offset from HEAD for small lists, from the nearest end (HEAD or TAIL) for large lists;
and N is the number of elements in the specified range.
 - The LREM command remove {num} instance from the Redis list where the value equals {value}.
Time complexity: O(N + M) where N is the length of the list and M is the number of elements removed.
 - The LPOP pop first element of the Redis list and move it to the back. Time complexity: O(N) where N is the number
of elements returned.
 - The RPOP pop last element of the Redis list and move it to the back. Time complexity: O(N) where N is the number
of elements returned.
 - The LINSERT command adds a value before or after the first occurrence of a specific value.
Time complexity: O(N) except for the head element and the tail element.
 - Tre BLPOP is a blocking list pop primitive. It is the blocking version of LPOP because it blocks the connection
when there are no elements to pop from any of the given lists. An element is popped from the head of the first
list that is non-empty, with the given keys being checked in the order that they are given.
Time complexity: O(N) where N is the number of elements returned.
 - The BRPOP is a blocking list pop primitive. It is the blocking version of RPOP because it blocks the connection
when there are no elements to pop from any of the given lists. An element is popped from the tail of the first list
that is non-empty, with the given keys being checked in the order that they are given.
Time complexity: O(N) where N is the number of elements returned.
 - The LSET command sets a value for the element specified by the index. The time complexity is O(N) except for
the head element and the tail element.
 - The RPOPLPUSH returns and removes the last element (tail) of the list stored at source, and pushes the element at
the first element (head) of the list stored at destination. Time complexity: O(1).
 - The BRPOPLPUSH is the blocking variant of RPOPLPUSH. Time complexity: O(1).
 - The RPUSHX inserts specified values at the tail of the list stored at key, if key already exists and holds a list.
Time complexity: O(1) for each element added, so O(N) to add N elements when the command is called with multiple
arguments.
 - The LPUSHX inserts specified values at the head of the list stored at key, if key already exists and holds a list.
Time complexity: O(1) for each element added, so O(N) to add N elements when the command is called with multiple
arguments.
 - The LINDEX returns the element at index index in the list stored at list. Time complexity: O(N) where N is
the number of elements to traverse to get to the element at index. This makes asking for the first or the last
element of the list O(1).
 - The LTRIM trims an existing list so that it will contain only the specified range of elements specified.
Time complexity: O(N) where N is the number of elements to be removed by the operation.
"""
from client import redis


def redis_list_example(test_list: str):
    for i in range(5):
        redis.lpush(test_list, i)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'4', b'3', b'2', b'1', b'0']

    for i in range(4):
        redis.rpush(test_list, i)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'4', b'3', b'2', b'1', b'0', b'0', b'1', b'2', b'3']

    array_len = redis.llen(test_list)
    assert array_len == 9

    redis.lrem(test_list, 2, 3)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'4', b'2', b'1', b'0', b'0', b'1', b'2']

    for i in range(2):
        redis.lpop(test_list)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'1', b'0', b'0', b'1', b'2']

    for i in range(2):
        redis.rpop(test_list)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'1', b'0', b'0']

    redis.linsert(test_list, 'after', 1, 78)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'1', b'78', b'0', b'0']

    redis.linsert(test_list, 'before', 1, 66)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'66', b'1', b'78', b'0', b'0']

    data = redis.blpop(test_list)[1]
    assert data == b'66'
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'1', b'78', b'0', b'0']

    data = redis.brpop(test_list)[1]
    assert data == b'0'
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'1', b'78', b'0']

    redis.lset(test_list, 2, 4)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'1', b'78', b'4']

    additional_array = 'example'
    redis.rpoplpush(test_list, additional_array)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'1', b'78']
    assert redis.lrange(additional_array, 0, redis.llen(test_list) - 1) == [b'4']

    redis.brpoplpush(test_list, additional_array)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'1']
    assert redis.lrange(additional_array, 0, redis.llen(test_list) - 1) == [b'78']

    num = redis.lpushx(test_list, 4)
    assert num == 2
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'4', b'1']

    num = redis.rpushx(test_list, 5)
    assert num == 3
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'4', b'1', b'5']

    element = redis.lindex(test_list, 2)
    assert element == b'5'

    redis.ltrim(test_list, 0, 1)
    assert redis.lrange(test_list, 0, redis.llen(test_list) - 1) == [b'4', b'1']


redis_list_example('test_list')
