# Filename: zadanie13.py
# Opis:
# Poniższy kod tworzy plik XML zawierający wygenerowane 20 tysięcy leków
# (100 oryginalnych + 19 900 wygenerowanych). Zawiera funkcję generate_test_database()
# oraz przykładowe wywołanie run_analysis_on_generated_data(), które można
# zintegrować z kodem z pliku podpunkt1.py (zadania 1-12).

import xml.etree.ElementTree as ET
import random


def generate_test_database(original_file, new_file, num_to_generate=19900, ns={'db': 'http://www.drugbank.ca'}):
    """
    Generuje dodatkowe wpisy leków na podstawie istniejących i zapisuje wynik do pliku XML.
    :param original_file: Ścieżka do oryginalnego pliku (z ok. 100 lekami).
    :param new_file: Ścieżka do nowego pliku, w którym zapisujemy łącznie 20 000 leków.
    :param num_to_generate: Liczba nowych wpisów, jakie chcemy wygenerować.
    :param ns: Namespace używany do znalezienia tagów w pliku XML.
    """
    tree = ET.parse(original_file)
    root = tree.getroot()

    # Znajdowanie istniejących leków
    original_drugs = root.findall('db:drug', ns)
    if not original_drugs:
        print("Brak wpisów w pliku oryginalnym.")
        return

    # Konwertujemy listę do losowania
    original_drugs_list = list(original_drugs)

    max_id_num = 0
    # Szukamy największego numeru w atrybucie <drugbank-id> (primary="true")
    for drug in original_drugs:
        db_id_elem = drug.find('db:drugbank-id[@primary="true"]', ns)
        if db_id_elem is not None:
            numeric_part = ''.join(ch for ch in db_id_elem.text if ch.isdigit())
            if numeric_part:
                numeric_val = int(numeric_part)
                if numeric_val > max_id_num:
                    max_id_num = numeric_val

    # Generujemy 19 900 nowych leków
    for i in range(num_to_generate):
        # Losowo wybieramy oryginalny lek do skopiowania danych
        template_drug = random.choice(original_drugs_list)

        # Kopiujemy całą strukturę <drug>
        new_drug = ET.fromstring(ET.tostring(template_drug, encoding='utf-8'))

        # Ustawiamy inny atrybut type (opcjonalnie)
        new_drug.set('type', 'test-simulated')

        # Zmieniamy (primary) DrugBank ID
        new_db_id = new_drug.find('db:drugbank-id[@primary="true"]', ns)
        if new_db_id is not None:
            # Nadajemy format DBTEST00001, DBTEST00002, itp.
            new_id_value = f"DBTEST{(i + 1):05d}"
            new_db_id.text = new_id_value

        # Dodajemy nowy wpis do drzewa XML
        root.append(new_drug)

    # Zapisujemy do pliku
    tree.write(new_file, encoding="utf-8", xml_declaration=True)
    print(f"Plik {new_file} zapisany z łączną liczbą leków: {len(root.findall('db:drug', ns))}.")


def run_analysis_on_generated_data():
    """
    Przykład wywołania funkcji generującej bazę,
    a następnie uruchomienie zadań 1-12 z pliku podpunkt1.py.
    Upewnij się, że w podpunkt1.py masz zaimportowane odpowiednie biblioteki i
    zdefiniowane zadania (zadanie1, zadanie2, itd.).
    """
    ns = {'db': 'http://www.drugbank.ca'}

    original_file = 'drugbank_partial.xml'
    new_file = 'drugbank_partial_and_generated.xml'

    # 1) Generowanie testowej bazy (100 + 19 900 = 20 000)
    generate_test_database(original_file, new_file, num_to_generate=19900, ns=ns)

    # 2) Import z pliku podpunkt1.py (zadania 1-12):
    from podpunkt1 import (zadanie1, zadanie2, zadanie3, zadanie4,
                           zadanie5, zadanie6, zadanie7, zadanie8,
                           zadanie9, zadanie10, zadanie11, zadanie12)

    # 3) Wczytanie nowo utworzonego pliku
    tree = ET.parse(new_file)
    root = tree.getroot()

    # 4) Wywołanie zadań 1-12
    zadanie1(root, ns)
    zadanie2(root, ns)
    zadanie3(root, ns)
    zadanie4(root, ns)
    zadanie5(root, ns)
    zadanie6(root, ns)
    zadanie7(root, ns)
    zadanie8(root, ns)
    zadanie9(root, ns)
    zadanie10(root, ns)
    zadanie11(root, ns, specific_gene='F2')  # Przykładowy gen
    zadanie12(root, ns)

run_analysis_on_generated_data()