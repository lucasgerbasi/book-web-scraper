import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Create directories if they don't exist
os.makedirs('data', exist_ok=True)
os.makedirs('output', exist_ok=True)
os.makedirs('css', exist_ok=True)

# Fetch the HTML content
url = "http://books.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract data
    books = []
    for book in soup.select('.product_pod'):
        title = book.h3.a['title']  # Book title
        price = book.select_one('.price_color').text.strip()  # Price
        price = price.replace('Â', '').replace('Â£', '£').strip()  # Clean up the price string

        rating_class = book.select_one('p.star-rating')['class'][1]
        rating = rating_class.capitalize()

        books.append({
            'Title': title,
            'Price': price,
            'Rating': rating
        })

    print(f"Found {len(books)} books.")

    # Create DataFrame
    df = pd.DataFrame(books)

    # Save to CSV in data directory
    df.to_csv('data/books.csv', index=False)
    print("Data saved to 'data/books.csv'.")

    # Generate HTML with CSS link
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Book List</title>
        <link rel="stylesheet" type="text/css" href="../css/style.css">
    </head>
    <body>
        <h1>Book List</h1>
        <table>
            <caption>Books Available</caption>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Price</th>
                    <th>Rating</th>
                </tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html_content += f"""
                <tr>
                    <td>{row['Title']}</td>
                    <td>{row['Price']}</td>
                    <td>{row['Rating']}</td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    # Save to HTML in output
    with open('output/books.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Data saved to 'output/books.html'.")

else:
    print("Failed to retrieve the webpage.")
