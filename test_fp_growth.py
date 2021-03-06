import unittest
from fp_growth import FPTree, FPTreeNode


class FPTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.tree = FPTree()

    def test_insert_transaction(self):
        ''' test if inserting a transaction works or not '''
        items = ['a', 'b', 'c', 'd', 'e']
        self.tree.insert_transaction(items)
        # from IPython.core.debugger import Tracer; Tracer()()
        current = self.tree.root
        counter = 0

        while True:
            try:
                self.assertIn(items[counter], current.children)  # make sure the child is there.
                child = current.get_child(items[counter])
                self.assertEqual(child.count, 1)  # make sure the count is 1
                current = child
                counter += 1
            # these exceptions occur when you reach the last element
            except (KeyError, IndexError):
                break

    def test_insert_two_transactions(self):
        ''' test if inserting two transactions works or not. '''
        first_transaction = ['a', 'b', 'c']
        second_transaction = ['a', 'b', 'd']

        ITEM, CHILDREN, COUNT = range(3)
        expected_result = [
            # item, children, count
            ('a', ('b', ), 2),
            ('b', ('c', 'd'), 2),
            ('c', (), 1),
            ('d', (), 1),
        ]

        self.tree.insert_transaction(first_transaction)
        self.tree.insert_transaction(second_transaction)

        count = 0

        for node in self.tree:
            if node.root:
                continue

            self.assertEqual(node.item, expected_result[count][ITEM])
            self.assertEqual(
                tuple(node.children.keys()), expected_result[count][CHILDREN])
            self.assertEqual(node.count, expected_result[count][COUNT])
            count += 1

    def test_prefix_path(self):
        ''' test if the prefix paths are getting properly generated or not. '''
        self.tree.insert_transaction(['a', 'b', 'c'])
        self.tree.insert_transaction(['a', 'd', 'c'])

        prefix_paths = self.tree.prefix_path('c')
        paths = [[node.item for node in path] for path in prefix_paths]
        self.assertEquals(paths, [['b', 'a'], ['d', 'a']])

    def test_header_pointers(self):
        '''
        test if the header pointers are getting created properly
        '''
        transaction = ['a', 'b', 'c', 'd']
        self.tree.insert_transaction(transaction)
        nodes = [node for node in self.tree]
        for key, value in self.tree._headers.iteritems():
            self.assertIn(key, transaction)
            self.assertIn(value, nodes)

    def test_headers(self):
        ''' test if the headers iterator is working properly or not. '''
        transaction = ['a', 'b', 'c']
        self.tree.insert_transaction(transaction)
        headers = [header.item for header in self.tree.headers]
        self.assertEqual(headers, ['c', 'b', 'a'])

    def test_linked_list_pointers(self):
        ''' test if the linked list pointers are getting properly
        initialized or not '''
        transaction_1 = ['a', 'b']
        transaction_2 = ['b', 'a']
        self.tree.insert_transaction(transaction_1)
        self.tree.insert_transaction(transaction_2)

        # make sure the `next` of the first item points to the last element.
        self.assertEqual(self.tree._headers['a'].neighbor, self.tree._latest_ptr['a'])
        self.assertEqual(self.tree._headers['b'].neighbor, self.tree._latest_ptr['b'])


class FPTreeNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.node = FPTreeNode()

    def test_node_creation(self):
        ''' test if the normal node is being created properly '''
        node = FPTreeNode('item')
        self.assertFalse(node._root)  # is not a root node
        self.assertEqual(node.count, 1)  # the count is 1
        self.assertEqual(node.item, 'item')

    def test_root_node_creation(self):
        ''' test if the root node is being created properly '''
        node = FPTreeNode()
        self.assertTrue(node._root)  # is a root node
        self.assertEqual(node.count, 0)  # the count is 0

    def test_has_child(self):
        ''' test if the has_child is working as expected '''
        self.node.add_child('item1')
        self.assertTrue(self.node.has_child('item1'))
        self.assertFalse(self.node.has_child('item2'))

    def test_get_child(self):
        ''' test if the get_child is working properly or not. '''
        child_node = self.node.add_child('child_node')
        other_child_node = self.node.get_child('child_node')
        self.assertEqual(child_node, other_child_node)

    def test_get_child_invalid(self):
        ''' test if the get_child is raises an exception when child is absent '''
        with self.assertRaises(KeyError):
            self.node.get_child('item1')

    def test_add_child(self):
        ''' test if add_child is working properly or not. '''
        self.node.add_child('child')
        self.assertTrue(self.node.has_child('child'))

    def test_add_child_existing(self):
        ''' test add_child when the child is already present. '''
        self.node.add_child('child')
        with self.assertRaises(ValueError):
            self.node.add_child('child')


if __name__ == '__main__':
    unittest.main()
