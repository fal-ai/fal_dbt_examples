"""Send event with model information to Datadog."""
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import events_api
from datadog_api_client.v1.models import EventCreateRequest
import os
import time
import io

current_time = time.time()

configuration = Configuration()
configuration.api_key['apiKeyAuth'] = os.getenv("DD_API_KEY")
configuration.api_key['appKeyAuth'] = os.getenv("DD_APP_KEY")

df = ref(context.current_model.name)

buf = io.StringIO()
df.info(buf=buf)

text = buf.getvalue()
tags = ["fal"]

event_body = EventCreateRequest(
    tags=tags,
    aggregation_key="fal",
    title="fal - event",
    text=text,
    date_happened=int(current_time)
)


with ApiClient(configuration) as api_client:
    # Create an instance of the API class
    events_api_instance = events_api.EventsApi(api_client)
    try:
        events_api_instance.create_event(event_body)
    except ApiException as e:
        assert e.response["error"]
