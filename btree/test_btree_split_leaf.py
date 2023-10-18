import os
from unittest import TestCase

from btree.node_encoder import NodeEncoder
from btree.nodes import NodeInstanciator, Leaf, Internal
from exceptions.page_full import PageFullException
from utils.file_manager import FileManager


class TestBTreeSplitLeaf(TestCase):

    def setUp(self):
        self.__file_name_test = 'test_leaf_956895.db'
        with open(self.__file_name_test, 'w'):
            pass
        self.node_encoder = NodeEncoder()
        self.file_manager = FileManager(self.__file_name_test, self.node_encoder)
        self.node_inst = NodeInstanciator(self.file_manager)
        self.leaf = self.node_inst.create_tree()
        self.file_manager.save(self.leaf)

    def test001_una_hoja_sabe_que_lo_es(self):
        self.assertTrue(self.leaf.is_leaf)

    def test002_una_hoja_root_comienza_sin_registros(self):
        self.assertTrue(self.leaf.is_root)
        self.assertEqual([], self.leaf.select_all())

    def test003_se_inserta_un_registro(self):
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        saved_leaf = self.node_inst.init_tree()

        self.assertEqual(1, saved_leaf.num_records)
        self.assertEqual(self.leaf.select_all(), saved_leaf.select_all())

    def test004_se_splitea_una_hoja_y_se_convierte_en_interno(self):
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        x = 1
        while x < 14:
            self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            x += 1

        saved_node = self.node_inst.seek_node(0)

        self.assertFalse(saved_node.is_leaf)

    def test005_se_splitea_una_hoja_y_su_hijo_derecho_es_una_hoja(self):
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        x = 1
        while x < 14:
            self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            x += 1
        root = self.node_inst.seek_node(0)
        r_node = self.node_inst.seek_node(root.right_child())

        self.assertTrue(r_node.is_leaf)

    def test006_se_splitea_una_hoja_y_contiene_un_hijo_izquierdo_el_cual_es_una_hoja(self):
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        x = 1
        while x < 14:
            self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            x += 1
        root = self.node_inst.seek_node(0)

        left_node_key_num_page = list(root.children().items())[0]
        left = self.node_inst.seek_node(left_node_key_num_page[1])
        self.assertTrue(left.is_leaf)

    def test007_se_splitean_hijos_de_un_nodo_interno_y_todos_sus_hijos_siguen_siendo_hojas(self):
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        x = 1
        while x < 31:
            self.leaf = self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            x += 1
        root = self.node_inst.seek_node(0)

        children = root.children().values()
        for num_page_child in children:
            child = self.node_inst.seek_node(num_page_child)
            self.assertTrue(child.is_leaf)

    def test008_se_splitea_una_hoja_y_sus_hijos_tienen_los_registros_del_padre_dividos_entre_si_mas_el_que_lleno_a_la_hoja_original(
            self):
        lista_unida_esperada = []
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        x = 1
        while x < 14:
            self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            lista_unida_esperada.append([x, 'chester', 'fede@sandoval.com'])
            x += 1
        lista_unida_esperada.append([60, 'chester', 'fede@sandoval.com'])

        root = self.node_inst.seek_node(0)
        l_node = self.node_inst.seek_node(1)
        r_node = self.node_inst.seek_node(root.right_child())

        l_curr_data = l_node.select_all()
        r_curr_data = r_node.select_all()

        self.assertEqual(7, len(l_node.records))
        self.assertEqual(7, len(r_node.records))
        self.assertEqual(lista_unida_esperada[:7], l_curr_data)
        self.assertEqual(lista_unida_esperada[7:], r_curr_data)

    def test009_se_puede_obtener_los_registros_de_todo_el_btree(self):
        lista_unida_esperada = []
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        x = 1
        while x < 14:
            self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            lista_unida_esperada.append([x, 'chester', 'fede@sandoval.com'])
            x += 1
        lista_unida_esperada.append([60, 'chester', 'fede@sandoval.com'])

        root = self.node_inst.seek_node(0)

        curr_lista = root.select_all()

        self.assertEqual(14, len(curr_lista))
        self.assertEqual(lista_unida_esperada, curr_lista)

    def test010_se_puede_obtener_la_cantidad_de_registros_de_un_btree(self):
        lista_unida_esperada = []
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        x = 1
        while x < 14:
            self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            lista_unida_esperada.append([x, 'chester', 'fede@sandoval.com'])
            x += 1
        lista_unida_esperada.append([60, 'chester', 'fede@sandoval.com'])

        root = self.node_inst.seek_node(0)

        num_pages, num_records = root.count_metadata()

        self.assertEqual(14, num_records)
        self.assertEqual(3, num_pages)

    def test011_se_levanta_una_excepcions_si_un_nodo_interno_debe_splitearse(self):
        self.leaf = Internal(True, 0, 0, dict(), 0, 0, self.file_manager, 0)

        with self.assertRaises(PageFullException):
            self.leaf.insert(1, 'f', 'd')

    def tearDown(self):
        os.remove(self.__file_name_test)
