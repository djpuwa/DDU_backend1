

import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from .models import Temp, ExtendUser, UserProfile,  UserRole
from graphene_file_upload.scalars import Upload

class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()
   verify_account = mutations.VerifyAccount.Field()
   token_auth = mutations.ObtainJSONWebToken.Field()
   update_account = mutations.UpdateAccount.Field()
#    resend_activation_email = mutations.ResendActivationEmail.Field()
   send_password_reset_email = mutations.SendPasswordResetEmail.Field()
   password_reset = mutations.PasswordReset.Field()
   password_change = mutations.PasswordChange.Field()
   revoke_token = mutations.RevokeToken.Field()
   refresh_token = mutations.RefreshToken.Field()

# models Type
class TempType(DjangoObjectType):
   class Meta:
      model = Temp
      fields=(
         'title',
      )

class ExtendUserTyoe(DjangoObjectType):
    class Meta:
        model=ExtendUser
        fields=(
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'userid',
            'username',
            'role',
        )
    
class UserProfileType(DjangoObjectType):
   class Meta:
      model=UserProfile
      fields=(
         'primaryContact',
         'photo',
         'secondaryContact',
         'currentAdd',
         'currentCity',
         'currentState',
         'permAdd',
         'permCity',
         'permState',
         'altEmail',
         'gender',
         'dob',
         'bloodGroup',
         'user',
      )



class UserRoleType(DjangoObjectType):
   class Meta:
      model = UserRole
      fields=(
         'id',
         'name',
         'description',
      )






# Model Inputs
class UserProfileInput(graphene.InputObjectType):
   primaryContact=graphene.String()
   photo = graphene.String()
   secondaryContact=graphene.String()
   currentAdd=graphene.String()
   currentCity=graphene.String()
   currentState=graphene.String()
   permAdd=graphene.String()
   permCity=graphene.String()
   permState=graphene.String()
   altEmail=graphene.String()
   gender=graphene.String()
   dob=graphene.String()
   bloodGroup=graphene.String()
   user=graphene.String()


class RoleInput(graphene.InputObjectType):
   id=graphene.Int()
   name=graphene.String()
   description = graphene.String()





# User and UserProfile Queries
class CreateUserProfile(graphene.Mutation):
   class Arguments:
      input = UserProfileInput(required=True)

   userProfile = graphene.Field(UserProfileType)

   @classmethod
   def mutate(cls, root, info, input):
      userProfile = UserProfile()
      userProfile.primaryContact=input.primaryContact
      userProfile.photo= input.photo
      userProfile.secondaryContact=input.secondaryContact
      userProfile.currentAdd=input.currentAdd
      userProfile.currentCity=input.currentCity
      userProfile.currentState=input.currentState
      userProfile.permAdd=input.permAdd
      userProfile.permCity=input.permCity
      userProfile.permState=input.permState
      userProfile.altEmail=input.altEmail
      userProfile.gender=input.gender
      userProfile.dob=input.dob
      userProfile.bloodGroup=input.bloodGroup
      userProfile.user=ExtendUser.objects.get(email=input.user)
      userProfile.save()
      return CreateUserProfile(userProfile=userProfile)

class UpdateUserProfile(graphene.Mutation):
   class Arguments:
      input = UserProfileInput()

   userProfile = graphene.Field(UserProfileType)

   @classmethod
   def mutate(cls, root, info, input):
      user=ExtendUser.objects.get(email=input.user)
      userProfile = UserProfile.objects.get(user=user)
      userProfile.primaryContact=input.primaryContact
      # userProfile.photo= input.photo
      userProfile.secondaryContact=input.secondaryContact
      userProfile.currentAdd=input.currentAdd
      userProfile.currentCity=input.currentCity
      userProfile.currentState=input.currentState
      userProfile.permAdd=input.permAdd
      userProfile.permCity=input.permCity
      userProfile.permState=input.permState
      userProfile.altEmail=input.altEmail
      userProfile.gender=input.gender
      userProfile.dob=input.dob
      userProfile.bloodGroup=input.bloodGroup
      # userProfile.user=ExtendUser.objects.get(email=input.user)
      userProfile.save()
      return CreateUserProfile(userProfile=userProfile)


class DeleteUser(graphene.Mutation):
   success = graphene.Boolean()

   class Arguments:
      email = graphene.String(required=True)

   @classmethod
   def mutate(cls, root, info, **kwargs):
      obj = ExtendUser.objects.get(email=kwargs["email"])
      if obj is not None:
         obj.delete()
         return cls(success=True)
      else:
         return cls(success=False)

class DeleteUserProfile(graphene.Mutation):
   success = graphene.Boolean()

   class Arguments:
      email = graphene.String(required=True)

   @classmethod
   def mutate(cls, root, info, **kwargs):
      obj = ExtendUser.objects.get(email=kwargs["email"])
      profile = UserProfile.objects.get(user=obj)
      if profile is not None:
         profile.delete()
         return cls(success=True)
      else:
         return cls(success=False)

class UpdateId(graphene.Mutation):
   class Arguments:
      # userid = UserInput(reqired=True)
      email = graphene.String(required=True)
      username= graphene.String(required=True)
   
   user = graphene.Field(ExtendUserTyoe)

   @classmethod
   def mutate(cls,root,info,email, username):
      user = ExtendUser.objects.get(email=email)
      user.username=username
      user.save()
      return UpdateId(user=user)



#UserRole Queries
class CreateUserRole(graphene.Mutation):
   class Arguments:
      input=RoleInput(required=True)
   
   role=graphene.Field(UserRoleType)

   @classmethod
   def mutate(cls,root,info,input):
      role=UserRole()
      role.name=input.name
      role.description=input.description
      role.save()
      return CreateUserRole(role=role)

class UpdateUserRole(graphene.Mutation):
   class Arguments:
      input=RoleInput()
   
   role=graphene.Field(UserRoleType)

   @classmethod
   def mutate(cls,root,info,input):
      role=UserRole.objects.get(id=input.id)
      role.name=input.name
      role.description=input.description
      role.save()
      return UpdateUserRole(role=role)

class DeleteUserRole(graphene.Mutation):
   class Arguments:
      input=RoleInput(required=True)
   
   success=graphene.Boolean()

   @classmethod
   def mutate(cls,root,info,input):
      role=UserRole.objects.get(id=input.id)
      role.delete()
      return cls(success=True)

class AssignUserRole(graphene.Mutation):
   class Arguments:
      email=graphene.String(required=True)
      role=graphene.Int(required=True)

   user=graphene.Field(ExtendUserTyoe)
   @classmethod
   def mutate(cls,root,info,email,role):
      urole=UserRole.objects.get(id=role)
      user=ExtendUser.objects.get(email=email)
      user.role=urole
      user.save()
      return AssignUserRole(user=user)

class Query(UserQuery, MeQuery, graphene.ObjectType):
   temp=graphene.List(TempType)
   userProfile=graphene.List(UserProfileType)
   user_role=graphene.List(UserRoleType)

   def resolve_temp(root, info, **kwargs):
       return Temp.objects.all()
   def resolve_userProfile(root,info,**kwargs):
      return UserProfile.objects.all()
   def resolve_user_role(root,info,**kwargs):
      return UserRole.objects.all()

class Mutation(AuthMutation, graphene.ObjectType):
   update_id = UpdateId.Field()
   delete_user = DeleteUser.Field()
   create_userProfile=CreateUserProfile.Field()
   update_userProfile=UpdateUserProfile.Field()
   delete_user_profile=DeleteUserProfile.Field()
   create_user_role=CreateUserRole.Field()
   update_user_role=UpdateUserRole.Field()
   delete_user_role=DeleteUserRole.Field()
   assign_user_role=AssignUserRole.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)