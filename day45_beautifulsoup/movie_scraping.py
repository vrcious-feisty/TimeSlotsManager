from bs4 import BeautifulSoup

with open("empire_movies.html", encoding="utf-8") as data_raw:
    data =  data_raw.read()

soup = BeautifulSoup(data,"html.parser")
list_raw = soup.find_all(name="h3", class_="title")
movies = [movie.getText() for movie in list_raw]
movies= [movie for movie in movies[::-1]]

with open("100_best_movies_to_watch.txt", mode = "w") as data:
    for movie in movies:
        data.write(f"{movie}\n")




print(movies)
print(len(movies))
