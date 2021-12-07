"""Send model data to Firestore."""

df = ref(context.current_model.name)

write_to_firestore(df=df,
                   collection="zendesk_sentiment_data",
                   key_column="id")

print("Success!")
