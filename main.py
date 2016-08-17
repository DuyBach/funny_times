#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from protorpc import messages
from protorpc import remote
from protorpc import message_types
import logging

class Item(messages.Message):
    name = messages.StringField(1, required=True)
    
class User(messages.Message):
    name = messages.StringField(1, required=True)
    
class ItemList(messages.Message):
    user = messages.MessageField(User, 1, required=True)
    items = messages.MessageField(Item, 2, repeated=True)

class ShoppingList(ndb.Model):
    user = ndb.StringProperty(required=True)
    items = ndb.StringProperty(repeated=True)

@endpoints.api(name='shoppingList', version='v1')
class ShoppingListApi(remote.Service):

    @endpoints.method(ItemList, ItemList,
                      name='Item.insert',
                      path='Item',
                      http_method='POST')
    def insert_task(self, request):
        query = ShoppingList.query(ShoppingList.user == request.user).get()
    
        test_list = [item.name for item in request.items]  
    
        if query:
            query.items = test_list
            query.put()
        else:      
            ShoppingList(user=request.user, items=test_list).put()
            
    @endpoints.method(User, ItemList,
                      name='Item.get',
                      path='Item',
                      http_method='GET')
    def list_task(self, request):
        query = ShoppingList.query(ShoppingList.user == request.name).get()
        items = []
        for item in query.items:
            items.append(Item(name=item))
        
        return ItemList(user=User(name=query.user), items=items)

application = endpoints.api_server([ShoppingListApi])
