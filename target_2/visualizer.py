import sys
import argparse
import requests
import zipfile
import os
from io import BytesIO
from graphviz import Digraph


# Функция для скачивания .nupkg файла
def download_nupkg(url):
    response = requests.get(url)
    response.raise_for_status()
    return BytesIO(response.content)


# Функция для извлечения зависимостей из .nupkg
def extract_dependencies(nupkg_file):
    with zipfile.ZipFile(nupkg_file) as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('nuspec'):
                with zip_ref.open(file) as nuspec:
                    dependencies = []
                    for line in nuspec.read().decode('utf-8').splitlines():
                        if '<dependency' in line:
                            dep_name = line.split('id="')[1].split('"')[0]
                            dependencies.append(dep_name)
                    return dependencies
    return []


# Функция для построения графа с помощью graphviz
def build_graph(package_name, dependencies):
    dot = Digraph(comment='Package Dependencies')
    dot.node(package_name, package_name)

    # Используем множество для отслеживания уже добавленных зависимостей
    added_dependencies = set()

    for dep in dependencies:
        if dep not in added_dependencies:
            dot.node(dep, dep)
            dot.edge(package_name, dep)
            added_dependencies.add(dep)

    return dot


# Функция для сохранения графа в файл PNG
def save_graph_as_png(dot, output_path):
    dot.render(output_path, format='png', cleanup=True)
    print(f"Graph successfully saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Visualize .NET package dependencies with a custom visualizer.")
    parser.add_argument('--visualizer_path', type=str, required=True, help='Path to the visualizer executable.')
    parser.add_argument('--package_name', type=str, required=True, help='Name of the .NET package to analyze.')
    parser.add_argument('--output_png_path', type=str, required=True, help='Path to save the PNG file.')
    parser.add_argument('--url', type=str, required=True, help='URL to download the .nupkg file.')

    args = parser.parse_args()



    try:
        nupkg_file = download_nupkg(args.url)
        dependencies = extract_dependencies(nupkg_file)
        graph = build_graph(args.package_name, dependencies)
        save_graph_as_png(graph, args.output_png_path)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

# python visualizer.py --visualizer_path ./visualizer.py --package_name Newtonsoft.Json --output_png_path ./output/output_graph_1 --url https://www.nuget.org/api/v2/package/Newtonsoft.Json/13.0.3
# python visualizer.py --visualizer_path ./visualizer.py --package_name Microsoft.Extensions.DependencyInjection --output_png_path ./output/output_graph_2 --url https://www.nuget.org/api/v2/package/Microsoft.Extensions.DependencyInjection/9.0.0
# python visualizer.py --visualizer_path ./visualizer.py --package_name Azure.Core --output_png_path ./output/output_graph_3 --url https://www.nuget.org/api/v2/package/Azure.Core/1.44.1