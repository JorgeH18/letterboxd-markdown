import feedparser, re

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
    star_rating = const_number_to_stars.get(number_rating_str, "None")
    return star_rating


def build_movie_dictionary_list(movies):
    movie_dictionary_list = []

    for movie in movies:
        movie_poster_and_review = get_movie_poster_and_review(movie.summary)
        movie_dictionary_list.append(dict(
            poster = movie_poster_and_review[0],
            title = movie.letterboxd_filmtitle,
            year = movie.letterboxd_filmyear,
            #movie_id = movie.tmdb_movieid,
            rating = get_rating(movie.letterboxd_memberrating), #transforming to stars
            watched_date = movie.letterboxd_watcheddate,
            rewatch = movie.letterboxd_rewatch,
            review = movie_poster_and_review[1],
            review_link = movie.link
            ))
        
    return movie_dictionary_list


def build_markdown(filename, title, movie_data):
    # Creates a Markdown file with a title, table of contents, and movie data.

    # Args:
    #     filename: The name of the Markdown file to create (e.g., "movies.md").
    #     title: The title of the document.
    #     movie_data: A list of dictionaries, where each dictionary represents a movie with data

    with open(filename, "w", encoding="utf-8") as f:  # Use utf-8 encoding
        f.write(f"# {title}\n\n")

        # Create the table of contents (using Markdown extensions)
        # Create the table header
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
                        markdown_image = f'<img src="{poster_url}" width="100em" height="150em">' # HTML image format
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


# TO DO: check if there is no rating to the review
def main():
    rss_url = "https://letterboxd.com/jorge_h18/rss/"
    feed = feedparser.parse(rss_url)
    print("Number of movies: ", len(feed.entries))

    movie_dictionary_list = build_movie_dictionary_list(feed.entries)
    build_markdown("letterboxd-diary.md", "Watched Movies", movie_dictionary_list)


if __name__=="__main__":
    main()