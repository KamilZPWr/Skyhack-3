labels_dict = {'Animals': ['zwierzęta', 'zwierzę', 'zwierzyna'],
                'Bench': ['ławka'],
                'Building': ['budynek', 'dom', 'zamek'],
                'Castle': ['zamek', 'ruiny'],
                'Cave': ['jaskinia', 'grota', 'sztolnia'],
                'Church': ['kościół'],
                'City': ['miasto', 'przedmieścia', 'dzielnica'],
                'Cross': ['krzyż'],
                'Cultural institution': ['muzeum', 'kino', 'teatr', ],
                'Food': ['jedzenie', 'posiłek', 'restauracja'],
                'Footpath': ['ścieżka', 'szlak', 'dróżka'],
                'Forest': ['las', 'zalesiony', 'drzewa'],
                'Furniture': ['meble', 'mebel'],
                'Grass': ['trawa', 'trawnik'],
                'Graveyard': ['cmentarz', 'grób'],
                'Lake': ['jezioro', 'staw'],
                'Landscape': ['krajobraz', 'widok', 'panorama', 'sceneria'],
                'Mine': ['kopalnia', 'szyb', 'sztolnia'],
                'Monument': ['posąg', 'rzeźba'],
                'Motor vehicle': ['samochód', 'samochodem', 'pojazd'],
                'Mountains': ['góry', 'tatry', 'szczyty', 'wzgórza'],
                'Museum': ['muzeum'],
                'Open-air museum': ['skansen'],
                'Park': ['park'],
                'Person': ['osoba', 'ludzie', 'człowiek', 'kobieta', 'mężczyzna'],
                'Plants': ['rośliny', 'kwiaty'],
                'Reservoir': ['rezerwat', 'park narodowy'],
                'River': ['rzeka', 'strumyk', 'potok'],
                'Road': ['droga', 'szosa'],
                'Rocks': ['skały', 'kamienie'],
                'Snow': ['śnieg'],
                'Sport': ['sport', 'dyscyplina'],
                'Sports facility': ['siłownia', 'basen', 'boisko', 'kort'],
                'Stairs': ['schody'],
                'Trees': ['drzewa', 'drzewo', 'park'],
                'Watercraft': ['statek', 'okręt', 'żaglówka', 'łódź'],
                'Windows': ['okno', 'okna', 'dom']}


def get_labels_from_text(text: str) -> list:
    list_of_labels = []
    for k, v in labels_dict.items():
        for word in v:
            if word in text.split():
                list_of_labels.append(k)
                break
    return list_of_labels

if __name__ == '__main__':
    s = 'Mieszkam przy ulicy parkowej, znajduje się tam siłownia'
    l = get_labels_from_text(s)
    print(l)