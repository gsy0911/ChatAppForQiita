mkdir ~/.aws
echo [default] >> ~/.aws/config
echo region = $region >> ~/.aws/config
echo [default] >> ~/.aws/credentials
echo aws_access_key_id = $aws_access_key_id >> ~/.aws/credentials
echo aws_secret_access_key = $aws_secret_access_key >> ~/.aws/credentials