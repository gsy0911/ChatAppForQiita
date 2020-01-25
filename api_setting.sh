slack_token=$slack_token
oauth_access_token=$slack_oauth_access_token
channel_id=$slack_2ch_channel_id
printf '{
  "version": "2.0",
  "app_name": "ChatAppPrivate",
  "stages": {
    "dev": {
      "api_gateway_stage": "api",
      "environment_variables": {
        "SLACK_TOKEN": "%s",
        "OAUTH_ACCESS_TOKEN": "%s",
        "CHANNEL_ID": "%s",
        "TZ": "Asia/Tokyo"
      }
    }
  }
}' $slack_token $oauth_access_token $channel_id > src/lambda/ChatAppForQiita/.chalice/config.json