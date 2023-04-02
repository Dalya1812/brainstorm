from muselsl import stream, list_muses
print(list_muses())
muse_one = list_muses()[0]
stream_data = stream(muse_one['address'])
print(stream_data)

