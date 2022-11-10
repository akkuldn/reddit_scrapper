import json
import csv
import os
import pandas as pd



def parse_json():
    f = open("./posts.json", "r")
    print("I am here \n\n\n\n\n")
    my_json = f.read()
    f.close()
    aList = json.loads(my_json)
    new_list = []
    new_list.append(aList[0])
    print("Im here \n\n\n\n\n\n\n")
    print(new_list)
    field_names = ['title', 'user', 'upvotes', 'content_link','time','awards']
    


    with open('reddit_top_posts.csv', 'a') as csvfile:
        rowcount  = 0
        for row in open('reddit_top_posts.csv'):
            rowcount+= 1
        writer = csv.DictWriter(csvfile, fieldnames = field_names, lineterminator='\n')
        if rowcount < 1:
            print("Header not found ")
            writer.writeheader()
        writer.writerows(new_list)
    if os.path.exists("./posts.json"):
      os.remove("./posts.json")
    else:
      print("The file does not exist")


if __name__=="__main__":
    parse_json()