from nose.plugins.attrib import attr
from zodiac import openstack
import unittest2 as unittest
import zodiac.config
from zodiac.utils.data_utils import data_gen

class ServerDetailsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.os = openstack.Manager()
        cls.client = cls.os.servers_client
        cls.config = zodiac.config.ZodiacConfig()
        cls.image_ref = cls.config.env.image_ref
        cls.flavor_ref = cls.config.env.flavor_ref
        cls.image_ref_alt = cls.config.env.image_ref_alt
        cls.flavor_ref_alt = cls.config.env.flavor_ref_alt
        
        cls.s1_name = data_gen('server')
        resp, server = cls.client.create_server(cls.s1_name, cls.image_ref, 
                                                cls.flavor_ref)
        cls.client.wait_for_server_status(server['id'], 'ACTIVE')
        resp, cls.s1 = cls.client.get_server(server['id'])
        
        cls.s2_name = data_gen('server')
        resp, server = cls.client.create_server(cls.s2_name, cls.image_ref_alt,
                                                cls.flavor_ref)
        cls.client.wait_for_server_status(server['id'], 'ACTIVE')
        resp, cls.s2 = cls.client.get_server(server['id'])
        
        cls.s3_name = data_gen('server')
        resp, server = cls.client.create_server(cls.s3_name, cls.image_ref, 
                                                cls.flavor_ref_alt)
        cls.client.wait_for_server_status(server['id'], 'ACTIVE')
        resp, cls.s3 = cls.client.get_server(server['id'])
        
    @classmethod
    def tearDownClass(cls):
        cls.client.delete_server(cls.s1['id'])
        cls.client.delete_server(cls.s2['id'])
        cls.client.delete_server(cls.s3['id'])
    
    @unittest.skip('Not currently enabled')
    def test_list_servers(self):
        """ All servers for the tenant should be returned """
        resp, body = self.client.list_servers()
        servers = body['servers']
        
        #self.assertTrue(self.s1 in servers)
        #self.assertTrue(self.s2 in servers)
        #self.assertTrue(self.s3 in servers)
        
    @unittest.skip('Not currently enabled')
    def test_list_servers_filter_by_image(self):
        """ Filter the list of servers by image """
        params = {'image' : self.image_ref}
        resp, body = self.client.list_servers(params)
        servers = body['servers']
        
        #self.assertTrue(self.s1 in servers)
        #self.assertTrue(self.s2 not in servers)
        #self.assertTrue(self.s3 in servers)
        
    @unittest.skip('Not currently enabled')
    def test_list_servers_filter_by_flavor(self):
        """ Filter the list of servers by flavor """
        params = {'flavor' : 1}
        self.client.list_servers(params)
          
    @unittest.skip('Not currently enabled')
    def test_list_servers_filter_by_server_name(self):
        """ Filter the list of servers by name """
        params = {'name' : 'clienttest'}
        self.client.list_servers(params)
        
    @unittest.skip('Not currently enabled')
    def test_list_servers_filter_by_server_status(self):
        """ Filter the list of servers by server status """
        params = {'status' : 'active'}
        resp, body = self.client.list_servers(params)    

    def test_list_servers_with_detail(self):
        """ Return a detailed list of all servers """
        resp, body =  self.client.list_servers_with_detail()
        servers = body['servers']
        
        self.assertTrue(self.s1 in servers)
        self.assertTrue(self.s2 in servers)
        self.assertTrue(self.s3 in servers)

    def test_list_servers_detailed_filter_by_image(self):
        """ Filter the detailed list of servers by image """
        params = {'image' : self.image_ref}
        resp, body = self.client.list_servers_with_detail(params)
        servers = body['servers']
        
        self.assertTrue(self.s1 in servers)
        self.assertTrue(self.s2 not in servers)
        self.assertTrue(self.s3 in servers)

    def test_list_servers_detailed_filter_by_flavor(self):
        """ Filter the detailed list of servers by flavor """
        params = {'flavor' : self.flavor_ref_alt}
        resp, body = self.client.list_servers_with_detail(params)  
        servers = body['servers']
        
        self.assertTrue(self.s1 not in servers)
        self.assertTrue(self.s2 not in servers)
        self.assertTrue(self.s3 in servers)
          
    def test_list_servers_detailed_filter_by_server_name(self):
        """ Filter the detailed list of servers by server name """
        params = {'name' : self.s1_name}
        resp, body = self.client.list_servers_with_detail(params)
        servers = body['servers']
        
        self.assertTrue(self.s1 in servers)
        self.assertTrue(self.s2 not in servers)
        self.assertTrue(self.s3 not in servers)
        
    def test_list_servers_detailed_filter_by_server_status(self):
        """ Filter the detailed list of servers by server status """
        params = {'status' : 'active'}
        resp, body = self.client.list_servers_with_detail(params)
        servers = body['servers']
        
        self.assertTrue(self.s1 in servers)
        self.assertTrue(self.s2 in servers)
        self.assertTrue(self.s3 in servers)

    def test_get_server_details(self):
        """ Return the full details of a single server """
        resp, server = self.client.get_server(self.s1['id'])
        
        self.assertEqual(self.s1_name, server['name'])
        self.assertEqual(self.image_ref, server['image']['id'])
        self.assertEqual(str(self.flavor_ref), server['flavor']['id'])