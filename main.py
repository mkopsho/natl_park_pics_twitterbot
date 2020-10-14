from TwitterAPI import TwitterAPI
import requests
import random
import os

# Set API vars
twitter_api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
nps_url = 'https://developer.nps.gov/api/v1/parks?api_key=[YOUR_API_KEY]&limit=500'

# Get random park dict:
nps_request = requests.get(nps_url)
park_list = nps_request.json()["data"]
park_obj = park_list[random.randint(0, len(park_list) - 1)]

# Get `fullName` and NPS website
full_name = park_obj["fullName"] 
website = park_obj["url"]

# Get random image from `images` list within park dict:
image_list = park_obj["images"]
image = park_obj["images"][random.randint(0, len(image_list) - 1)]["url"]

# Download image
image_response = requests.get(image)

def download():
  if image_response.status_code == 200:
      with open("IMAGE_PATH", 'wb') as f:
        f.write(image_response.content)
        f.close()
        upload()

# Tweet it
## Upload image
def upload():
  image_path = "IMAGE_PATH"
  if os.path.getsize(image_path) <= 5242880:
    file = open(image_path, 'rb')
    data = file.read()
    request = twitter_api.request('media/upload', None, { 'media': data })
    print("Success" if request.status_code == 200 else "Failure: " + request.text)
    reference(request)
  elif os.path.getsize(image_path) > 5242880:
    download()

## Reference uploaded image
def reference(request):
  if request.status_code == 200:
    media_id = request.json()['media_id']
    request = twitter_api.request('statuses/update', { 'status': full_name + " | " + website, 'media_ids': media_id })
    print("Success" if request.status_code == 200 else "Failure: " + request.text)

download()

