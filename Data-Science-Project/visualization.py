import matplotlib.pyplot as plt
import pandas as pd

def plot_popular_artists(no_features, counting_features, name_y = "", title = "", count = 10):
# Create a figure with 2 columns and 1 row
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # Adjust figsize for better display
    fig.suptitle(title)
    
    #Artists and values, excluding features
    no_features = no_features.head(count).to_dict()
    artists_no_features = list(no_features.keys())
    values_no_features = list(no_features.values())
    
    # First bar plot
    axs[0].bar(artists_no_features, values_no_features, color='moccasin', edgecolor='black')
    axs[0].set_xlabel("Artist")
    axs[0].set_ylabel(name_y)
    axs[0].set_title("Top 15 Main Artists")
    axs[0].set_xticks(artists_no_features)
    axs[0].set_xticklabels(artists_no_features, rotation=45, ha='right')
    
    #Artists and values, counting features
    counting_features = counting_features.head(count).to_dict()
    artists_with_features = list(counting_features.keys())
    values_with_features = list(counting_features.values())

    # Second bar plot
    axs[1].bar(artists_with_features, values_with_features, color='limegreen', edgecolor='black')
    axs[1].set_xlabel("Artist")
    axs[1].set_ylabel(name_y)
    axs[1].set_title("Top 15 Artists Counting Features")
    axs[1].set_xticks(artists_with_features)
    axs[1].set_xticklabels(artists_with_features, rotation=45, ha='right')

    plt.tight_layout()
    plt.show()
    

def period_avg_position(data, genre, start_year, end_year, return_result = False):
    avg = data[(data.spotify_genre == genre) & (data.year >= start_year) & (data.year <= end_year)].peak_position.mean()
     
    if return_result:
        return avg
    
    print(f"Average position for {genre} songs during {start_year}-{end_year}: {round(avg, 2) * -1}")
    
    
def plot_genre_performance(data, genre):
    performance_over_years = data[data.spotify_genre == genre].year.value_counts().to_dict()
    performance_over_years = dict(sorted(performance_over_years.items()))
    
    plt.plot(performance_over_years.keys(), performance_over_years.values(), color = 'lightgreen', linewidth = 3)
    plt.scatter(performance_over_years.keys(), performance_over_years.values(), s = 15, color = 'indigo', zorder=5)
    plt.grid()
    plt.xlabel("Year")
    plt.ylabel("Number of songs")
    plt.title(f"{genre.capitalize()} songs over the years")
    
    plt.show()
    

def spotify_feature_subplot(ax, data, col_name, clr = 'gold'):
    avg_values = data.groupby('spotify_genre')[col_name].mean().sort_values(ascending = False).head(5).to_dict()
    

    ax.bar(avg_values.keys(), avg_values.values(), color = clr)
    ax.set_xlabel("Top Genres")
    ax.set_ylabel("Average Value")
    ax.set_title(col_name.capitalize().replace("_", " "))
    
    x_labels = avg_values.keys()
    ax.set_xticks(list(x_labels))
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    if (data[col_name].sum() < 0):
        ax.invert_yaxis()
        
        
def boxplot_chart_performance(data, genre, start_year = 1958, end_year = 2024, interval = 1, relative_genre_name = False):
    if relative_genre_name:
        filtered_years = data[(data.spotify_genre.str.contains(genre)) & (data.year >= start_year) & (data.year <= end_year)].copy()
    else:
        filtered_years = data[(data.spotify_genre == genre) & (data.year >= start_year) & (data.year <= end_year)].copy()

    filtered_years['year_group'] = pd.cut(filtered_years['year'], bins = range(start_year, end_year + 1, interval), right = False)
    
    filtered_years.boxplot(column = "peak_position", by = "year_group", figsize = (8, 5))
    plt.ylabel('peak positions')
    plt.title("")
    plt.suptitle(f"Chart performance of {genre} songs over the years")
    plt.gca().invert_yaxis() #Invert the values, so that 1 is the highest position
    
    
