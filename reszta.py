import pandas as pd
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt

# Wczytanie pliku XML
tree = ET.parse('drugbank_partial.xml')
root = tree.getroot()

# Namespace
ns = {'db': 'http://www.drugbank.ca'}

# Zadanie 1: Tworzenie ramki danych z informacjami o lekach
def zadanie1(root, ns):
    def create_drug_info_dataframe(root, ns):
        drug_data = []

        for drug in root.findall('db:drug', ns):
            drug_info = {
                'drugbank_id': drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                    'db:drugbank-id[@primary="true"]', ns) is not None else None,
                'name': drug.find('db:name', ns).text if drug.find('db:name', ns) is not None else None,
                'type': drug.get('type'),
                'description': drug.find('db:description', ns).text if drug.find('db:description',
                                                                                 ns) is not None else None,
                'state': drug.find('db:state', ns).text if drug.find('db:state', ns) is not None else None,
                'indication': drug.find('db:indication', ns).text if drug.find('db:indication',
                                                                               ns) is not None else None,
                'mechanism_of_action': drug.find('db:mechanism-of-action', ns).text if drug.find(
                    'db:mechanism-of-action', ns) is not None else None,
                'food_interactions': ', '.join(
                    [fi.text for fi in drug.findall('db:food-interactions/db:food-interaction', ns)]) if drug.findall(
                    'db:food-interactions/db:food-interaction', ns) else None
            }
            drug_data.append(drug_info)

        df = pd.DataFrame(drug_data)
        return df

    df_drug_info = create_drug_info_dataframe(root, ns)
    print("Drug Info DataFrame:")
    print(df_drug_info)

    df_drug_info.to_csv('podpunkt1.csv', index=False)

# Zadanie 2: Tworzenie ramki danych z synonimami leków
def zadanie2(root, ns):
    def create_synonyms_dataframe(root, ns):
        synonyms_data = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            for synonym in drug.findall('db:synonyms/db:synonym', ns):
                synonyms_data.append({
                    'drugbank_id': drugbank_id,
                    'synonym': synonym.text
                })

        df_synonyms = pd.DataFrame(synonyms_data)
        return df_synonyms

    df_synonyms = create_synonyms_dataframe(root, ns)
    print("Synonyms DataFrame:")
    print(df_synonyms)

    df_synonyms.to_csv('podpunkt2.csv', index=False)

    def draw_synonyms_graph(drugbank_id, df_synonyms):
        synonyms = df_synonyms[df_synonyms['drugbank_id'] == drugbank_id]

        if synonyms.empty:
            print(f"No synonyms found for DrugBank ID: {drugbank_id}")
            return

        G = nx.Graph()

        for _, row in synonyms.iterrows():
            G.add_edge(drugbank_id, row['synonym'])

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold",
                edge_color="gray")
        plt.title(f"Synonyms for DrugBank ID: {drugbank_id}")
        plt.show()

    draw_synonyms_graph('DB00001', df_synonyms)

# Zadanie 3: Tworzenie ramki danych o produktach farmaceutycznych
def zadanie3(root, ns):
    def create_products_dataframe(root, ns):
        products_data = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            for product in drug.findall('db:products/db:product', ns):
                product_info = {
                    'drugbank_id': drugbank_id,
                    'product_name': product.find('db:name', ns).text if product.find('db:name',
                                                                                     ns) is not None else None,
                    'manufacturer': product.find('db:labeller', ns).text if product.find('db:labeller',
                                                                                         ns) is not None else None,
                    'ndc_product_code': product.find('db:ndc-product-code', ns).text if product.find(
                        'db:ndc-product-code', ns) is not None else None,
                    'dosage_form': product.find('db:dosage-form', ns).text if product.find('db:dosage-form',
                                                                                           ns) is not None else None,
                    'route': product.find('db:route', ns).text if product.find('db:route', ns) is not None else None,
                    'strength': product.find('db:strength', ns).text if product.find('db:strength',
                                                                                     ns) is not None else None,
                    'country': product.find('db:country', ns).text if product.find('db:country',
                                                                                   ns) is not None else None,
                    'source': product.find('db:source', ns).text if product.find('db:source', ns) is not None else None
                }
                products_data.append(product_info)

        df_products = pd.DataFrame(products_data)
        return df_products

    df_products = create_products_dataframe(root, ns)
    print("Products DataFrame:")
    print(df_products)

    df_products.to_csv('podpunkt3.csv', index=False)

# Zadanie 4: Tworzenie ramki danych o szlakach interakcji leków
def zadanie4(root, ns):
    def create_pathways_dataframe(root, ns):
        pathways_data = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            for pathway in drug.findall('db:pathways/db:pathway', ns):
                pathway_info = {
                    'drugbank_id': drugbank_id,
                    'pathway_id': pathway.find('db:smpdb-id', ns).text if pathway.find('db:smpdb-id',
                                                                                       ns) is not None else None,
                    'pathway_name': pathway.find('db:name', ns).text if pathway.find('db:name',
                                                                                     ns) is not None else None,
                    'pathway_category': pathway.find('db:category', ns).text if pathway.find('db:category',
                                                                                             ns) is not None else None
                }
                pathways_data.append(pathway_info)

        df_pathways = pd.DataFrame(pathways_data)
        return df_pathways

    df_pathways = create_pathways_dataframe(root, ns)
    print("Pathways DataFrame:")
    print(df_pathways)

    total_pathways = df_pathways['pathway_id'].nunique()
    print(f"Total number of pathways: {total_pathways}")

    df_pathways.to_csv('podpunkt4.csv', index=False)

def zadanie5(root, ns):
    def create_pathway_drug_interactions_dataframe(root, ns):
        pathway_interactions = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            drug_name = drug.find('db:name', ns).text if drug.find('db:name', ns) is not None else None

            for pathway in drug.findall('db:pathways/db:pathway', ns):
                pathway_interactions.append({
                    'pathway_id': pathway.find('db:smpdb-id', ns).text if pathway.find('db:smpdb-id',
                                                                                       ns) is not None else None,
                    'pathway_name': pathway.find('db:name', ns).text if pathway.find('db:name',
                                                                                     ns) is not None else None,
                    'drugbank_id': drugbank_id,
                    'drug_name': drug_name
                })

        df_interactions = pd.DataFrame(pathway_interactions)
        return df_interactions

    df_interactions = create_pathway_drug_interactions_dataframe(root, ns)
    print("Pathway-Drug Interactions DataFrame:")
    print(df_interactions)

    df_interactions.to_csv('podpunkt5.csv', index=False)

    def draw_bipartite_graph(df_interactions):
        B = nx.Graph()

        pathway_nodes = df_interactions['pathway_name'].unique()
        drug_nodes = df_interactions['drug_name'].unique()

        B.add_nodes_from(pathway_nodes, bipartite=0, color='lightcoral')
        B.add_nodes_from(drug_nodes, bipartite=1, color='skyblue')

        edges = [(row['drug_name'], row['pathway_name']) for _, row in df_interactions.iterrows()]
        B.add_edges_from(edges)

        pos = nx.spring_layout(B, seed=42)
        colors = [B.nodes[node]['color'] for node in B.nodes]

        plt.figure(figsize=(12, 8))
        nx.draw(B, pos, with_labels=True, node_size=2000, node_color=colors, font_size=8, edge_color='gray')
        plt.title("Bipartite Graph of Drug-Pathway Interactions")
        plt.show()

    draw_bipartite_graph(df_interactions)

def zadanie6(root, ns):
    def create_drug_pathway_count_dataframe(root, ns):
        drug_pathway_counts = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            drug_name = drug.find('db:name', ns).text if drug.find('db:name', ns) is not None else None
            pathway_count = len(drug.findall('db:pathways/db:pathway', ns))

            drug_pathway_counts.append({
                'drugbank_id': drugbank_id,
                'drug_name': drug_name,
                'pathway_count': pathway_count
            })

        df_counts = pd.DataFrame(drug_pathway_counts)
        return df_counts

    df_counts = create_drug_pathway_count_dataframe(root, ns)
    print("Drug Pathway Counts DataFrame:")
    print(df_counts)

    df_counts.to_csv('popdunkt6.csv', index=False)

    def plot_histogram(df_counts):
        plt.figure(figsize=(12, 8))
        plt.hist(df_counts['pathway_count'], bins=range(0, df_counts['pathway_count'].max() + 2), edgecolor='black')
        plt.xlabel('Number of Pathways')
        plt.ylabel('Number of Drugs')
        plt.title('Histogram of Number of Pathways per Drug')
        plt.xticks(range(0, df_counts['pathway_count'].max() + 2))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    plot_histogram(df_counts)

def zadanie7(root, ns):
    def create_protein_interactions_dataframe(root, ns):
        protein_interactions = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            drug_name = drug.find('db:name', ns).text if drug.find('db:name', ns) is not None else None

            for target in drug.findall('db:targets/db:target', ns):
                target_id = target.find('db:id', ns).text if target.find('db:id', ns) is not None else None
                polypeptide = target.find('db:polypeptide', ns)

                if polypeptide is not None:
                    polypeptide_name = polypeptide.find('db:name', ns).text if polypeptide.find('db:name',
                                                                                                ns) is not None else None
                    gene_name = polypeptide.find('db:gene-name', ns).text if polypeptide.find('db:gene-name',
                                                                                              ns) is not None else None
                    chromosome = polypeptide.find('db:chromosome-location', ns).text if polypeptide.find(
                        'db:chromosome-location', ns) is not None else None
                    cellular_location = polypeptide.find('db:cellular-location', ns).text if polypeptide.find(
                        'db:cellular-location', ns) is not None else None

                    # Pobieranie external identifiers
                    external_ids_list = []
                    genatlas_id = None
                    external_ids = polypeptide.find("db:external-identifiers", ns)

                    if external_ids is not None:
                        for external_id_entry in external_ids.findall("db:external-identifier", ns):
                            resource = external_id_entry.find("db:resource", ns)
                            identifier = external_id_entry.find("db:identifier", ns)

                            if resource is not None and identifier is not None:
                                external_ids_list.append(f"{resource.text}: {identifier.text}")

                                # Sprawdzamy, czy to GenAtlas
                                if resource.text.strip().lower() == "genatlas":
                                    genatlas_id = identifier.text

                    external_id = ", ".join(external_ids_list) if external_ids_list else None

                    protein_interactions.append({
                        'drugbank_id': drugbank_id,
                        'drug_name': drug_name,
                        'target_id': target_id,
                        'source': polypeptide.get('source'),  # Pobieranie atrybutu "source" z polypeptide
                        'external_id': external_id,
                        'polypeptide_name': polypeptide_name,
                        'gene_name': gene_name,
                        'genatlas_id': genatlas_id,
                        'chromosome': chromosome,
                        'cellular_location': cellular_location
                    })

        df_proteins = pd.DataFrame(protein_interactions)
        return df_proteins

    df_proteins = create_protein_interactions_dataframe(root, ns)
    print("Protein-Drug Interactions DataFrame:")
    print(df_proteins)

    df_proteins.to_csv('podpunkt7.csv', index=False)

def zadanie8(root, ns):
    def create_protein_interactions_dataframe(root, ns):
        protein_interactions = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            drug_name = drug.find('db:name', ns).text if drug.find('db:name', ns) is not None else None

            for target in drug.findall('db:targets/db:target', ns):
                target_id = target.find('db:id', ns).text if target.find('db:id', ns) is not None else None
                polypeptide = target.find('db:polypeptide', ns)

                if polypeptide is not None:
                    polypeptide_name = polypeptide.find('db:name', ns).text if polypeptide.find('db:name', ns) is not None else None
                    gene_name = polypeptide.find('db:gene-name', ns).text if polypeptide.find('db:gene-name', ns) is not None else None
                    chromosome = polypeptide.find('db:chromosome-location', ns).text if polypeptide.find('db:chromosome-location', ns) is not None else None
                    cellular_location = polypeptide.find('db:cellular-location', ns).text if polypeptide.find('db:cellular-location', ns) is not None else None

                    protein_interactions.append({
                        'drugbank_id': drugbank_id,
                        'drug_name': drug_name,
                        'target_id': target_id,
                        'polypeptide_name': polypeptide_name,
                        'gene_name': gene_name,
                        'chromosome': chromosome,
                        'cellular_location': cellular_location
                    })

        df_proteins = pd.DataFrame(protein_interactions)
        return df_proteins

    # Tworzymy ramkę danych
    df_proteins = create_protein_interactions_dataframe(root, ns)

    # Zliczenie liczby wystąpień każdej lokalizacji w komórce
    location_counts = df_proteins['cellular_location'].value_counts()

    # Tworzenie wykresu kołowego
    plt.figure(figsize=(8, 8))
    plt.pie(location_counts, labels=location_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title("Procentowe występowanie targetów w różnych częściach komórki")
    plt.show()

def zadanie9(root, ns):
    def create_drug_status_dataframe(root, ns):
        status_data = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            groups = [group.text for group in drug.findall('db:groups/db:group', ns)]

            status_data.append({
                'drugbank_id': drugbank_id,
                'approved': 'approved' in groups,
                'withdrawn': 'withdrawn' in groups,
                'experimental': 'experimental' in groups,
                'investigational': 'investigational' in groups,
                'vet_approved': 'vet_approved' in groups
            })

        df_status = pd.DataFrame(status_data)
        return df_status

    df_status = create_drug_status_dataframe(root, ns)
    print("Drug Status DataFrame:")
    print(df_status)

    # Liczenie liczby leków w poszczególnych kategoriach
    approved_count = df_status['approved'].sum()
    withdrawn_count = df_status['withdrawn'].sum()
    experimental_count = df_status['experimental'].sum()
    investigational_count = df_status['investigational'].sum()
    vet_approved_count = df_status['vet_approved'].sum()

    # Liczenie liczby zatwierdzonych leków, które nie zostały wycofane
    approved_not_withdrawn_count = df_status[(df_status['approved']) & (~df_status['withdrawn'])].shape[0]

    print(f"Liczba zatwierdzonych leków, które nie zostały wycofane: {approved_not_withdrawn_count}")

    # Tworzenie wykresu kołowego
    def plot_pie_chart(approved, withdrawn, experimental, investigational, vet_approved):
        labels = ['Approved', 'Withdrawn', 'Experimental', 'Investigational', 'Vet Approved']
        sizes = [approved, withdrawn, experimental, investigational, vet_approved]
        colors = ['lightgreen', 'lightcoral', 'lightskyblue', 'lightyellow', 'lightpink']
        explode = (0.1, 0, 0, 0, 0)  # Wysunięcie pierwszego klina (zatwierdzone)

        plt.figure(figsize=(10, 7))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Utrzymanie koła w równowadze
        plt.title('Drug Status Distribution')
        plt.show()

    plot_pie_chart(approved_count, withdrawn_count, experimental_count, investigational_count, vet_approved_count)

def zadanie10(root, ns):
    def create_drug_interactions_dataframe(root, ns):
        interactions_data = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find('db:drugbank-id[@primary="true"]', ns) is not None else None
            drug_name = drug.find('db:name', ns).text if drug.find('db:name', ns) is not None else None
            for interaction in drug.findall('db:drug-interactions/db:drug-interaction', ns):
                interacting_drug_id = interaction.find('db:drugbank-id', ns).text if interaction.find('db:drugbank-id', ns) is not None else None
                interacting_drug_name = interaction.find('db:name', ns).text if interaction.find('db:name', ns) is not None else None
                description = interaction.find('db:description', ns).text if interaction.find('db:description', ns) is not None else None

                interactions_data.append({
                    'drugbank_id': drugbank_id,
                    'drug_name': drug_name,
                    'interacting_drug_id': interacting_drug_id,
                    'interacting_drug_name': interacting_drug_name,
                    'description': description
                })

        df_interactions = pd.DataFrame(interactions_data)
        return df_interactions

    df_interactions = create_drug_interactions_dataframe(root, ns)
    print("Drug Interactions DataFrame:")
    print(df_interactions)

    df_interactions.to_csv('podpunkt10.csv', index=False)


# Przykładowe wywołanie funkcji dla zadania 1

zadanie8(root, ns)

