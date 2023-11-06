import os
import random
from unittest import TestCase

from btree.node_encoder import NodeEncoder
from btree.nodes import NodeDecoder, Leaf, Internal
from exceptions.duplicate_key import DuplicateKeyException
from exceptions.page_full import PageFullException
from utils.file_manager import FileManager


class TestBTreeSplitInternal(TestCase):

    def setUp(self):
        self.__file_name_test = 'test_leaf_956895.db'
        with open(self.__file_name_test, 'w'):
            pass
        self.node_encoder = NodeEncoder()
        self.file_manager = FileManager(self.__file_name_test, self.node_encoder)
        self.node_inst = NodeDecoder(self.file_manager, 2, 8)
        self.node = self.node_inst.create_tree()
        self.file_manager.save(self.node)

    def test01_un_nodo_interno_que_se_splitea_mantiene_su_arbol_y_los_registros(self):
        self.node = self.node.insert(66, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(10, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(22, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(33, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(77, 'chester', 'fede@sandoval.com')
        self.node = self.node.insert(1, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(12, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(21, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(111, 'chester', 'fede@sandoval.com')
        self.node = self.node.insert(90, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(76, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(55, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(43, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(91, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(100, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(2, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(5, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(14, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(15, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(29, 'chester', 'fede@sandoval.com') #
        self.node = self.node.insert(34, 'chester', 'fede@sandoval.com') #

        nodes = []

        x = self.file_manager.file_size()
        base = 0
        y = 0
        while x > base:
            z = self.node_inst.seek_node(y)
            nodes.append(z)
            base += 4096
            y += 1

        self.assertEqual(self.node.count_metadata()[1], 21)

    def test02_un_btree_puede_insertar_datos_desordenados_pero_mantendra_el_orden_de_sus_hijos(self):
        self.node_inst = NodeDecoder(self.file_manager, 13, 20)
        self.node = self.node_inst.create_tree()
        self.file_manager.save(self.node)
        min = 1
        max = 491
        unique_nums = max - min + 1
        lista_numeros_unicos = random.sample(range(min, max + 1), unique_nums)
        random.shuffle(lista_numeros_unicos)

        for x in lista_numeros_unicos:
            self.node = self.node.insert(x, 'chester', 'fede@sandoval.com')


        nodes = []
        file_size = self.file_manager.file_size()
        base = 0
        curr_index = 0
        while file_size > base:
            curr_node = self.node_inst.seek_node(curr_index)
            if not curr_node.is_leaf:
                nodes.append(curr_node)
            base += 4096
            curr_index += 1

        for internal_node in nodes:
            self.assertTrue(self.esta_ordenada(list(internal_node.children())))

        self.assertEqual(self.node.count_metadata()[1], 491)
        self.assertEqual(len(self.node_inst.seek_node(0).select_all()), 491)

    def test03_un_btree_puede_insertar_datos_desordenados_pero_si_se_quiere_insertar_un_duplicado_se_levanta_excepcion(self):
        self.node_inst = NodeDecoder(self.file_manager, 13, 40)
        self.node = self.node_inst.create_tree()
        self.file_manager.save(self.node)
        min = 1
        max = 500
        unique_nums = max - min + 1
        lista_numeros_unicos = random.sample(range(min, max + 1), unique_nums)
        random.shuffle(lista_numeros_unicos)

        for x in lista_numeros_unicos:
            self.node = self.node.insert(x, 'chester', 'fede@sandoval.com')

        with self.assertRaises(DuplicateKeyException):
            self.node.insert(lista_numeros_unicos[0], 'f', 'd')

    @staticmethod
    def esta_ordenada(lista):
        for i in range(len(lista) - 1):
            if lista[i] > lista[i + 1]:
                return False
        return True

    def tearDown(self):
        os.remove(self.__file_name_test)
