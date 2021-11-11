from transformers import pipeline


ticket_descriptions = list(ref("stg_zendesk_ticket_data").description)
classifier = pipeline("sentiment-analysis")
print(classifier(ticket_descriptions))
## todo write the analysis back to a table..
