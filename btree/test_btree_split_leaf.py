import os
import random
from unittest import TestCase

from btree.node_encoder import NodeEncoder
from btree.nodes import NodeDecoder, Leaf, Internal
from exceptions.duplicate_key import DuplicateKeyException
from exceptions.page_full import PageFullException
from utils.file_manager import FileManager


class TestBTreeSplitLeaf(TestCase):

    def setUp(self):
        self.__file_name_test = 'test_leaf_956895.db'
        with open(self.__file_name_test, 'w'):
            pass
        self.node_encoder = NodeEncoder()
        self.file_manager = FileManager(self.__file_name_test, self.node_encoder)
        self.node_inst = NodeDecoder(self.file_manager)
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
            self.leaf = self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            x += 1

        saved_node = self.node_inst.seek_node(0)

        self.assertFalse(saved_node.is_leaf)

    def test005_se_splitea_una_hoja_y_su_hijo_derecho_es_una_hoja(self):
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        x = 1
        while x < 14:
            self.leaf = self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            x += 1
        root = self.node_inst.seek_node(0)
        r_node = self.node_inst.seek_node(root.right_child())

        self.assertTrue(r_node.is_leaf)

    def test006_se_splitea_una_hoja_y_contiene_un_hijo_izquierdo_el_cual_es_una_hoja(self):
        self.leaf.insert(60, 'chester', 'fede@sandoval.com')
        x = 1
        while x < 14:
            self.leaf = self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            x += 1
        root = self.node_inst.seek_node(0)

        left_node_key_num_page = list(root.children().items())[0]
        left = self.node_inst.seek_node(left_node_key_num_page[1])
        self.assertTrue(left.is_leaf)

    def test007_se_splitean_hijos_de_un_nodo_interno_y_todos_sus_hijos_siguen_siendo_hojas(self):
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
            self.leaf = self.leaf.insert(x, 'chester', 'fede@sandoval.com')
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
            self.leaf = self.leaf.insert(x, 'chester', 'fede@sandoval.com')
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
            self.leaf = self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            lista_unida_esperada.append([x, 'chester', 'fede@sandoval.com'])
            x += 1
        lista_unida_esperada.append([60, 'chester', 'fede@sandoval.com'])

        root = self.node_inst.seek_node(0)

        num_pages, num_records = root.count_metadata()
        nodes = []
        x = self.file_manager.file_size()
        base = 0
        y = 0
        while x > base:
            nodes.append(self.node_inst.seek_node(y))
            base += 4096
            y +=1

        self.assertEqual(14, num_records)
        self.assertEqual(3, num_pages)

    def test011_se_levanta_una_excepcion_si_insertamos_un_dato_con_clave_existente(self):
        x = 1
        while x < 13:
            self.leaf = self.leaf.insert(x, 'chester', 'fede@sandoval.com')
            x += 1

        root = self.node_inst.seek_node(0)

        with self.assertRaises(DuplicateKeyException):
            root.insert(9, 'f', 'd')

    def test012_un_btree_puede_insertar_datos_desordenados_pero_siempre_tendra_ordenadas_las_claves_de_sus_hojas(self):
        min = 1
        max = 345
        unique_nums = max - min + 1
        lista_numeros_unicos = random.sample(range(min, max + 1), unique_nums)
        random.shuffle(lista_numeros_unicos)

        for x in lista_numeros_unicos:
            self.leaf = self.leaf.insert(x, 'chester', 'fede@sandoval.com')

        root: Internal = self.node_inst.seek_node(0)

        self.assertTrue(self.esta_ordenada(list(root.children())))

    @staticmethod
    def esta_ordenada(lista):
        for i in range(len(lista) - 1):
            if lista[i] > lista[i + 1]:
                return False
        return True

    def tearDown(self):
        os.remove(self.__file_name_test)
