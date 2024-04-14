import random

def select_random_years(ratings, min_years=5, year_selection_threshold=8):
    if len(ratings) < min_years:
        return []  # Not enough data to play the game

    num_years_to_select = 3 if len(ratings) >= year_selection_threshold else 2
    if len(ratings) < year_selection_threshold:
        num_years_to_select = min(len(ratings), 2)  # Adjust based on available data

    selected_years = random.sample(ratings, num_years_to_select)
    return selected_years

# Example usage:
ratings_example = [{'year': 2010, 'rating': 85}, {'year': 2011, 'rating': 87},
                   {'year': 2012, 'rating': 88}, {'year': 2013, 'rating': 90},
                   {'year': 2014, 'rating': 92}, {'year': 2015, 'rating': 93},
                   {'year': 2016, 'rating': 94}, {'year': 2017, 'rating': 95},
                   {'year': 2018, 'rating': 96}, {'year': 2019, 'rating': 97}]

random_years = select_random_years(ratings_example)
print(random_years)