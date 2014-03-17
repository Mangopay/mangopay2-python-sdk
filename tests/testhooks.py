import unittest
from tests.testbase import TestBase
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.entities.hook import Hook

class Test_Hooks(TestBase):
    """Test methods for hooks."""


    def test_Hooks_Create(self):
        hook = self.getJohnHook()
        self.assertTrue(hook.Id > 0);
    
    def test_Hooks_Get(self):
        hook = self.getJohnHook()
        getHook = self.sdk.hooks.Get(hook.Id)
        self.assertEqual(getHook.Id, hook.Id)
    
    def test_Hooks_Update(self):
        hook = self.getJohnHook()
        hook.Url = 'http://test123.com'
        
        saveHook = self.sdk.hooks.Update(hook)
        
        self.assertEqual(saveHook.Id, hook.Id)
        self.assertEqual(saveHook.Url, 'http://test123.com')
    
    def test_Hooks_All(self):
        hook = self.getJohnHook()
        pagination = Pagination(1, 1)
        
        list = self.sdk.hooks.GetAll(pagination)
        
        self.assertTrue(isinstance(list[0], Hook))
        self.assertEqual(hook.Id, list[0].Id)
        self.assertEqual(pagination.Page, 1)
        self.assertEqual(pagination.ItemsPerPage, 1)