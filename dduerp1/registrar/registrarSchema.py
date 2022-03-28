

from accounts.models import UserRole
import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from .models import *
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

class ExamScemeHeadType(DjangoObjectType):
    class Meta:
        model=ExamSchemeHead
        fields=(
            'id',
            'type',
        )

class TeachingSchemeHeadType(DjangoObjectType):
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

class TeachingSchemeType(DjangoObjectType):
    class Meta:
        model=TeachingScheme
        fields=(
            "id",
            "head",
            "hours",
            "credit",
        )

class ExamSchemeType(DjangoObjectType):
    class Meta:
        model=ExamScheme
        fields=(
            "id",
            "head",
            "maxMarks",
            "minMarks",
            "passingMarks",
        )

class SubjectTeachingType(DjangoObjectType):
    class Meta:
        model=SubjectTeaching
        fields=(
            "id",
            "schemeId",
            "teachingScheme",
        )

class SubjectExamType(DjangoObjectType):
    class Meta:
        model=SubjectExam
        fields=(
            "id",
            "schemeId",
            "examScheme",
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

class ExamSchemeHeadInput(graphene.InputObjectType):
    id=graphene.Int()
    type=graphene.String()

class TeachingSchemeHeadInput(graphene.InputObjectType):
    id=graphene.Int()
    type=graphene.String()

class SubjectInput(graphene.InputObjectType):
    code=graphene.String()
    name=graphene.String()
    shortName=graphene.String()
    teachingScheme=graphene.String()
    examScheme=graphene.String()

class TeachingSchemeInput(graphene.InputObjectType):
    id=graphene.Int()
    teachingHead=graphene.Int()
    hours=graphene.Int()
    credit=graphene.Int()

class ExamSchemeInput(graphene.InputObjectType):
    id=graphene.Int()
    head=graphene.Int()
    maxMarks=graphene.Int()
    minMarks=graphene.Int()
    passingMarks=graphene.Int()



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
class CreateExamSchemeHead(graphene.Mutation):
    class Arguments:
        input=ExamSchemeHeadInput()
    
    exam=graphene.Field(ExamScemeHeadType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root, info,input):
        exam=ExamSchemeHead()
        exam.type=input.type
        exam.save()
        return CreateExamScheme(exam=exam)

class UpdateExamSchemeHead(graphene.Mutation):
    class Arguments:
        input=ExamSchemeHeadInput()
    
    exam=graphene.Field(ExamScemeHeadType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root, info,input):
        exam=ExamSchemeHead.objects.get(id=input.id)
        exam.type=input.type
        exam.save()
        return UpdateExamSchemeHead(exam=exam)

class DeleteExamSchemeHead(graphene.Mutation):
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
class CreateTeachingSchemeHead(graphene.Mutation):
    class Arguments:
        input=TeachingSchemeHeadInput()
    
    teachingScheme=graphene.Field(TeachingSchemeHeadType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info, input):
        teachingScheme=TeachingSchemeHead()
        teachingScheme.type=input.type
        teachingScheme.save()
        return CreateTeachingSchemeHead(teachingScheme=teachingScheme)

class UpdateTeachingSchemeHead(graphene.Mutation):
    class Arguments:
        input=TeachingSchemeHeadInput()
    
    teachingScheme=graphene.Field(TeachingSchemeHeadType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info, input):
        teachingScheme=TeachingSchemeHead.objects.get(id=input.id)
        teachingScheme.type=input.type
        teachingScheme.save()
        return UpdateTeachingSchemeHead(teachingScheme=teachingScheme)

class DeleteTeachingSchemeHead(graphene.Mutation):
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
        subject.teachingScheme=input.teachingScheme
        subject.examScheme=input.examScheme
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
        subject.teachingScheme=input.teachingScheme
        subject.examScheme=input.examScheme
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

class CreateExamScheme(graphene.Mutation):
    class Arguments:
        input=ExamSchemeInput()
    
    exam=graphene.Field(ExamSchemeType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,input):
        exam=ExamScheme()
        exam.head=ExamSchemeHead.objects.get(id=input.head)
        exam.maxMarks=input.maxMarks
        exam.minMarks=input.minMarks
        exam.passingMarks=input.passingMarks
        exam.save()
        return CreateExamScheme(exam=exam)

class UpdateExamScheme(graphene.Mutation):
    class Arguments:
        input=ExamSchemeInput()
    
    exam=graphene.Field(ExamSchemeType)
    @classmethod    
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,input):
        exam=ExamScheme.objects.get(id=input.id)
        exam.head=ExamSchemeHead.objects.get(id=input.head)
        exam.maxMarks=input.maxMarks
        exam.minMarks=input.minMarks
        exam.passingMarks=input.passingMarks
        exam.save()
        return UpdateExamScheme(exam=exam)

class DeleteExamScheme(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
    
    success=graphene.Boolean()
    
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,id):
        try:
            exam=ExamScheme.objects.get(id=id)
            exam.delete()
            return cls(success=True)
        except:
            return cls(success=False)

class CreateTeachingScheme(graphene.Mutation):
    class Arguments:
        input=TeachingSchemeInput()
    
    scheme=graphene.Field(TeachingSchemeType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,input):
        scheme=TeachingScheme()
        scheme.head=TeachingSchemeHead.objects.get(id=input.head)
        scheme.hours=input.hours
        scheme.credit=input.credit
        scheme.save()
        return CreateTeachingScheme(scheme=scheme)

class UpdateTeachingScheme(graphene.Mutation):
    class Arguments:
        input=TeachingSchemeInput()
    
    scheme=graphene.Field(TeachingSchemeType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,input):
        scheme=TeachingScheme.objects.get(id=input.id)
        scheme.head=TeachingSchemeHead.objects.get(id=input.head)
        scheme.hours=input.hours
        scheme.credit=input.credit
        scheme.save()
        return UpdateTeachingScheme(scheme=scheme)

class DeleteTeachingScheme(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
    
    success=graphene.Boolean()
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,id):
        try:
            scheme=TeachingScheme.objects.get(id=id)
            scheme.delete()
            return cls(success=True)
        except:
            return cls(success=False)

class CreateSubjectTeaching(graphene.Mutation):
    class Arguments:
        schemeId=graphene.String()
        teachingScheme=graphene.Int()
    
    scheme=graphene.Field(SubjectTeachingType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,schemeId,teachingScheme):
        scheme=SubjectTeaching()
        scheme.schemeId=schemeId
        scheme.teachingScheme=TeachingScheme.objects.get(id=teachingScheme)
        scheme.save()
        return CreateSubjectTeaching(scheme=scheme)

class UpdateSubjectTeaching(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
        schemeId=graphene.String()
        teachingScheme=graphene.Int()
    
    scheme=graphene.Field(SubjectTeachingType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,schemeId,teachingScheme,id):
        scheme=SubjectTeaching.objects.get(id=id)
        scheme.schemeId=schemeId
        scheme.teachingScheme=TeachingScheme.objects.get(id=teachingScheme)
        scheme.save()
        return UpdateSubjectTeaching(scheme=scheme)

class DeleteSubjectTeaching(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
    
    success=graphene.Boolean()
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,id):
        try:
            scheme=SubjectTeaching.objects.get(id=id)
            scheme.save()
            return cls(success=True)
        except:
            return cls(success=False)

class CreateSubjectExam(graphene.Mutation):
    class Arguments:
        schemeId=graphene.String()
        examScheme=graphene.Int()
    
    scheme=graphene.Field(SubjectExamType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,schemeId,examScheme):
        scheme=SubjectExam()
        scheme.schemeId=schemeId
        scheme.examScheme=ExamScheme.objects.get(id=examScheme)
        scheme.save()
        return CreateSubjectExam(scheme=scheme)

class UpdateSubjectExam(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
        schemeId=graphene.String()
        examScheme=graphene.Int()
    
    scheme=graphene.Field(SubjectExamType)
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,schemeId,examScheme,id):
        scheme=SubjectExam.objects.get(id=id)
        scheme.schemeId=schemeId
        scheme.examScheme=ExamScheme.objects.get(id=examScheme)
        scheme.save()
        return UpdateSubjectExam(scheme=scheme)

class DeleteSubjectExam(graphene.Mutation):
    class Arguments:
        id=graphene.Int()
    
    success=graphene.Boolean()
    @classmethod
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def mutate(cls,root,info,id):
        try:
            scheme=SubjectExam.objects.get(id=id)
            scheme.save()
            return cls(success=True)
        except:
            return cls(success=False)



class Query(UserQuery, MeQuery, graphene.ObjectType):
    faculty=graphene.Field(FacultyType,id=graphene.Int())
    all_faculty=graphene.List(FacultyType)
    all_department=graphene.List(DepartmentType)
    department=graphene.Field(DepartmentType,id=graphene.Int())
    all_program=graphene.List(ProgramType)
    program=graphene.Field(ProgramType,id=graphene.Int())
    all_exam_scheme_head=graphene.List(ExamScemeHeadType)
    exam_scheme_head=graphene.Field(ExamScemeHeadType,id=graphene.Int())
    all_teaching_scheme_head=graphene.List(TeachingSchemeHeadType)
    teaching_scheme_head=graphene.Field(TeachingSchemeHeadType,id=graphene.Int())
    all_subject=graphene.List(SubjectType)
    subject=graphene.Field(SubjectType,id=graphene.Int())
    all_exam_scheme=graphene.List(ExamSchemeType)
    exam_scheme=graphene.Field(ExamSchemeType,id=graphene.Int())
    all_teaching_scheme=graphene.List(TeachingSchemeType)
    teaching_scheme=graphene.Field(TeachingSchemeType,id=graphene.Int())
    all_subject_teaching=graphene.List(SubjectTeachingType)
    subject_teaching=graphene.Field(SubjectTeachingType,id=graphene.Int())
    subject_teaching_collection=graphene.List(SubjectTeachingType,schemeId=graphene.String())
    all_subject_exam=graphene.List(SubjectExamType)
    subject_exam=graphene.Field(SubjectExamType,id=graphene.Int())
    subject_exam_collection=graphene.List(SubjectExamType,schemeId=graphene.String())

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_subject_exam(root,info,**kwargs):
        return SubjectExam.objects.all()

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_subject_exam(root,info,**kwargs):
        return SubjectExam.objects.get(id=kwargs.get("id"))

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_subject_exam_collection(root,info,schemeId):
        return SubjectExam.objects.filter(schemeId=schemeId)

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_subject_teaching(root,info,**kwargs):
        return SubjectTeaching.objects.all()

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_subject_teaching(root,info,**kwargs):
        return SubjectTeaching.objects.get(id=kwargs.get("id"))

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_subject_teaching_collection(root,info,schemeId):
        return SubjectTeaching.objects.filter(schemeId=schemeId)

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_teaching_scheme(root,info,**kwargs):
        return TeachingScheme.objects.all()

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_teaching_scheme(root,info,**kwargs):
        return TeachingScheme.objects.get(id=kwargs.get("id"))

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_exam_scheme(root,info,**kwargs):
        return ExamScheme.objects.all()
    
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_exam_scheme(root,info,**kwargs):
        return ExamScheme.objects.get(id=kwargs.get("id"))

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_faculty(root,info,**kwargs):
        # print(info.context.user.role.name)
        return Faculty.objects.get(id=kwargs.get("id"))
    
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_faculty(root,info,**kwargs):
        # print(info.context.user.role.name)
        return Faculty.objects.all()

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_department(root,info,**kwargs):
        return Department.objects.all()
    
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_department(root,info,**kwargs):
        return Department.objects.get(id=kwargs.get("id"))

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_program(root,info,**kwargs):
        return Program.objects.all()

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_program(root,info,**kwargs):
        return Program.objects.get(id=kwargs.get("id"))

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_exam_scheme_head(root,info,**kwargs):
        return ExamSchemeHead.objects.all()
    
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_exam_scheme_head(root,info,**kwargs):
        return ExamSchemeHead.objects.get(id=kwargs.get("id"))

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_teaching_scheme_head(root,info,**kwargs):
        return TeachingSchemeHead.objects.all()
    
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_teaching_scheme_head(root,info,**kwargs):
        return TeachingSchemeHead.objects.get(id=kwargs.get("id"))

    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_all_subject(root,info,**kwargs):
        return Subject.objects.all()
    
    @login_required
    @user_passes_test(lambda user: user.role == UserRole.objects.get(name="Registrar"))
    def resolve_subject(root,info,**kwargs):
        return Subject.objects.get(id=kwargs.get("id"))



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
    update_exam_scheme_head=UpdateExamSchemeHead.Field()
    delete_exam_scheme_head=DeleteExamSchemeHead.Field()
    create_teaching_scheme_head=CreateTeachingSchemeHead.Field()
    update_teaching_scheme_head=UpdateTeachingSchemeHead.Field()
    delete_teaching_scheme_head=DeleteTeachingSchemeHead.Field()
    create_subject=CreateSubject.Field()
    update_subject=UpdateSubject.Field()
    delete_subject=DeleteSubject.Field()
    create_exam_scheme=CreateExamScheme.Field()
    update_exam_scheme=UpdateExamScheme.Field()
    delete_exam_scheme=DeleteExamScheme.Field()
    creat_teaching_scheme=CreateTeachingScheme.Field()
    update_teaching_scheme=UpdateTeachingScheme.Field()
    delete_teaching_scheme=DeleteTeachingScheme.Field()
    create_subject_teaching=CreateSubjectTeaching.Field()
    update_subject_teaching=UpdateSubjectTeaching.Field()
    delete_subject_teaching=DeleteSubjectTeaching.Field()
    create_subject_exam=CreateSubjectExam.Field()
    update_subject_exam=UpdateSubjectExam.Field()
    delete_subject_exam=DeleteSubjectExam.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)