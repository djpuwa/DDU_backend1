
import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from .models import  FeeStructureHead, FeeStructureCategory
from graphene_file_upload.scalars import Upload

from graphql_jwt.decorators import login_required, user_passes_test



class FeeStructureHeadType(DjangoObjectType):
   class Meta:
      model=FeeStructureHead
      fields=(
         'id',
         'name',
         'type',
         'description',
         'time_stamp',
      )

class FeeStructureCategoryType(DjangoObjectType):
   class Meta:
      model=FeeStructureCategory
      fields=(
         'id',
         'name',
         'description',
         'time_stamp',
      )




class FeeHeadInput(graphene.InputObjectType):
   id=graphene.Int()
   name=graphene.String()
   type = graphene.String()
   description = graphene.String()
   time_stamp=graphene.DateTime()

class FeeCategoryInput(graphene.InputObjectType):
   id=graphene.Int()
   name=graphene.String()
   description = graphene.String()
   time_stamp=graphene.DateTime()


# fee structure queries
class CreateFeeStructureHead(graphene.Mutation):
   class Arguments:
      input=FeeHeadInput(required=True)
   
   feeHead=graphene.Field(FeeStructureHeadType)

   @classmethod
   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def mutate(cls, root, info, input):
      feeHead = FeeStructureHead()
      feeHead.name =input.name
      feeHead.type=input.type
      feeHead.description=input.description
      feeHead.time_stamp=input.time_stamp
      feeHead.save()
      return CreateFeeStructureHead(feeHead=feeHead)

class UpdateFeeStructure(graphene.Mutation):
   class Arguments:
      input = FeeHeadInput()
   
   feeStruct = graphene.Field(FeeStructureHeadType)

   @classmethod
   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def mutate(cls, root, info, input):
      feeStruct=FeeStructureHead.objects.get(id=input.id)
      feeStruct.name = input.name
      feeStruct.type = input.type
      feeStruct.description=input.description
      feeStruct.time_stamp=input.time_stamp
      feeStruct.save()
      return UpdateFeeStructure(feeStruct=feeStruct)

class DeleteFeeStructure(graphene.Mutation):
   class Arguments:
      id = graphene.Int()
   
   success = graphene.Boolean()

   @classmethod
   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def mutate(cls, root, info,id):
      feeStruct=FeeStructureHead.objects.get(id=id)
      feeStruct.delete()
      return cls(success=True)


# fee category queries
class CreateFeeCategoy(graphene.Mutation):
   class Arguments:
      input=FeeCategoryInput(required=True)
   
   feeCatagory=graphene.Field(FeeStructureCategoryType)

   @classmethod
   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def mutate(cls, root, info, input):
      feeHead = FeeStructureCategory()
      feeHead.name =input.name
      feeHead.description=input.description
      feeHead.time_stamp=input.time_stamp
      feeHead.save()
      return CreateFeeCategoy(feeCatagory=feeHead)

class UpdateFeeCategory(graphene.Mutation):
   class Arguments:
      input = FeeCategoryInput()
   
   feeCatagory = graphene.Field(FeeStructureCategoryType)

   @classmethod
   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def mutate(cls, root, info, input):
      feeStruct=FeeStructureCategory.objects.get(id=input.id)
      feeStruct.name = input.name
      feeStruct.description=input.description
      feeStruct.time_stamp=input.time_stamp
      feeStruct.save()
      return UpdateFeeCategory(feeCatagory=feeStruct)

class DeleteFeeCategory(graphene.Mutation):
   class Arguments:
      id = graphene.Int()
   
   success = graphene.Boolean()

   @classmethod
   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def mutate(cls, root, info,id):
      feeStruct=FeeStructureCategory.objects.get(id=id)
      feeStruct.delete()
      return cls(success=True)


class Query(UserQuery, MeQuery, graphene.ObjectType):
   fee_structure_head=graphene.Field(FeeStructureHeadType,id=graphene.Int())
   all_fee_structure_head=graphene.List(FeeStructureHeadType)
   fee_structure_category= graphene.Field(FeeStructureCategoryType,id=graphene.Int())
   all_fee_structure_category=graphene.List(FeeStructureCategoryType)

   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def resolve_fee_structure_head(root,info,**kwargs):
      return FeeStructureHead.objects.get(id=kwargs.get("id"))

   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def resolve_all_fee_structure_head(root,info,**kwargs):
      return FeeStructureHead.objects.all()
   
   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def resolve_fee_structure_category(root,info,**kwargs):
      return FeeStructureCategory.objects.get(id=kwargs.get("id"))
   
   @login_required
   @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
   def resolve_all_fee_structure_category(root,info,**kwargs):
      return FeeStructureCategory.objects.all()


class Mutation( graphene.ObjectType):
    create_fee_structure_head=CreateFeeStructureHead.Field()
    update_fee_structure_head=UpdateFeeStructure.Field()
    delete_fee_structure_head=DeleteFeeStructure.Field()
    create_fee_structure_category=CreateFeeCategoy.Field()
    update_fee_structure_category=UpdateFeeCategory.Field()
    delete_fee_structure_category=DeleteFeeCategory.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)