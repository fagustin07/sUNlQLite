from unittest import TestCase

from btree.node import Node
from exceptions.duplicate_key import DuplicateKeyException
from exceptions.page_full import PageFullException


class TestNode(TestCase):
    def test_comienza_sin_registros(self):
        node = Node(True, True, None, 0, 1, [], 3)
        self.assertEqual([], node.data())

    def test_se_inserta_un_registro(self):
        pk1 = 10
        node = Node(True, True, None, 0, 1, [], 3)
        node.insert(pk1, 'fede', 'rico')

        self.assertEqual(node.get_pk(pk1), pk1)
        self.assertEqual(node.get_username(pk1), 'fede')
        self.assertEqual(node.get_email(pk1), 'rico')
        self.assertEqual(1, node.num_records)

    def test_cuando_se_splitea_una_hoja_el_numrecords_pasa_a_ser_la_cantidad_de_hijos(self):
        pk1 = 10
        pk2 = 45
        pk3 = 1
        pk4 = 8
        node = Node(True, True, None, 0, 1, [], 3)
        node.insert(pk1, 'fede1', 'rico1')
        node.insert(pk2, 'fede2', 'rico2')
        node.insert(pk3, 'fede3', 'rico3')
        node.insert(pk4, 'fede4', 'rico4')

        self.assertEqual(2, node.num_records)
        self.assertEqual(1, len(node.subtrees))

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
        self.assertEqual(6, node.count_records())

    def test_obtener_registros_desde_un_nodo_interno(self):
        pk1 = 10
        pk2 = 45
        node = Node(True, True, None, 0, 1, [], 1)
        node.insert(pk1, 'fede1', 'rico1')
        node.insert(pk2, 'fede2', 'rico2')

        self.assertFalse(node.is_leaf)
        self.assertEqual([[10, 'fede1', 'rico1'], [45, 'fede2', 'rico2']], node.data())

    def test_un_nodo_hoja_que_no_es_root_puede_splitearse_y_todos_los_subarboles_tienen_al_mismo_padre(self):
        pk1 = 10
        pk2 = 45
        node = Node(True, True, None, 0, 1, [], 1)
        node.insert(pk1, 'fede1', 'rico1')
        node.insert(pk2, 'fede2', 'rico2')
        node.insert(5, 'fede3', 'rico3')
        node.insert(16, 'fede4', 'rico4')

        self.assertTrue(all(subtree.parent == node for subtree in node.nodes_subtrees()))

    def test_un_nodo_hoja_que_no_es_root_puede_splitearse(self):
        pk1 = 10
        pk2 = 45
        node = Node(True, True, None, 0, 1, [], 1)
        node.insert(pk1, 'fede1', 'rico1')
        node.insert(pk2, 'fede2', 'rico2')
        node.insert(5, 'fede3', 'rico3')
        node.insert(16, 'fede4', 'rico4')

        self.assertEqual(5, node.count_pages())

    def test_desde_root_se_pueden_obtener_todos_los_registros(self):
        node = Node(True, True, None, 0, 1, [], 1)
        registros_a_insertar = [[23, 'fede1', 'rico1'], [44, 'fede1', 'rico1'], [10000, 'fede1', 'rico1'],
                                [323, 'fede1', 'rico1']]
        for record in registros_a_insertar:
            node.insert(record[0], record[1], record[2])

        self.assertEqual(sorted(registros_a_insertar, key=lambda record: record[0]), node.data())

    def test_desde_root_se_levanta_una_excepcion_al_querer_insertar_una_key_duplicada(self):
        node = Node(True, True, None, 0, 1, [], 1)
        registro = [23, 'fede1', 'rico1']
        node.insert(registro[0], registro[1], registro[2])
        with self.assertRaises(DuplicateKeyException):
            node.insert(registro[0], registro[1], registro[2])

    def test_se_levanta_una_excepcion_al_llenar_los_subhijos_de_un_nodo_interno_por_no_estar_implementado(self):
        node = Node(True, True, None, 0, 1, [], 1)
        curr = 0
        while curr < 511:
            curr += 1
            node.insert(curr, 'fede', 'feeee')

        with self.assertRaises(PageFullException):
            node.insert(9999, 'fede', 'feeee')
