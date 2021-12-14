from transformers import pipeline
import pandas as pd
import numpy as np

ticket_data = ref("stg_zendesk_ticket_data")
ticket_descriptions = list(ticket_data.description)
classifier = pipeline("sentiment-analysis")
description_sentimet_analysis = classifier(ticket_descriptions)

rows = []
for id, sentiment in zip(ticket_data.id, description_sentimet_analysis):
    rows.append((int(id), sentiment["label"], sentiment["score"]))

records = np.array(rows, dtype=[("id", int), ("label", "U8"), ("score", float)])

sentiment_df = pd.DataFrame.from_records(records)

print("Uploading\n", sentiment_df)
write_to_source(sentiment_df, "results", "ticket_data_sentiment_analysis")
