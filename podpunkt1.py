import pandas as pd
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
import requests
import random

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

    df_drug_info.to_csv('drug_info.csv', index=False)


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

    df_synonyms.to_csv('drug_synonyms.csv', index=False)

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

    df_products.to_csv('products.csv', index=False)


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

    df_pathways.to_csv('pathways.csv', index=False)

def zadanie5(root, ns):
    def create_pathway_interactions_dataframe(root, ns):
        interactions_data = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find('db:drugbank-id[@primary="true"]', ns) is not None else None
            drug_name = drug.find('db:name', ns).text if drug.find('db:name', ns) is not None else None
            for pathway in drug.findall('db:pathways/db:pathway', ns):
                pathway_id = pathway.find('db:smpdb-id', ns).text if pathway.find('db:smpdb-id', ns) is not None else None
                pathway_name = pathway.find('db:name', ns).text if pathway.find('db:name', ns) is not None else None
                pathway_category = pathway.find('db:category', ns).text if pathway.find('db:category', ns) is not None else None

                interactions_data.append({
                    'drugbank_id': drugbank_id,
                    'drug_name': drug_name,
                    'pathway_id': pathway_id,
                    'pathway_name': pathway_name,
                    'pathway_category': pathway_category
                })

        df_interactions = pd.DataFrame(interactions_data)
        return df_interactions

    df_interactions = create_pathway_interactions_dataframe(root, ns)
    print("Pathway Interactions DataFrame:")
    print(df_interactions)

    df_interactions.to_csv('pathway_interactions.csv', index=False)

    def draw_bipartite_graph(df_interactions):
        B = nx.Graph()

        for _, row in df_interactions.iterrows():
            B.add_node(row['drug_name'], bipartite=0)
            B.add_node(row['pathway_name'], bipartite=1)
            B.add_edge(row['drug_name'], row['pathway_name'])

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(B, k=0.5)
        drug_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}
        pathway_nodes = set(B) - drug_nodes

        nx.draw_networkx_nodes(B, pos, nodelist=drug_nodes, node_color="lightblue", node_size=500, label="Drugs")
        nx.draw_networkx_nodes(B, pos, nodelist=pathway_nodes, node_color="lightgreen", node_size=500, label="Pathways")
        nx.draw_networkx_edges(B, pos, edgelist=B.edges(), edge_color="gray")
        nx.draw_networkx_labels(B, pos, font_size=10, font_weight="bold")

        plt.title("Bipartite Graph of Drug-Pathway Interactions")
        plt.legend(loc="best")
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

    df_counts.to_csv('drug_pathway_counts.csv', index=False)

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
        protein_data = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find('db:drugbank-id[@primary="true"]', ns) is not None else None
            for target in drug.findall('db:targets/db:target', ns):
                protein_info = {
                    'drugbank_id': drugbank_id,
                    'target_id': target.find('db:id', ns).text if target.find('db:id', ns) is not None else None,
                    'source': target.find('db:external-identifiers/db:external-identifier/db:resource', ns).text if target.find('db:external-identifiers/db:external-identifier/db:resource', ns) is not None else None,
                    'external_id': target.find('db:external-identifiers/db:external-identifier/db:identifier', ns).text if target.find('db:external-identifiers/db:external-identifier/db:identifier', ns) is not None else None,
                    'polypeptide_name': target.find('db:polypeptide/db:name', ns).text if target.find('db:polypeptide/db:name', ns) is not None else None,
                    'gene_name': target.find('db:polypeptide/db:gene-name', ns).text if target.find('db:polypeptide/db:gene-name', ns) is not None else None,
                    'genatlas_id': target.find('db:polypeptide/db:genatlas-id', ns).text if target.find('db:polypeptide/db:genatlas-id', ns) is not None else None,
                    'chromosome': target.find('db:polypeptide/db:chromosome', ns).text if target.find('db:polypeptide/db:chromosome', ns) is not None else None,
                    'cellular_location': target.find('db:polypeptide/db:cellular-location', ns).text if target.find('db:polypeptide/db:cellular-location', ns) is not None else None
                }
                protein_data.append(protein_info)

        df_proteins = pd.DataFrame(protein_data)
        return df_proteins

    df_proteins = create_protein_interactions_dataframe(root, ns)
    print("Protein Interactions DataFrame:")
    print(df_proteins)

    df_proteins.to_csv('protein_interactions.csv', index=False)

def zadanie8(root, ns):
    def create_cellular_location_dataframe(root, ns):
        location_data = []

        for drug in root.findall('db:drug', ns):
            for target in drug.findall('db:targets/db:target', ns):
                cellular_location = target.find('db:polypeptide/db:cellular-location', ns).text if target.find('db:polypeptide/db:cellular-location', ns) is not None else 'Unknown'
                location_data.append(cellular_location)

        df_locations = pd.DataFrame(location_data, columns=['cellular_location'])
        return df_locations

    df_locations = create_cellular_location_dataframe(root, ns)
    print("Cellular Locations DataFrame:")
    print(df_locations)

    df_counts = df_locations['cellular_location'].value_counts()
    print("Cellular Location Counts:")
    print(df_counts)

    def plot_pie_chart(df_counts):
        plt.figure(figsize=(10, 7))
        plt.pie(df_counts, labels=df_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
        plt.title('Percentage Occurrence of Targets in Different Cellular Locations')
        plt.axis('equal')
        plt.show()

    plot_pie_chart(df_counts)


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

    df_interactions.to_csv('drug_interactions.csv', index=False)


def zadanie11(root, ns, specific_gene=None):
    def create_gene_interactions_dataframe(root, ns):
        interactions_data = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            drug_name = drug.find('db:name', ns).text if drug.find('db:name', ns) is not None else None

            for target in drug.findall('db:targets/db:target', ns):
                gene_name = target.find('db:polypeptide/db:gene-name', ns).text if target.find(
                    'db:polypeptide/db:gene-name', ns) is not None else None

                for product in drug.findall('db:products/db:product', ns):
                    product_name = product.find('db:name', ns).text if product.find('db:name', ns) is not None else None

                    interactions_data.append({
                        'drugbank_id': drugbank_id,
                        'drug_name': drug_name,
                        'gene_name': gene_name,
                        'product_name': product_name
                    })

        df_interactions = pd.DataFrame(interactions_data)
        return df_interactions

    df_interactions = create_gene_interactions_dataframe(root, ns)
    print("Gene Interactions DataFrame:")
    print(df_interactions)

    if specific_gene:
        df_interactions = df_interactions[df_interactions['gene_name'] == specific_gene]

    def draw_interaction_graph(df_interactions):
        G = nx.Graph()

        for _, row in df_interactions.iterrows():
            G.add_node(row['gene_name'], bipartite=0, color='lightcoral')
            G.add_node(row['drug_name'], bipartite=1, color='lightblue')
            G.add_node(row['product_name'], bipartite=2, color='lightgreen')
            G.add_edge(row['gene_name'], row['drug_name'])
            G.add_edge(row['drug_name'], row['product_name'])

        pos = nx.spring_layout(G, k=0.5)
        colors = [G.nodes[n]['color'] for n in G.nodes]

        plt.figure(figsize=(15, 10))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color=colors, font_size=10, font_weight='bold',
                edge_color='gray')
        plt.title('Gene-Drug-Product Interactions')
        plt.show()

    draw_interaction_graph(df_interactions)


def fetch_uniprot_data(protein_id):
    """
    Pobiera dane XML z UniProt dla danego identyfikatora białka.
    """
    url = f"https://www.uniprot.org/uniprot/{protein_id}.xml"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None


def parse_uniprot_data(xml_data):
    """
    Parsuje dane XML z UniProt, aby wyodrębnić informacje o funkcji i lokalizacji komórkowej białka.
    """
    root = ET.fromstring(xml_data)
    namespace = {'ns': 'http://uniprot.org/uniprot'}

    function = root.find('.//ns:comment[@type="function"]/ns:text', namespace)
    location = root.find('.//ns:subcellularLocation/ns:location', namespace)

    function_text = function.text if function is not None else 'Unknown'
    location_text = location.text if location is not None else 'Unknown'

    return function_text, location_text


def zadanie12(root, ns):
    """
    Tworzy ramkę danych zawierającą informacje o białkach (targetach) leków, funkcjach biologicznych oraz lokalizacji komórkowej. Prezentuje dane w formie wykresów.
    """

    def create_protein_info_dataframe(root, ns):
        """
        Tworzy ramkę danych zawierającą informacje o białkach, funkcjach biologicznych oraz lekach, które z nimi wchodzą w interakcje.
        """
        protein_data = []

        for drug in root.findall('db:drug', ns):
            drugbank_id = drug.find('db:drugbank-id[@primary="true"]', ns).text if drug.find(
                'db:drugbank-id[@primary="true"]', ns) is not None else None
            drug_name = drug.find('db:name', ns).text if drug.find('db:name', ns) is not None else None

            for target in drug.findall('db:targets/db:target', ns):
                protein_id = target.find(
                    'db:polypeptide/db:external-identifiers/db:external-identifier[db:resource="UniProtKB"]/db:identifier',
                    ns).text if target.find(
                    'db:polypeptide/db:external-identifiers/db:external-identifier[db:resource="UniProtKB"]/db:identifier',
                    ns) is not None else None
                if protein_id:
                    xml_data = fetch_uniprot_data(protein_id)
                    if xml_data:
                        function_text, location_text = parse_uniprot_data(xml_data)

                        protein_data.append({
                            'drugbank_id': drugbank_id,
                            'drug_name': drug_name,
                            'protein_id': protein_id,
                            'function': function_text,
                            'location': location_text
                        })

        df_protein_info = pd.DataFrame(protein_data)
        return df_protein_info

    # Tworzenie ramki danych z informacjami o białkach
    df_protein_info = create_protein_info_dataframe(root, ns)
    print("Protein Info DataFrame:")
    print(df_protein_info)

    # Zapisanie ramki danych do pliku CSV
    df_protein_info.to_csv('protein_info.csv', index=False)

    def plot_function_distribution(df_protein_info):
        """
        Tworzy wykres słupkowy przedstawiający rozkład funkcji biologicznych białek.
        """
        function_counts = df_protein_info['function'].value_counts()

        plt.figure(figsize=(15, 10))
        function_counts.plot(kind='bar')
        plt.xlabel('Function')
        plt.ylabel('Count')
        plt.title('Distribution of Protein Functions')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def plot_location_distribution(df_protein_info):
        """
        Tworzy wykres kołowy przedstawiający rozkład lokalizacji komórkowej białek.
        """
        location_counts = df_protein_info['location'].value_counts()

        plt.figure(figsize=(10, 7))
        plt.pie(location_counts, labels=location_counts.index, autopct='%1.1f%%', startangle=140,
                colors=plt.cm.tab20.colors)
        plt.title('Distribution of Protein Cellular Locations')
        plt.axis('equal')
        plt.show()

    # Tworzenie wykresów
    plot_function_distribution(df_protein_info)
    plot_location_distribution(df_protein_info)


# Przykładowe wywołanie funkcji dla zadania 1
# zadanie1(root, ns)
