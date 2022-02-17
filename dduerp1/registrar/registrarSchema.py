
import email
import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from .models import Faculty, Department, Program, ExamSchemeHead
from accounts.models import ExtendUser
from graphene_file_upload.scalars import Upload




class FacultyType(DjangoObjectType):
    class Meta:
        model= Faculty
        fields=(
            'id',
            'name',
            'shortName',
            'dean',
        )

class DepartmentType(DjangoObjectType):
    class Meta:
        model= Department
        fields=(
            'id',
            'name',
            'shortName',
            'faculty',
            'head',
        )

class ProgramType(DjangoObjectType):
    class Meta:
        model=Program
        fields=(
            'id',
            'name',
            'type',
            'degree',
            'faculty',
            'department',
            'duration',
            'sessionalType',
            'maxSessions',
        )



class FacultyInput(graphene.InputObjectType):
    id=graphene.Int()
    name=graphene.String()
    shortName=graphene.String()
    dean=graphene.String()

class DepartmentInput(graphene.InputObjectType):
    id=graphene.Int()
    name=graphene.String()
    shortName=graphene.String()
    faculty=graphene.Int()
    head=graphene.String()

class ProgramInput(graphene.InputObjectType):
    id=graphene.Int()
    name=graphene.String()
    type=graphene.String()
    degree=graphene.String()
    faculty=graphene.Int()
    department=graphene.Int()
    duration=graphene.Float()
    sessionalType=graphene.String()
    maxSssions=graphene.Int()

#Faculty Query
class CreateFaculty(graphene.Mutation):
    class Arguments:
        input=FacultyInput(required=True)
    
    faculty=graphene.Field(FacultyType)

    @classmethod
    def mutate(cls, root, info, input):
        faculty=Faculty()
        faculty.name=input.name
        faculty.shortName=input.shortName
        dean=ExtendUser.objects.get(email=input.dean)
        faculty.dean=dean
        faculty.save()
        return CreateFaculty(faculty=faculty)

class UpdateFaculty(graphene.Mutation):
    class Arguments:
        input=FacultyInput()
    
    faculty=graphene.Field(FacultyType)
    @classmethod
    def mutate(cls, root, info, input):
        faculty=Faculty.objects.get(id=input.id)
        faculty.name=input.name
        faculty.shortName=input.shortName
        dean=ExtendUser.objects.get(email=input.dean)
        faculty.dean=dean
        faculty.save()
        return CreateFaculty(faculty=faculty)

class DeleteFaculty(graphene.Mutation):
    class Arguments:
        input=graphene.Int()
    
    success=graphene.Boolean()
    error=graphene.String()
    @classmethod
    def mutate(cls, root, info, input):
        if Faculty.objects.get(id=input):
            faculty=Faculty.objects.get(id=input)
            faculty.delete()
            return cls(success=True)
        else:
            return cls(success=False,error="No Data Found")


#Department Query
class CreateDepartment(graphene.Mutation):
    class Arguments:
        input=DepartmentInput(required=True)
    
    dept=graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls, root, info, input):
        dept=Department()
        dept.name=input.name
        dept.shortName=input.shortName
        faculty=Faculty.objects.get(id=input.faculty)
        dept.faculty=faculty
        head=ExtendUser.objects.get(email=input.head)
        dept.head=head
        dept.save()
        return CreateFaculty(faculty=faculty)

class UpdateDepartment(graphene.Mutation):
    class Arguments:
        input=DepartmentInput(required=True)
    
    dept=graphene.Field(DepartmentType)

    @classmethod
    def mutate(cls, root, info, input):
        dept=Department.objects.get(id=input.id)
        dept.name=input.name
        dept.shortName=input.shortName
        faculty=Faculty.objects.get(id=input.faculty)
        dept.faculty=faculty
        head=ExtendUser.objects.get(email=input.head)
        dept.head=head
        dept.save()
        return CreateFaculty(faculty=faculty)

class DeleteDepartment(graphene.Mutation):
    class Arguments:
        input=graphene.Int()
    
    success=graphene.Boolean()
    error=graphene.String()
    @classmethod
    def mutate(cls, root, info, input):
        if Department.objects.get(id=input):
            dept=Department.objects.get(id=input)
            dept.delete()
            return cls(success=True)
        else:
            return cls(success=False,error="No Data Found")

#Program Queries
class CreateProgram(graphene.Mutation):
    class Arguments:
        input=ProgramInput(required=True)
    
    program=graphene.Field(ProgramType)
    @classmethod
    def mutate(cls,root,info,input):
        program=Program()
        program.name=input.name
        program.type=input.type
        program.degree=input.degree
        program.faculty=input.faculty
        program.department=input.department
        program.duration=input.duration
        program.sessionalType=input.sessionalType
        program.maxSessions=input.maxSessions
        program.save()
        return CreateProgram(program=program)

class UpdateProgram(graphene.Mutation):
    class Arguments:
        input=ProgramInput(required=True)
    
    program=graphene.Field(ProgramType)
    @classmethod
    def mutate(cls,root,info,input):
        program=Program.objects.get(id=input.id)
        program.name=input.name
        program.type=input.type
        program.degree=input.degree
        program.faculty=input.faculty
        program.department=input.department
        program.duration=input.duration
        program.sessionalType=input.sessionalType
        program.maxSessions=input.maxSessions
        program.save()
        return UpdateProgram(program=program)

class DeleteProgram(graphene.Mutation):
    class Arguments:
        input=graphene.Int()
    
    success=graphene.Boolean()
    error=graphene.String()
    @classmethod
    def mutate(cls, root, info, input):
        if Program.objects.get(id=input):
            dept=Program.objects.get(id=input)
            dept.delete()
            return cls(success=True)
        else:
            return cls(success=False,error="No Data Found")



class Query(UserQuery, MeQuery, graphene.ObjectType):
    faculty=graphene.List(FacultyType)
    department=graphene.List(DepartmentType)
    program=graphene.List(ProgramType)

    def resolve_faculty(root,info,**kwargs):
        return Faculty.objects.all()
    def resolve_department(root,info,**kwargs):
        return Department.objects.all()
    def resolve_program(root,info,**kwargs):
        return Program.objects.all()


class Mutation( graphene.ObjectType):
    create_faculty=CreateFaculty.Field()
    update_faculty=UpdateFaculty.Field()
    delete_faculty=DeleteFaculty.Field()
    create_department=CreateDepartment.Field()
    update_department=UpdateDepartment.Field()
    delete_department=DeleteDepartment.Field()
    create_program=CreateProgram.Field()
    update_program=UpdateProgram.Field()
    delete_program=DeleteProgram.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)