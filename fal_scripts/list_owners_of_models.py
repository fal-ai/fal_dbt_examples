models = list_models()

for model in models:
    if model.meta:
        print(model.meta["owner"])
