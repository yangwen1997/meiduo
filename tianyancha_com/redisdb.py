import redis


# Jon!Q@W#E
class redisdb(object):

    def __init__(self,host='localhost', port=6379, db=1, password = None):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
        self.Redis = redis.Redis(connection_pool=self.pool)

    # push a new link at the end of list
    def pushLink(self, rlist, value):
        return self.Redis.lpush(rlist, value)

    # return the last link
    def lpopLink(self, rlist):
        return self.Redis.lpop(rlist)

    # return the first link
    def rpopLink(self, rlist, value):
        return self.Redis.rpop(rlist)

    def brpoplpush(self, src, dst, timeout=10):
        return self.Redis.brpoplpush(src, dst, timeout=10)

    def lrem(self, list_name, key, num=0):
        return self.Redis.lrem(list_name, key, num)

    def lrange(self, list_name, sta, sto):
        return self.Redis.lrange(list_name, sta, sto)

    # get length of list
    def lenList(self, rlist):
        return self.Redis.llen(rlist)

    # init list
    def delList(self, rlist):
        return self.Redis.delete(rlist)

    # get
    def rget(self, key):
        return self.Redis.get(key)

    # delete key
    def delete(self, key):
        return self.Redis.delete(key)

    # all keys
    def rkeys(self):
        return self.Redis.keys()

    # set
    def rset(self, key, value):
        return self.Redis.set(key, value)

    def flushdb(self):
        return self.Redis.flushdb()

    # check key
    def exists(self, name):
        return self.Redis.exists(name)

    # set add new values
    def rsadd(self, name, values):
        return self.Redis.sadd(name, values)

    # set sismember
    def sismember(self, name, value):
        return self.Redis.sismember(name, value)

    # Push ``values`` onto the tail of the list ``name``
    def rpush(self, name, *values):
        return self.Redis.rpush(name, *values)

    # rpop remove last value
    def rpop(self, name):
        return self.Redis.rpop(name)

    # rpop remove last value
    def rblpop(self, name):
        return self.Redis.blpop(name, timeout=20)

    # rspop remove random value
    def rspop(self, name):
        return self.Redis.spop(name)

    # rscard get length of set
    def rscard(self, name):
        return self.Redis.scard(name)

    # Set key to value within hash ``name`` for each corresponding key and value from the ``mapping`` dict.
    def rhmset(self, name, mapping):
        return  self.Redis.hmset(name, mapping)

    # Set ``key`` to ``value`` within hash ``name``
    def rhset(self, name, key ,value):
        return  self.Redis.hset( name, key ,value)

    # "Return the value of ``key`` within the hash ``name``"
    def rhget(self, name, key):
        return  self.Redis.hget(name, key)

    # "Return a Python dict of the hash's name/value pairs"
    def rhgetall(self, name):
        return self.Redis.hgetall(name)

    # "Return the list of keys within hash ``name``"
    def rhkeys(self, name):
        return self.Redis.hkeys(name)

    #"Returns a boolean indicating if ``key`` exists within hash ``name``"
    def rhexists(self,name, key):
        return self.Redis.hexists(name, key)

    #"Delete ``keys`` from hash ``name``"
    def rhdel(self, name, key):
        return self.Redis.hdel(name, key)

