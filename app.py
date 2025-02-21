# Imports necessary libraries
import feedparser, re
from datetime import datetime

# Extracts poster URL and review text from a movie summary using RegEx
def get_movie_poster_and_review(summary):
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

# Converts numeric rating to star symbols.
def get_rating(number_rating):
    const_number_to_stars = {
        "0.5": "½",
        "1.0": "★",
        "1.5": "★½",
        "2.0": "★★",
        "2.5": "★★½",
        "3.0": "★★★",
        "3.5": "★★★½",
        "4.0": "★★★★",
        "4.5": "★★★★½",
        "5.0": "★★★★★"
    }

    number_rating_str = str(number_rating)
    star_rating = const_number_to_stars.get(number_rating_str, " ")
    return star_rating

 # Reformats date from YYYY-MM-DD to DD/MM/YYYY.
def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d/%m/%Y")

# Builds a list of movie dictionaries from RSS feed entries.
def build_movie_dictionary_list(movies):
    movie_dictionary_list = []

    for movie in movies:
        movie_poster_and_review = get_movie_poster_and_review(movie.summary)
        movie_dictionary_list.append(dict(
            poster = movie_poster_and_review[0],
            title = movie.letterboxd_filmtitle,
            year = movie.letterboxd_filmyear,
            #movie_id = movie.tmdb_movieid,
            rating = get_rating(getattr(movie, "letterboxd_memberrating", "0")), # Handling if there is no rating on the review
            watched_date = format_date(movie.letterboxd_watcheddate),
            rewatch = movie.letterboxd_rewatch,
            review = movie_poster_and_review[1],
            review_link = movie.link
            ))
        
    return movie_dictionary_list

# Builds a Markdown file from movie data.
    # Args:
    #     filename: The name of the Markdown file to create (e.g., "movies.md").
    #     title: The title of the document.
    #     movie_data: A list of dictionaries, where each dictionary represents a movie with data
def build_markdown(filename, title, movie_data):
    with open(filename, "w", encoding="utf-8") as f:  # Use utf-8 encoding
        f.write(f"# {title}\n\n")

        if movie_data:  # Check if movie_data is not empty
            header = movie_data[0].keys()  # Get keys from the first movie's dictionary
            # Filter out "rewatch" from the header
            filtered_header = [key for key in header if key != "rewatch"]
            f.write("| " + " | ".join(filtered_header).title() + " |\n")
            f.write("| " + " | ".join(["---"] * len(filtered_header)) + " |\n")

            # Populate the table rows
            for movie in movie_data:
                row = []
                for key in header:
                    # Special handling for the 'poster' column for setting the image
                    if key == "poster":
                        poster_url = movie.get(key, "")
                        #markdown_image = f"![{title}]({poster_url})" # Markdown image format
                        markdown_image = f'<img src="{poster_url}" width="100px" height="150px">' # HTML image format
                        row.append(markdown_image)

                    # Special handling for the 'watched date' column for specify if is a rewatch
                    elif key == "watched_date" and movie["rewatch"]=="Yes" :
                        row.append(str(movie.get(key, "") + " 🔁"))
                    # Also if is a rewatch skip the step as that attribute is only wanted for the previous code
                    elif key == "rewatch":
                        continue

                    # For the rest of the data
                    else:
                        row.append(str(movie.get(key, "")))
                f.write("| " + " | ".join(row) + " |\n")

        else:
            f.write("No movie data available.\n")

#Parses the Letterboxd RSS feed and returns only diary entries (films).
def get_diary_entries(rss_url):
    feed = feedparser.parse(rss_url)
    diary_entries = []

    for entry in feed.entries:
        # Check for the presence of a 'movieid' or similar identifier that only films have.
        if hasattr(entry, 'tmdb_movieid'):
            diary_entries.append(entry)

    return diary_entries


def main():
    # Example usage:
    rss_url = "https://letterboxd.com/jorge_h18/rss/"  # Replace with your actual RSS URL
    diary_entries = get_diary_entries(rss_url)
    print("Number of movies: ", len(diary_entries))

    movie_dictionary_list = build_movie_dictionary_list(diary_entries)
    build_markdown("letterboxd-diary.md", "Watched Movies", movie_dictionary_list)


if __name__=="__main__":
    main()