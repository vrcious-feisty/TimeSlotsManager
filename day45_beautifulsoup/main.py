from bs4 import BeautifulSoup
import requests

response= requests.get(url="https://news.ycombinator.com/")
response_html = response.text
soup = BeautifulSoup(response_html,"html.parser")
span = soup.find_all(name="span", class_="titleline")
titles = [uni.contents[0].getText() for uni in span]
links = [uni.contents[0].get("href") for uni in span]

span_score = soup.find_all(name="span", class_= "score")

scores = [uni.contents[0].getText() for uni in span_score]
scores = [int(uni.split(" ")[0]) for uni in scores]

scores_reverse = sorted(scores,reverse=True)
n = -1
index=[]
def sort():
    global n
    if scores.count(score) == 1 :
       return scores.index(score)
    else:
        n += 1

##############################conditional list comprehension and outside lead to different results#########################
        indices = [i for i,x in enumerate(scores) if x == score]
        return indices[n]
    # print(indices)

# print(f"indices:{indices}")



for score in scores_reverse:
    index.append(sort())

print(titles)
print(links)
print(f"score:{scores}")
print(f"reverse scores :{sorted(scores,reverse=True)}")
print(f"original indices:{index}")

for unit in index:
    print(links[unit])




# print(tag)


#
# print(soup)



















# with open("website.html") as file:
#     contents = file.read()
#     # print(contents)
#
# soup = BeautifulSoup(contents,"html.parser")
#
# all_tags = soup.find_all("a")
#
# print(all_tags)
# for tag in all_tags:
#     print(tag.get("href"))
#
#
# # print(soup.prettify())
# # print(soup.body.p)