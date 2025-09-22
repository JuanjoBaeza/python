import json

# Datos sintéticos corregidos (sin coma al final del JSON)
data_file = """
[
        {
            "id": 1,
            "name": "Elemento 1",
            "tags": ["python", "C#"]
        },
        {
            "id": 2,
            "name": "Elemento 2",
            "tags": ["java", "web"]
        },
        {
            "id": 3,
            "name": "Elemento 3",
            "tags": ["python", "Go"]
        },
        {
            "id": 4,
            "name": "Elemento 4",
            "tags": ["javascript", "C++"]
        },
        {
            "id": 5,
            "name": "Elemento 5"
        }
]
"""

query_tag = "python"

class NoResultsFound(Exception):
    """Excepción personalizada para cuando no hay resultados."""
    pass

class SearchByTag:

    def __init__(self, data_file, query_tag):
        self.data_file = data_file
        self.query_tag = query_tag

    def search(self):
        try:
            data = json.loads(self.data_file)
        except json.JSONDecodeError:
            return iter([])  # iterador vacío si JSON no es válido

        if not isinstance(data, list):
            return iter([])

        # Generador que devuelve solo los elementos con el tag
        for item in data:
            if "tags" in item and self.query_tag in item["tags"]:
                yield item

    def first(self):
        generator = self.search()
        try:
            return next(generator)
        except StopIteration:
            raise StopIteration("No se ha encontrado ningún elemento")


searcher = SearchByTag(data_file, query_tag)

print("Resultados con la tag 'python':")
for result in searcher.search():
    print(result)

print("\nPrimer resultado con la tag 'python':")
try:
    print(searcher.first())
except NoResultsFound as e:
    print(e)