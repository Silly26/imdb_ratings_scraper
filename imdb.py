import requests
from bs4 import BeautifulSoup

def scrape_imdb_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    movie_items = soup.find_all('div', class_='lister-item-content')
    movies = []
    
    for item in movie_items:
        name = item.find('h3', class_='lister-item-header').find('a').text.strip()
        rating_element = item.find('div', class_='inline-block ratings-imdb-rating')
        rating = rating_element['data-value'] if rating_element else 'N/A'
        movies.append((name, rating))
    
    return movies

def sort_movies_by_rating(movie):
    rating = movie[1]
    return float(rating) if rating != 'N/A' else 0

def main():
    base_url = 'https://www.imdb.com/search/title/?title_type=feature&genres=western&explore=genres&start='
    start_page = 1
    end_page = 3  # Change this value if you want to loop through more pages.
    
    all_movies = []
    for page in range(start_page, end_page + 1):
        url = f"{base_url}{(page - 1) * 50 + 1}"
        print(f"Scraping page {page}...")
        movies = scrape_imdb_page(url)
        all_movies.extend(movies)
    
    # Sort the movies based on rating (highest to lowest)
    sorted_movies = sorted(all_movies, key=sort_movies_by_rating, reverse=True)

    # Save the sorted results to a text file
    try:
        with open('imdb_movies.txt', 'w', encoding='utf-8') as file:
            for name, rating in sorted_movies:
                file.write(f"{name}: {rating}\n")
        print("Data saved to imdb_movies.txt")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

if __name__ == "__main__":
    main()
