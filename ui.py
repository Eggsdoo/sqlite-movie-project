import db
from objects import Movie

def display_welcome():
    print("The Movie List program")
    print()    
    display_menu()

def display_menu():
    print("COMMAND MENU")
    print("cat  - View movies by category")
    print("year - View movies by year")
    print("sort - Sort Movies") # new feature
    print("fil - Filter Movies") # new feature
    print("add  - Add a movie")
    print("del  - Delete a movie")
    print("exit - Exit program")
    print()    

def display_categories():
    print("CATEGORIES")
    categories = db.get_categories()    
    for category in categories:
        print(f"{category.id}. {category.name}")
    print()
    
def display_movies(movies, title_term): # sort_by=None do not need this anymore
    print(f"MOVIES - {title_term}")
    
    print(f"{'ID':4}{'Name':38}{'Year':6}" 
          f"{'Mins':6}{'Category':10}")
    print("-" * 63)
    for movie in movies:
        print(f"{movie.id:<4d}{movie.name:38}{movie.year:<6d}"
              f"{movie.minutes:<6d}{movie.category.name:10}")                               
    print()  

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid whole number. Please try again.\n")

def display_movies_by_category():
    category_id = get_int("Category ID: ")
    category = db.get_category(category_id)
        
    if category == None:
        print("There is no category with that ID.\n")
    else:
        print()
        movies = db.get_movies_by_category(category_id)
        display_movies(movies, category.name.upper())

def display_movies_by_year():
    year = get_int("Year: ")
    print()
    movies = db.get_movies_by_year(year)
    display_movies(movies, year)

def sort_movies():
    sorting_option = input("Sort by (name/year/category): ").lower()
    movies = db.get_movies()

    if sorting_option == "name":
        sorted_movies = sorted(movies, key=lambda x: x.name)
    elif sorting_option == "year":
        sorted_movies = sorted(movies, key=lambda x: x.year)
    elif sorting_option == "category":
        sorted_movies = sorted(movies, key=lambda x: x.category.name)
    else:
        print("Invalid sorting option. Please try again.")
        return 
    display_movies(sorted_movies, "All Movies") # sorting_option <- do not need this anymore

def filter_movies():
    year = get_int("Filter by Year (enter 0 to skip): ")
    category_id = get_int("Filter by Category (enter 0 to skip): ")

    movies = db.get_movies()
    filtered_movies = movies

    if year > 0:
        filtered_movies = [movie for movie in filtered_movies if movie.year == year]

    if category_id > 0:
        filtered_movies = [movie for movie in filtered_movies if movie.category.id == category_id]

    if year > 0 or category_id > 0:
        display_movies(filtered_movies, "Filtered Movies")

def add_movie():
    name        = input("Name: ")
    year        = get_int("Year: ")
    minutes     = get_int("Minutes: ")
    category_id = get_int("Category ID: ")

    category = db.get_category(category_id)
    if category == None:
        print("There is no category with that ID. Movie NOT added.\n")
    else:
        movie = Movie(name=name, year=year, minutes=minutes,
                      category=category)
        db.add_movie(movie)
        print(f"{name} was added to database.\n")
    
def delete_movie():
    movie_id = get_int("Movie ID: ")
    db.delete_movie(movie_id)
    print(f"Movie ID {movie_id} was deleted from database.\n")
        
def main():
    db.connect()
    display_welcome()
    display_categories()
    
    while True:        
        command = input("Command: ").lower()
        if command == "cat":
            display_movies_by_category()
        elif command == "year":
            display_movies_by_year()
        elif command == "sort":
            sorted_movies = sort_movies()
            if sorted_movies:
                display_movies(sorted_movies, "All Movies")
        elif command == "fil":
            filter_movies()
        elif command == "add":
            add_movie()
        elif command == "del":
            delete_movie()
        elif command == "exit":
            break
        else:
            print("Not a valid command. Please try again.\n")
            display_menu()
            
    db.close()
    print("Thanks Bye!")

if __name__ == "__main__":
    main()
