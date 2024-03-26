# For the whole period
all_musician_paths = {
    # Baroque
    'Bach': './asap-dataset/Bach/',
    # Classical
    'Haydn': './asap-dataset/Haydn/',
    'Mozart': './asap-dataset/Mozart/',
    'Beethoven': './asap-dataset/Beethoven/',
    # Romantic
    'Chopin': './asap-dataset/Chopin/',
    'Liszt': './asap-dataset/Liszt/',
    'Schumann': './asap-dataset/Schumann/',
    'Brahms': './asap-dataset/Brahms',
    'Tchaikovsky': './asap-dataset/Tchaikovsky/',
    'Rachmaninoff': './asap-dataset/Rachmaninoff/',
    'Schubert': './asap-dataset/Schubert/',
    # Impressionist
    'Debussy': './asap-dataset/Debussy/',
    # Modern
    'Prokofiev': './asap-dataset/Prokofiev/',
    'Ravel': './asap-dataset/Ravel/',
    'Scriabin': './asap-dataset/Scriabin/',
    'Balakirev': './asap-dataset/Balakirev/',
    'Glinka': './asap-dataset/Glinka/',
}

# define the period
era_musician_paths = {
    'Baroque': ['Bach'],
    'Classical': ['Mozart', 'Haydn', 'Beethoven'],
    'Romantic': ['Chopin', 'Liszt', 'Schumann', 'Brahms', 'Tchaikovsky', 'Rachmaninoff', 'Schubert'],
    'Impressionist': ['Debussy'],
    'Modern': ['Prokofiev', 'Ravel', 'Scriabin', 'Balakirev', 'Glinka'],
}

Baroque_musician_paths = {
    musician: all_musician_paths[musician] for musician in era_musician_paths['Baroque']
}

Classical_musician_paths = {
    musician: all_musician_paths[musician] for musician in era_musician_paths['Classical']
}

Romantic_musician_paths = {
    musician: all_musician_paths[musician] for musician in era_musician_paths['Romantic']
}

Impressionist_musician_paths = {
    musician: all_musician_paths[musician] for musician in era_musician_paths['Impressionist']
}

Modern_musician_paths = {
    musician: all_musician_paths[musician] for musician in era_musician_paths['Modern']
}
