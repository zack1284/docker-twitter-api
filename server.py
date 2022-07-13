import requests
import os
import json
from datetime import datetime
import argparse
import ast
import re

# To set your environment variables in your terminal run the following line:
bearer_token = os.environ.get("BEARER_TOKEN")

import sys
import spacy

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

def clean_text(text):
   if type(text) != str:
       text = text.decode("utf-8")
   doc = re.sub(regex, '', text, flags=re.MULTILINE) # remove URLs
   sentences = []
   for sentence in doc.split("\n"):
       if len(sentence) == 0:
           continue
       sentences.append(sentence)
   doc = nlp("\n".join(sentences))
   doc = " ".join([token.lemma_.lower().strip() for token in doc
                       if (not token.is_stop)
                           and (not token.like_url)
                           and (not token.lemma_ == "-PRON-")
                           and (not len(token) < 4)])
   doc = ''.join([i for i in doc if not i.isdigit()])
   doc = remove_prefix(doc,'@') 
   doc = remove_symbol(doc,['@','.','[',']','{','}','(',')','!','#','$','%','^','*','+','/','|','-','<','>','?','_','~','`',':','"',';']) #remove all symbols in list

   return doc

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever
def remove_symbol(doc,list_s):
    for i in range(len(list_s)):
        filter(lambda x:x[0]!=list_s[i], doc.split())
        doc = " ".join(filter(lambda x:x[0]!=list_s[i],doc.split()))
    
    return doc
	
def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
        
    for response_line in response.iter_lines():
     try:
        if response_line:
            json_response = json.loads(response_line)
            json_data = json_response["data"]
         
            if json_data["lang"] == "en":
             created_at = json_data["created_at"]
             text = clean_text(json_data["text"])
             date_object = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
             date = date_object.strftime("%Y-%m-%d-%H-%M-%S")
             output = str(date) + " " + text
             fileObject = open("tweets.txt", "a")
             fileObject.write(output + "\n")
             fileObject.close()
             #print(output)
        print("Writing tweets to tweets.txt... Press ctrl+C to end...")
     except ValueError:
         print("error! Might need to export your bearer token!")



def read_file(file):
   json_data = file["data"]
   if json_data["lang"] == "en":
     created_at = json_data["created_at"]
     text = clean_text(json_data["text"])
     date_object = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
     date = date_object.strftime("%Y-%m-%d-%H-%M-%S")
     output = str(date) + " " + text
     fileObject = open("tweets.txt", "a")
     fileObject.write(output + "\n")
     fileObject.close()
     
   return print("Successfully write into tweets.txt")
   

def main():
   url = create_url()
   timeout = 0
   
   parser = argparse.ArgumentParser(description='filename')
   parser.add_argument('--filename', type=str, default='nofile',help='Enter a FIle name or read from twitter API')
   args = parser.parse_args() #print(args.filename)
   
   while args.filename == 'nofile':
    try:
      connect_to_endpoint(url)
      timeout += 1
    except KeyboardInterrupt:  
      sys.exit(0)
   else:
     with open(args.filename) as infile:
        read = infile.read()
        file = json.loads(read)
        read_file(file)
     
if __name__ == "__main__":
  main()
    
    
    
