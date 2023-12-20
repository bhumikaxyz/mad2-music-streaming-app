import redis

r = redis.Redis(
  host='redis-10155.c305.ap-south-1-1.ec2.cloud.redislabs.com',
  port=10155,
  password='X8kWly7NmJxeETDtmtsG8YZee2Bb3X1j')

# to set a key value pair for redis

print(r.set('name','vishal'))

# to get a value from redis

print(r.get('name'))

# to delete a value from redis

print(r.delete('name'))

# to get all the keys from redis

print(r.keys())

# to get all the values from redis

# print(r.values())

# to get all the key value pairs from redis




