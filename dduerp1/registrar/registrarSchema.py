
from accounts.models import UserRole
import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from .models import Faculty, Department, Program, ExamSchemeHead, TeachingSchemeHead, Subject
from accounts.models import ExtendUser
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required, user_passes_test



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

class ExamScemeType(DjangoObjectType):
    class Meta:
        model=ExamSchemeHead
        fields=(
            'id',
            'type',
        )

class TeachingSchemeType(DjangoObjectType):
    class Meta:
        model=TeachingSchemeHead
        fields=(
            'id',
            'type',
        )

class SubjectType(DjangoObjectType):
    class Meta:
        model=Subject
        fields=(
            'code',
            'name',
            'shortName',
            'teachingScheme',
            'examScheme',
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

class ExamSchemeInput(graphene.InputObjectType):
    id=graphene.Int()
    type=graphene.String()

class TeachingSchemeInput(graphene.InputObjectType):
    id=graphene.Int()
    type=graphene.String()

class SubjectInput(graphene.InputObjectType):
    code=graphene.String()
    name=graphene.String()
    shortName=graphene.String()
    teachingScheme=graphene.Int()
    examScheme=graphene.Int()


#Faculty Query
class CreateFaculty(graphene.Mutation):
    class Arguments:
        input=FacultyInput(required=True)
    
    faculty=graphene.Field(FacultyType)

    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
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
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
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
        id=graphene.Int()
    
    success=graphene.Boolean()
    error=graphene.String()
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls, root, info, id):
        if Faculty.objects.get(id=id):
            faculty=Faculty.objects.get(id=id)
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
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls, root, info, input):
        dept=Department()
        dept.name=input.name
        dept.shortName=input.shortName
        faculty=Faculty.objects.get(id=input.faculty)
        dept.faculty=faculty
        head=ExtendUser.objects.get(email=input.head)
        dept.head=head
        dept.save()
        return CreateDepartment(dept=dept)

class UpdateDepartment(graphene.Mutation):
    class Arguments:
        input=DepartmentInput(required=True)
    
    dept=graphene.Field(DepartmentType)

    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls, root, info, input):
        dept=Department.objects.get(id=input.id)
        dept.name=input.name
        dept.shortName=input.shortName
        faculty=Faculty.objects.get(id=input.faculty)
        dept.faculty=faculty
        head=ExtendUser.objects.get(email=input.head)
        dept.head=head
        dept.save()
        return CreateFaculty(dept=dept)

class DeleteDepartment(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
    
    success=graphene.Boolean()
    error=graphene.String()
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls, root, info, id):
        if Department.objects.get(id=id):
            dept=Department.objects.get(id=id)
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
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
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
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
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
        id=graphene.Int()
    
    success=graphene.Boolean()
    error=graphene.String()
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls, root, info, d):
        if Program.objects.get(id=id):
            dept=Program.objects.get(id=id)
            dept.delete()
            return cls(success=True)
        else:
            return cls(success=False,error="No Data Found")

#ExamScemeHead
class CreateExamScheme(graphene.Mutation):
    class Arguments:
        input=ExamSchemeInput()
    
    exam=graphene.Field(ExamScemeType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root, info,input):
        exam=ExamSchemeHead()
        exam.type=input.type
        exam.save()
        return CreateExamScheme(exam=exam)

class UpdateExamScheme(graphene.Mutation):
    class Arguments:
        input=ExamSchemeInput()
    
    exam=graphene.Field(ExamScemeType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root, info,input):
        exam=ExamSchemeHead.objects.get(id=input.id)
        exam.type=input.type
        exam.save()
        return UpdateExamScheme(exam=exam)

class DeleteExamScheme(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
    
    success=graphene.Boolean()
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root, info,input):
        exam=ExamSchemeHead.objects.get(id=id)
        exam.delete()
        return cls(success=True)

#Teaching Scheme
class CreateTeachingScheme(graphene.Mutation):
    class Arguments:
        input=TeachingSchemeInput()
    
    teachingScheme=graphene.Field(TeachingSchemeType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info, input):
        teachingScheme=TeachingSchemeHead()
        teachingScheme.type=input.type
        teachingScheme.save()
        return CreateTeachingScheme(teachingScheme=teachingScheme)

class UpdateTeachingScheme(graphene.Mutation):
    class Arguments:
        input=TeachingSchemeInput()
    
    teachingScheme=graphene.Field(TeachingSchemeType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info, input):
        teachingScheme=TeachingSchemeHead.objects.get(id=input.id)
        teachingScheme.type=input.type
        teachingScheme.save()
        return UpdateTeachingScheme(teachingScheme=teachingScheme)

class DeleteTeachingScheme(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
    
    success=graphene.Boolean()
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info, id):
        teachingScheme=TeachingSchemeHead.objects.get(id=id)
        teachingScheme.delete()
        return cls(success=True)

#Subject
class CreateSubject(graphene.Mutation):
    class Arguments:
        input=SubjectInput()
    
    subject=graphene.Field(SubjectType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls, root, info,input):
        subject=Subject()
        subject.code=input.code
        subject.name=input.name
        subject.shortName=input.shortName
        if input.teachingScheme :
            subject.teachingScheme=TeachingSchemeHead.objects.get(id=input.teachingScheme)
        if input.examScheme :
            subject.examScheme=ExamSchemeHead.objects.get(id=input.examScheme)
        subject.save()
        return CreateSubject(subject=subject)

class UpdateSubject(graphene.Mutation):
    class Arguments:
        input=SubjectInput()
    
    subject=graphene.Field(SubjectType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls, root, info,input):
        subject=Subject.objects.get(code=input.code)
        subject.name=input.name
        subject.shortName=input.shortName
        subject.teachingScheme=TeachingSchemeHead.objects.get(id=input.teachingScheme)
        subject.examScheme=ExamSchemeHead.objects.get(id=input.examScheme)
        subject.save()
        return CreateSubject(subject=subject)

class DeleteSubject(graphene.Mutation):
    class Arguments:
        code=graphene.String()

    success=graphene.Boolean()
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,code):
        subject=Subject.objects.get(code=code)
        subject.delete()
        return cls(success=True)
        



class Query(UserQuery, MeQuery, graphene.ObjectType):
    faculty=graphene.List(FacultyType)
    department=graphene.List(DepartmentType)
    program=graphene.List(ProgramType)
    exam_scheme_head=graphene.List(ExamScemeType)
    teaching_scheme_head=graphene.List(TeachingSchemeType)
    subject=graphene.List(SubjectType)

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_faculty(root,info,**kwargs):
        # print(info.context.user.role.name)
        return Faculty.objects.all()
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_department(root,info,**kwargs):
        return Department.objects.all()
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_program(root,info,**kwargs):
        return Program.objects.all()
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_exam_scheme_head(root,info,**kwargs):
        return ExamSchemeHead.objects.all()
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_teaching_scheme_head(root,info,**kwargs):
        return TeachingSchemeHead.objects.all()
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_subject(root,info,**kwargs):
        return Subject.objects.all()



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
    create_exam_scheme_head=CreateExamScheme.Field()
    update_exam_scheme_head=UpdateExamScheme.Field()
    delete_exam_scheme_head=DeleteExamScheme.Field()
    create_teaching_scheme_head=CreateTeachingScheme.Field()
    update_teaching_scheme_head=UpdateTeachingScheme.Field()
    delete_teaching_scheme_head=DeleteTeachingScheme.Field()
    create_subject=CreateSubject.Field()
    update_subject=UpdateSubject.Field()
    delete_subject=DeleteSubject.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)