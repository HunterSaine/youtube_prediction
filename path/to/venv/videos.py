from keys import api_key
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors

pd.options.mode.chained_assignment = None
apiServiceName = "youtube"
apiVersion = "v3"


def getyoutubevideos(api_key, max_results):
    youtube = googleapiclient.discovery.build(apiServiceName, apiVersion, developerKey=api_key)
    request = youtube.videos().list(part="snippet,contentDetails,statistics",
                                    chart="mostPopular",
                                    regionCode="US",
                                    maxResults=max_results)

    all_videos = []
    while request is not None:
        response = request.execute()
        all_videos.extend(response['items'])
        request = youtube.videos().list_next(request, response)
    return all_videos


videos = getyoutubevideos(api_key, 1000)
print(len(videos))

video_df = pd.json_normalize(videos)
video_df = video_df.fillna(0)
filtered_df = video_df[
    ['snippet.title', 'snippet.channelTitle', 'snippet.publishedAt', 'statistics.viewCount', 'statistics.likeCount',
     'statistics.commentCount']]
filtered_df.columns = ['Title', 'Channel', 'Published At', 'View Count', 'Like Count', 'Comment Count']
filtered_df['Published At'] = pd.to_datetime(filtered_df['Published At'])
filtered_df['Published At'] = filtered_df['Published At'].dt.date
filtered_df['View Count'] = filtered_df['View Count'].astype(int)
filtered_df['Like Count'] = filtered_df['Like Count'].astype(int)
filtered_df['Comment Count'] = filtered_df['Comment Count'].astype(int)
filtered_df['Like Ratio'] = filtered_df['Like Count'] / filtered_df['View Count']
filtered_df['Comment Ratio'] = filtered_df['Comment Count'] / filtered_df['View Count']
filtered_df.to_csv('video_data.csv', index=True)
