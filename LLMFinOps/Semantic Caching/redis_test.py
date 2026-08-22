import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

print(r.ping())

# Store
r.set("user:1", "Yatharth")

# Retrieve
value = r.get("user:1")
print(value)

# Value expiration
r.set("user:1", "Yatharth", ex=30)
print(r.ttl("user:1"))

# see expiration of user:1
# python -c "import redis; r=redis.Redis(host='localhost', port=6379, decode_responses=True); print(r.ttl('user:1'))"

# hashes
r.hset(
    "user:2",
    mapping={
        "name": "Yatharth",
        "age": "23",
        "city": "Pune"
    }
)

print(r.hget("user:2", "name"))
print(r.hgetall("user:2"))

# Reids List
r.rpush("tasks", "learn Redis")
r.rpush("tasks", "learn Docker")
r.rpush("tasks", "learn Kubernetes")
print(r.lrange("tasks", 0, -1))

## add left
r.lpush("tasks", "learn Python")
print(r.lrange("tasks", 0, -1))

## LPUSH → beginning
## RPUSH → end

## remove item from list
## remove from beginning
task = r.lpop("tasks")
print(task)

## remove from end
task = r.rpop("tasks")
print(task)

## len of list
print(r.llen("tasks"))

## index access
print(r.lindex("tasks", 0))

## delete list 
r.delete("tasks")

# SETS in redis
r.sadd("skills", "Python")
r.sadd("skills", "Redis")
r.sadd("skills", "Docker")
print(r.smembers("skills"))

r.sadd("skills", "Python")
r.sadd("skills", "Python")

print(r.scard("skills"))

## check if exists in set or not
print(r.sismember("skills", "Python"))
print(r.sismember("skills", "Java"))
print(r.smembers("skills"))

## common between sets
r.sadd("backend", "Python", "Redis", "Docker")
r.sadd("data", "Python", "Pandas", "Redis")
print(f"Common skills: {r.sinter('backend', 'data')}")

## Union of sets
print(f"Union of skills: {r.sunion('backend', 'data')}")

## Difference of sets
print(f"Difference of skills: {r.sdiff('backend', 'data')}")

# Redis Sorted Sets (ZSETs): Sorted by values 
r.zadd(
    "leaderboard",
    {
        "Alice": 1500,
        "Bob": 1800,
        "Charlie": 1200
    }
)
print(r.zrange("leaderboard", 0, -1))
print("Get scores:")
print(
    r.zrange(
        "leaderboard",
        0,
        -1,
        withscores=True
    )
)
print("Get scores in reverse order:")
print(
    r.zrevrange(
        "leaderboard",
        0,
        -1,
        withscores=True
    )
)
print("Get one member's score:")
print(r.zscore("leaderboard", "Alice"))

## Update a score
r.zincrby("leaderboard", 200, "Alice")
print(r.zscore("leaderboard", "Alice"))


# Redis Pub/Sub



# clear Redis database
r.flushdb()
print("Redis database cleared")