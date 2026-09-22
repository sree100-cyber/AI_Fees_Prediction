from config import client

models = client.models.list()
for m in models.data:
    print(m.id)
    