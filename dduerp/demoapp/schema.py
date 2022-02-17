import email
import graphene
from graphene_django import DjangoObjectType
from .models import User

class UserTyoe(DjangoObjectType):
    class Meta:
        model=User
        fiels={
            'email',
            'password',
            'firstName',
            'lastName',
        }

class Query(graphene.ObjectType):
    users=graphene.List(UserTyoe)
    
    def resolve_users(root,info,**kwargs):
        return User.objects.all()

schema = graphene.Schema(query=Query)