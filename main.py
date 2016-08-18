###################################################################################################
#!/usr/bin/env python                                                                             #
#                                                                                                 #
# Copyright 2007 Google Inc.                                                                      #
#                                                                                                 #
# Licensed under the Apache License, Version 2.0 (the "License");                                 #
# you may not use this file except in compliance with the License.                                #
# You may obtain a copy of the License at                                                         #
#                                                                                                 #
#     http://www.apache.org/licenses/LICENSE-2.0                                                  #
#                                                                                                 #
# Unless required by applicable law or agreed to in writing, software                             #
# distributed under the License is distributed on an "AS IS" BASIS,                               #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                        #
# See the License for the specific language governing permissions and                             #
# limitations under the License.                                                                  #
###################################################################################################

from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from protorpc import messages
from protorpc import remote
from protorpc import message_types

###################################################################################################

class Item(messages.Message):
    name = messages.StringField(1, required=True)
    
class ItemList(messages.Message):
    items = messages.MessageField(Item, 1, repeated=True)
    items_bought = messages.MessageField(Item, 2, repeated=True)
    
###################################################################################################
    
class ShoppingList(ndb.Model):
    user = ndb.StringProperty(required=True)
    items = ndb.StringProperty(repeated=True)
    items_bought = ndb.StringProperty(repeated=True)
    
class FavMarket(ndb.Model):
    user = ndb.StringProperty(required=True)
    ids = ndb.StringProperty(repeated=True)

###################################################################################################

@endpoints.api(name='shoppingList', version='v1')
class ShoppingListApi(remote.Service):

    @endpoints.method(ItemList, ItemList,
                      name='Item.insert',
                      path='Item',
                      http_method='POST')
    def insert_itemlist(self, request):
        # DEBUG
        if not endpoints.get_current_user().user_id():
            user_id = '123456789'
        else:
            user_id = endpoints.get_current_user().user_id()
    
        query = ShoppingList.query(ShoppingList.user == user_id).get()
    
        items = [item.name for item in request.items] 
        items_bought = [item.name for item in request.items_bought]
    
        if query:
            query.items = items
            query.items_bought = items_bought
            query.put()
        else:
            ShoppingList(user=user_id, items=items, items_bought=items_bought).put()
            
        return request
            
    @endpoints.method(message_types.VoidMessage, ItemList,
                      name='Item.get',
                      path='Item',
                      http_method='GET')
    def list_itemlist(self, request):
        # DEBUG
        if not endpoints.get_current_user().user_id():
            user_id = '123456789'
        else:
            user_id = endpoints.get_current_user().user_id()
    
        query = ShoppingList.query(ShoppingList.user == user_id).get()
        items = []
        items_bought = []
        
        if not query:
            return ItemList(items=[], items_bought=[])
        
        for item in query.items:
            items.append(Item(name=item))
            
        for item_bought in query.items_bought:
            items_bought.append(Item(name=item_bought))
        
        return ItemList(items=items, items_bought = items_bought)
        
        
@endpoints.api(name='favMarket', version='v1')
class FavMarketApi(remote.Service):
    
    @endpoints.method(Markets, Markets,
                      name='FavMarket.insert',
                      path='FavMarket',
                      http_method='POST')
    def insert_favMarket(self, request):
        # DEBUG
        if not endpoints.get_current_user().user_id():
            user_id = '123456789'
        else:
            user_id = endpoints.get_current_user().user_id()
    
        query = FavMarket.query(FavMarket.user == user_id).get()
    
        ids = [id for id in request.ids]
    
        if query:
            query.ids = ids
            query.put()
        else:      
            FavMarket(user=user_id, ids=ids).put()
            
        return request
        
    @endpoints.method(message_types.VoidMessage, Markets,
                      name='FavMarket.get',
                      path='FavMarket',
                      http_method='GET')
    def list_favMarket(self, request):
        # DEBUG
        if not endpoints.get_current_user().user_id():
            user_id = '123456789'
        else:
            user_id = endpoints.get_current_user().user_id()
    
        query = FavMarket.query(FavMarket.user == user_id).get()
        ids = []
        
        
        if not query:
            return Markets(ids=[])
        
        for id in query.ids:
            ids.append(id)
    
        return Markets(ids=ids)
        
###################################################################################################

application = endpoints.api_server([ShoppingListApi, FavMarketApi])
