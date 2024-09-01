import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns


def get_common_words(dataset, total_words = 100, genre = None, col = 'all_words'):
    """
    Returns a dictionary containing the most common words for 
    a genre by iterating through the given dataset."""
    if genre:
        rows_matching_genre = dataset[dataset.spotify_genre == genre] #Filter the dataframe
    else:
        rows_matching_genre = dataset
    word_list = []
    for val in rows_matching_genre[col]:
        word_list.extend(val) #Add the lyrics to the initiated word_list
    count_words = Counter(word_list) #Count the occurances of each word
    return count_words.most_common(total_words)


def plot_common_words(dataset, total_words = 100, genre = None, col = 'all_words'):
    """
    Create either a barplot or a word cloud, displaying the most used words in a specified genre.
    Uses the get_common_words function to get the data.
    """
    common_words = get_common_words(dataset, total_words, genre, col)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(common_words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    

def word_avg_position(data, n = 100, lowest_positions = True):
    
    # Filter out words that occur less than n times
    word_counts = data['words'].value_counts()
    frequent_words = word_counts[word_counts >= n].index
    
    filtered_data = data[data.words.isin(frequent_words)]
    avg_pos = filtered_data.groupby('words').peak_position.mean().sort_values(ascending = lowest_positions).head(10)
    avg_pos = pd.DataFrame(avg_pos).reset_index()
    avg_pos.columns = ['word', 'position']
    avg_pos.position = avg_pos.position.apply(lambda x: round(x, 2))
    
    plt.figure(figsize = (10, 6))
    sns.barplot(x='word', y='position', data=avg_pos, palette='viridis')

    plt.title("Top 10 words with the lowest average chart position")
    plt.gca().invert_yaxis()
    plt.gca().bar_label(plt.gca().containers[0])