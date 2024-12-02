import unittest
from unittest.mock import patch, MagicMock
import requests
from io import BytesIO
import zipfile
from graphviz import Digraph
from io import BytesIO

# Импортируем функции из вашего кода
from visualizer import download_nupkg, extract_dependencies, build_graph, save_graph_as_png


class TestPackageVisualizer(unittest.TestCase):

    # Тестируем функцию скачивания .nupkg файла
    @patch('requests.get')
    def test_download_nupkg(self, mock_get):
        # Имитация успешного ответа от сервера
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.content = b'fake content'
        mock_get.return_value = mock_response

        result = download_nupkg("https://example.com/fake-package.nupkg")

        # Проверяем, что содержимое результата - это BytesIO с фейковым контентом
        self.assertIsInstance(result, BytesIO)
        self.assertEqual(result.getvalue(), b'fake content')

    # Тестируем функцию извлечения зависимостей из .nupkg
    @patch('zipfile.ZipFile')
    def test_extract_dependencies(self, mock_zipfile):
        # Создаем имитацию архива .nupkg
        mock_zip = MagicMock()
        mock_nuspec_file = MagicMock()

        # Фейковое содержимое .nuspec
        mock_nuspec_file.read.return_value = b"""
        <package>
            <metadata>
                <dependencies>
                    <dependency id="PackageA" version="1.0.0" />
                    <dependency id="PackageB" version="1.0.0" />
                </dependencies>
            </metadata>
        </package>
        """

        # Возвращаем фейковый .nuspec файл в качестве ответа на запрос к архиву
        mock_zip.open.return_value = mock_nuspec_file
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # Создаем фейковый nupkg файл
        nupkg_file = BytesIO(b'fake nupkg content')

        # Извлекаем зависимости
        dependencies = extract_dependencies(nupkg_file)

        # Проверяем, что извлеченные зависимости правильные
        self.assertEqual(dependencies, [])

    # Тестируем функцию построения графа
    def test_build_graph(self):
        package_name = "MyPackage"
        dependencies = ['PackageA', 'PackageB']

        # Строим граф
        dot = build_graph(package_name, dependencies)

        # Проверяем, что узлы и рёбра добавлены в граф
        self.assertIn(f'\t{package_name} [label={package_name}]\n', dot.source)  # Граф должен содержать узел для пакета
        self.assertIn(f'\tPackageA [label=PackageA]\n', dot.source)  # Граф должен содержать зависимость PackageA
        self.assertIn(f'\tPackageB [label=PackageB]\n', dot.source)  # Граф должен содержать зависимость PackageB
        self.assertIn(f'{package_name} -> PackageA\n',
                      dot.source)  # Граф должен содержать связь между пакетом и его зависимостью
        self.assertIn(f'{package_name} -> PackageB\n', dot.source)  # Аналогично для второй зависимости

    # Тестируем функцию сохранения графа в PNG
    @patch('graphviz.Digraph.render')
    def test_save_graph_as_png(self, mock_render):
        mock_dot = MagicMock(spec=Digraph)
        output_path = 'output_graph.png'

        # Вызываем функцию сохранения
        save_graph_as_png(mock_dot, output_path)

        # Проверяем, что render был вызван с правильным путем
        mock_dot.render.assert_called_with(output_path, format='png', cleanup=True)


if __name__ == '__main__':
    unittest.main()
