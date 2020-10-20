from TwitterAPI import TwitterAPI
import requests
import random
import os

# Set vars
twitter_api = TwitterAPI(api_key, api_secret, access_token_key, access_token_secret)
nps_url = 'https://developer.nps.gov/api/v1/parks?api_key=[YOUR_API_KEY]&limit=500'
park_stats = {}

def download():
  # Get random park dict:
  nps_request = requests.get(nps_url)
  park_list = nps_request.json()["data"]
  park_obj = park_list[random.randint(0, len(park_list) - 1)]

  # Get `fullName` and NPS website
  park_stats["full_name"] = park_obj["fullName"] 
  park_stats["website"] = park_obj["url"]

  # Get random image from `images` list within park dict:
  if park_obj["images"]:
    image_list = park_obj["images"]
    image = image_list[random.randint(0, len(image_list) - 1)]["url"]
  else:
    download()

  # Download image
  image_response = requests.get(image)
  if image_response.status_code == 200:
    with open("IMAGE_PATH", 'wb') as f:
      f.write(image_response.content)
      f.close()
      upload()
  else:
    download()

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
    request = twitter_api.request('statuses/update', { 'status': park_stats["full_name"] + " | " + park_stats["website"], 'media_ids': media_id })
    print("Success" if request.status_code == 200 else "Failure: " + request.text)
  # Cleanup
  if os.path.exists("IMAGE_PATH"):
    os.remove("IMAGE_PATH")
  else:
    print("The file does not exist")

download()
