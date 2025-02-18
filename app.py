import feedparser, re, markdown

def get_movie_poster_and_review(summary):
    # Extract the image URL using regular expressions
    image_match = re.search(r'<img src="(.*?)"', summary)
    if image_match:
        image_url = image_match.group(1)
    else:
        image_url = None  # Handle the case where no image is found

    # Remove the image tag and surrounding <p> tags from the summary
    review = re.sub(r'<p><img src=".*?"></p>', '', summary).strip()
    # Clean up any remaining HTML tags (optional, if needed)
    review = re.sub(r'<.*?>', '', review).strip()  # Removes all HTML tags
    return image_url,review


#def build_markdown(filename, title, movie_data):
# Creates a Markdown file with a title, table of contents, and movie data.

# Args:
#     filename: The name of the Markdown file to create (e.g., "movies.md").
#     title: The title of the document.
#     movie_data: A list of dictionaries, where each dictionary represents a movie with data
#                 For example:
#                 [
#                     {"title": "Movie 1", "rating": 4, "date": "2024-01-01", "review": "Great movie!"},
#                     {"title": "Movie 2", "rating": 5, "date": "2024-01-15", "review": "Amazing!"},
#                 ]


def build_movie_dictionary_list(movies):
    movie_dictionary_list = []

    for movie in movies:
        movie_poster_and_review = get_movie_poster_and_review(movie.summary)
        movie_dictionary_list.append(dict(
            title = movie.letterboxd_filmtitle, #Captain America: Brave New World
            year = movie.letterboxd_filmyear, #2025
            rating = movie.letterboxd_memberrating, #2.5
            watched_date = movie.letterboxd_watcheddate, #2025-02-16
            review_link = movie.link, #https://letterboxd.com/jorge_h18/film/captain-america-brave-new-world/
            rewatch = movie.letterboxd_rewatch, #No
            movie_id = movie.tmdb_movieid, #822119
            poster = movie_poster_and_review[0],
            review = movie_poster_and_review[1]
            ))
        
    return movie_dictionary_list



def main():
    rss_url = "https://letterboxd.com/jorge_h18/rss/"
    feed = feedparser.parse(rss_url)
    print("Number of movies: ", len(feed.entries))

    print(build_movie_dictionary_list(feed.entries))
    #build_markdown(movie_data)


if __name__=="__main__":
    main()