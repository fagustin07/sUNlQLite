from unittest import TestCase

from btree.node import Node


class TestNode(TestCase):
    def test_comienza_sin_registros(self):
        node = Node(True, True, None, 0, 1, [], 3)
        self.assertEqual(node.data(), [])

    def test_se_inserta_un_registro(self):
        pk1 = 10
        node = Node(True, True, None, 0, 1, [], 3)
        node.insert(pk1, 'fede', 'rico')

        self.assertEqual(node.get_pk(pk1), pk1)
        self.assertEqual(node.get_username(pk1), 'fede')
        self.assertEqual(node.get_email(pk1), 'rico')
        self.assertEqual(node.num_records, 1)

    def test_se_splitea_una_hoja(self):
        pk1 = 10
        pk2 = 45
        pk3 = 1
        pk4 = 8
        node = Node(True, True, None, 0, 1, [], 3)
        node.insert(pk1, 'fede1', 'rico1')
        node.insert(pk2, 'fede2', 'rico2')
        node.insert(pk3, 'fede3', 'rico3')
        node.insert(pk4, 'fede4', 'rico4')

        self.assertEqual(node.num_records, 0)

    def test_obtener_cantidad_de_registros_desde_un_nodo_interno(self):
        pk1 = 10
        pk2 = 45
        pk3 = 1
        pk4 = 8
        node = Node(True, True, None, 0, 1, [], 5)
        node.insert(pk1, 'fede1', 'rico1')
        node.insert(pk2, 'fede2', 'rico2')
        node.insert(pk3, 'fede3', 'rico3')
        node.insert(pk4, 'fede4', 'rico4')
        node.insert(33, 'fede9', 'rico9')
        node.insert(22, 'fede68', 'rico8')

        self.assertFalse(node.is_leaf)
        self.assertEqual(node.count_records(), 6)

    def test_obtener_registros_desde_un_nodo_interno(self):
        pk1 = 10
        pk2 = 45
        node = Node(True, True, None, 0, 1, [], 1)
        node.insert(pk1, 'fede1', 'rico1')
        node.insert(pk2, 'fede2', 'rico2')

        self.assertFalse(node.is_leaf)
        self.assertEqual(node.data(), [[10, 'fede1', 'rico1'], [45, 'fede2', 'rico2']])
