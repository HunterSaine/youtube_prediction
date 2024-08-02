import json
from keys import api_key
import pandas as pd
import numpy as np
import googleapiclient.discovery
import googleapiclient.errors

apiServiceName = "youtube"
apiVersion = "v3"
youtube = googleapiclient.discovery.build(apiServiceName, apiVersion, developerKey = api_key)
request = youtube.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode= "US")
response = request.execute()
print(json.dumps(response, indent=2))
