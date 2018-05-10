import model_reference
import pytest
from iospec import IoSpec

from codeschool import settings
from codeschool.accounts.factories import make_yoda_teacher, make_teachers, \
    make_students, make_joe_user
from codeschool.conftest import model_fixture
from codeschool.core.models import get_wagtail_root_page
from codeschool.lms.activities.factories import make_basic_activities

# Tests
joe_user = model_fixture(make_joe_user)
yoda_teacher = model_fixture(make_yoda_teacher)


@pytest.fixture
def root(db):
    return model_reference.load('root-page')


@pytest.fixture
def hello_world_question(root):
    from questions.coding_io import make_hello_world_question
    return make_hello_world_question(root)


def test_hello_world_submissions(hello_world_question, joe_user):
    from questions.coding_io import make_hello_world_submissions
    sub1, sub2 = make_hello_world_submissions(hello_world_question, joe_user)


def test_create_yoda(db):
    yoda = make_yoda_teacher()
    assert yoda.profile
    assert yoda.profile.age == 900


def test_create_teachers(db):
    teachers = make_teachers()


def test_create_students(db):
    students = make_students(5)


def test_create_standard_activities(db):
    make_basic_activities()


def test_create_basic_coding_io_questions(db):
    parent = get_wagtail_root_page()
    from questions.coding_io import \
        make_hello_world_question, make_question_from_markio_example
    make_hello_world_question(parent)
    make_question_from_markio_example('simple.md', parent)


def test_basic_coding_io_can_expand_tests(hello_world_question):
    question = hello_world_question
    pre = question.get_expanded_pre_tests()
    post = question.get_expand_post_tests()
    assert isinstance(pre, IoSpec)
    assert pre == post


def test_consecutive_submissions_recycle(db, hello_world_question, user,
                                         request_with_user):
    qst = hello_world_question
    sub1 = qst.submit(request_with_user, source='print("hello")',
                      language='python')
    sub2 = qst.submit(request_with_user, source='print("hello")',
                      language='python')
    assert sub1.id == sub2.id
    assert sub2.num_recycles == 1


def test_can_send_submission_and_autograde(db, hello_world_question, user,
                                           request_with_user):
    submission = hello_world_question.submit(
        request_with_user, source='print("hello")', language='python')
    feedback = submission.auto_feedback()
    assert feedback.given_grade_pc == 0


# Optional apps
if 'codeschool.lms.courses' in settings.INSTALLED_APPS:
    def test_create_course(db, yoda_teacher):
        from codeschool.lms.courses.factories import make_cs101_course

        course = make_cs101_course(yoda_teacher)
