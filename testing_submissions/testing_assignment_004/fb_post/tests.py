import pytest
from .models import *
from .exceptions import *
from .utils import *
import datetime
from freezegun import freeze_time
import datetime
import unittest


@pytest.fixture
def user():
    user_obj=User.objects.create(name="ammu")
    return user_obj


@pytest.fixture
def user2():
    user_obj=User.objects.create(name="ammudu")
    return user_obj

@pytest.fixture
def user3():
    user_obj=User.objects.create(name="usha")
    return user_obj

@pytest.fixture
def user4():
    user_obj=User.objects.create(name="usha tirumalasetty")
    return user_obj


@pytest.fixture
def post():
    post_obj=Post.objects.create(posted_by_id=1,content="ammu is a very good girl")
    return post_obj

@pytest.fixture
def post2():
    post_obj=Post.objects.create(posted_by_id=2,content="ammudu is a very good girl")
    return post_obj

@pytest.fixture
def post3():
    post_obj=Post.objects.create(posted_by_id=3,content="usha is a very good girl")
    return post_obj


@pytest.fixture
def comment():
    comment_obj=Comment.objects.create(commented_by_id=1,post_id=1,content="yes ofcourse!!!")
    return comment_obj

@pytest.fixture
def reply_comment():
    reply_comment_obj=Comment.objects.create(commented_by_id=2,post_id=1,content="yes ofcourse!!!",parent_comment_id=1)
    return reply_comment_obj

@pytest.fixture
def reaction():
    reaction_obj=Reaction.objects.create(post_id=1,reaction="WOW",reacted_by_id=1)
    return reaction_obj

@pytest.fixture
def reaction2():
    reaction_obj=Reaction.objects.create(post_id=2,reaction="SAD",reacted_by_id=2)
    return reaction_obj
@pytest.fixture
def reaction3():
    reaction_obj=Reaction.objects.create(post_id=3,reaction="WOW",reacted_by_id=3)
    return reaction_obj
@pytest.fixture
def reaction4():
    reaction_obj=Reaction.objects.create(post_id=3,reaction="SAD",reacted_by_id=4)
    return reaction_obj


@pytest.fixture
def reaction_to_comment():
    reaction_obj=Reaction.objects.create(comment_id=1,reaction="WOW",reacted_by_id=1)
    return reaction_obj





@pytest.mark.django_db
def test_create_post_user_id_invalid():
    #arrange
    
    #act
    with pytest.raises(InvalidUserException):
        create_post(2,"usha")

    #assert
@pytest.mark.django_db
def test_create_post_post_content_invalid(user):
    #arrange
    
    #act
    with pytest.raises(InvalidPostContent):
        create_post(1,"")
    
    #assert
@pytest.mark.django_db
def test_create_post_valid(user):
    #arrange
    
    #act
    post=create_post(1,"usha")
    
    #assert
    assert Post.objects.get(id=1).id==post

@pytest.mark.django_db
def test_create_comment_user_id_invalid():
    #arrange
    
    #act
    with pytest.raises(InvalidUserException):
         create_comment(2,1,"usha")
    
    #assert

@pytest.mark.django_db
def test_create_comment_post_id_invalid(user):
    #arrange
    
    #act
    with pytest.raises(InvalidPostException):
         create_comment(1,1,"usha")
    
    #assert
@pytest.mark.django_db
def test_create_comment_comment_content_invalid(user,post):
    #arrange
    
    #act
    with pytest.raises(InvalidCommentContent):
        create_comment(1,1,"")

    #assert

@pytest.mark.django_db
def test_create_comment_valid(user,post):
    #arrange
    
    #act
    comment_id=create_comment(1,1,"ofcourse!!!")
    
    #assert
    assert Comment.objects.get(id=1).id==comment_id

@pytest.mark.django_db
def test_reply_to_comment_user_id_invalid():
    #arrange
    
    #act
    with pytest.raises(InvalidUserException):
        reply_to_comment(3,1,"i too agree")

    #assert
    
@pytest.mark.django_db
def test_reply_to_comment_comment_id_invalid(user):
    #arrange
    
    #act
    with pytest.raises(InvalidCommentException):
        reply_to_comment(1,3,"i too agree")
    
    #assert
    
@pytest.mark.django_db
def test_reply_to_comment_reply_content_invalid(user,comment,post):
    #arrange
    
    #act
    with pytest.raises(InvalidReplyContent):
        reply_to_comment(1,1,"")
        
    # assert

@pytest.mark.django_db
def test_reply_to_comment_for_direct_comment(user,comment,post):
    #arrange
    
    #act
    reply_id=reply_to_comment(1,1,"u need to accept because thats true")
    
    #assert
    assert Comment.objects.get(content="u need to accept because thats true").id==reply_id


@pytest.mark.django_db
def test_reply_to_comment_for_reply_comment(user,user2,comment,reply_comment,post):
    #arrange
    
    #act
    reply_to_comment(2,2,"ofcourse thats true")
    parent_id=1
    
    #assert
    assert Comment.objects.get(content="ofcourse thats true").parent_comment_id==parent_id

@pytest.mark.django_db
def test_react_to_post_user_id_invalid():
    #arrange
    
    #act
    with pytest.raises(InvalidUserException):
        react_to_post(3,1,"WOW")

    #assert
    

@pytest.mark.django_db
def test_react_to_post_comment_id_invalid(user):
    #arrange
    
    #act
    with pytest.raises(InvalidPostException):
        react_to_post(1,3,"i too agree")
    
    #assert
    
@pytest.mark.django_db
def test_react_to_post_reaction_type_invalid(user,post):
    #arrange
    
    #act
    with pytest.raises(InvalidReactionTypeException):
        react_to_post(1,1,"yep")
    
    #assert

@pytest.mark.django_db
def  test_react_to_post_first_time(user,post,reaction):
    #arrange
    
    #act
    
    #assert
    assert reaction.id==1

@pytest.mark.django_db
def  test_react_to_post_already_reacted_reaction_type_same(user,post,reaction):
    #arrange
    
    #act
    react_to_post(1,1,"WOW")
    
    #assert
    assert list(Reaction.objects.all())==[]

@pytest.mark.django_db
def  test_react_to_post_already_reacted_reaction_type_different(user,post,reaction):
    #arrange
    
    #act
    react_to_post(1,1,"LIT")
    reactions=Reaction.objects.all()
    
    #assert
    assert reactions[0].reaction=="LIT"


@pytest.mark.django_db
def test_react_to_comment_user_id_invalid():
    #arrange
    
    #act
    with pytest.raises(InvalidUserException):
        react_to_comment(3,1,"WOW")

    #assert
    
@pytest.mark.django_db
def test_react_to_comment_comment_id_invalid(user):
    #arrange
    
    #act
    with pytest.raises(InvalidCommentException):
        react_to_comment(1,3,"i too agree")
    
    #assert
    
@pytest.mark.django_db
def test_react_to_comment_reaction_type_invalid(user,post,comment):
    #arrange
    
    #act
    with pytest.raises(InvalidReactionTypeException):
        react_to_comment(1,1,"yep")
    
    #assert
        

@pytest.mark.django_db
def  test_react_to_comment_first_time(user,post,comment,reaction_to_comment):
    #arrange
    
    #act
    
    #assert
    assert reaction_to_comment.id==1


@pytest.mark.django_db
def  test_react_to_comment_already_reacted_reaction_type_same(user,post,comment,reaction_to_comment):
    #arrange
    
    #act
    react_to_comment(1,1,"WOW")
    
    #assert
    assert list(Reaction.objects.all())==[]


@pytest.mark.django_db
def  test_react_to_comment_already_reacted_reaction_type_different(user,post,comment,reaction_to_comment):
    #arrange
    
    #act
    react_to_comment(1,1,"LIT")
    reactions=Reaction.objects.all()
    
    #assert
    assert reactions[0].reaction=="LIT"

@pytest.mark.django_db
def test_get_total_reaction_count(user,post,comment,reaction,reaction_to_comment):
    #arrange
    
    #act
    
    #assert
    assert get_total_reaction_count()=={'count':2}

@pytest.mark.django_db
def test_get_reaction_metrices_post_invalid(user,user2,post,comment,reply_comment,reaction,reaction_to_comment):
    #arrange
    
    #act
    
    #assert
    assert get_reaction_metrics(1)=={"WOW":1}

@pytest.mark.django_db
def test_delete_post_user_id_invalid(user,post):
    #arrange
    
    #act
    with pytest.raises(InvalidUserException):
        delete_post(3,1)
    
    #assert

@pytest.mark.django_db
def test_delete_post_post_id_invalid(user,post):
    #arrange
    
    #act
    with pytest.raises(InvalidPostException):
        delete_post(1,3)
    
    #assert

@pytest.mark.django_db
def test_delete_post_user_id_not_creator_of_post(user,user2,post,post2):
    #arrange
    
    #act
    with pytest.raises(UserCannotDeletePostException):
        delete_post(1,2)
        
    #assert    

@pytest.mark.django_db
def test_delete_post_valid(user,user2,post,post2):
    #arrange
    
    #act
    delete_post(1,1)
    
    #assert
    assert list(Post.objects.filter(id=1,posted_by_id=1))==[]

@pytest.mark.django_db
def test_get_posts_with_positive_reactions(user,user2,post,post2,reaction,reaction2):
    #arrange
    
    #act
    
    #assert
    assert list(get_posts_with_more_positive_reactions())==[1]

@pytest.mark.django_db
def test_get_posts_with_positive_reactions_reactions_positive_none(user,user2,post,post2,reaction2):
    #arrange
    
    #act
    
    #assert
    assert list(get_posts_with_more_positive_reactions())==[]

@pytest.mark.django_db
def test_get_posts_with_positive_reactions_positive_and_negitive_equal(user,user2,user3,user4,post,post2,post3,reaction4):
    #arrange
    
    #act
    
    #assert
    assert list(get_posts_with_more_positive_reactions())==[]


@pytest.mark.django_db
def test_get_posts_reacted_by_user_id_invalid():
    #arrange
    
    #act
    with pytest.raises(InvalidUserException):
         get_posts_reacted_by_user(3)

    #assert
   
@pytest.mark.django_db
def test_get_posts_reacted_valid(user,user2,post,post2,reaction,reaction2):
    #arrange
    
    #act
    posts_reacted_by_user=[1]
    
    #assert
    assert list(get_posts_reacted_by_user(1))==posts_reacted_by_user

@pytest.mark.django_db
def test_get_reactions_to_post_post_id_invalid(user,post):
    #arrange
    
    #act
    with pytest.raises(InvalidPostException):
        get_reactions_to_post(3)
        
    #assert

@pytest.mark.django_db
def test_get_reactions_to_post_valid(user,user2,post,post2,reaction,reaction2):
    #arrange
    
    #act
    post_reactions=[{"user_id": 1, "name": "ammu", "profile_pic": None, "reaction": "WOW"},]
    #assert
    assert get_reactions_to_post(1)==post_reactions


@pytest.mark.django_db
def test_get_post_post_id_invalid():
    #arrange
    
    #act
    with pytest.raises(InvalidPostException):
        get_post(3)

    #assert

@pytest.mark.django_db
@freeze_time(str(datetime.datetime.now()))
def test_get_post():
    #arrange
    user=User.objects.create(name="ammu")
    user2=User.objects.create(name="ammudu")
    post=Post.objects.create(posted_by_id=1,content="ammu is a very good girl")
    post2=Post.objects.create(posted_by_id=2,content="ammudu is a very good girl")
    comment=Comment.objects.create(commented_by_id=1,post_id=1,content="yes ofcourse!!!")
    reply_comment=Comment.objects.create(commented_by_id=2,post_id=1,content="yes ofcourse!!!",parent_comment_id=1)
    reaction=Reaction.objects.create(post_id=1,reaction="WOW",reacted_by_id=1)
    reaction2=Reaction.objects.create(post_id=2,reaction="SAD",reacted_by_id=2)
    reaction_to_comment=Reaction.objects.create(comment_id=1,reaction="WOW",reacted_by_id=1)
    
    #act
    details=get_post(1)
    
    #assert
    assert details=={
        "post_id": 1,
        "posted_by": {
            "name": "ammu",
            "user_id": 1,
            "profile_pic":None
        },
        "posted_at":str(datetime.datetime.now()),
        "post_content": "ammu is a very good girl",
        "reactions": {
            "count": 1,
            "type": ["WOW"]
        },
        "comments": [
            {
                "comment_id": 1,
                "commenter": {
                    "user_id": 1,
                    "name":"ammu",
                    "profile_pic":None
                },
                "commented_at":str(datetime.datetime.now()),
                "comment_content": "yes ofcourse!!!",
                "reactions": {
                    "count": 1,
                    "type": ["WOW"]
                },
                "replies_count": 1,
                "replies": [{
                    "comment_id": 2,
                    "commenter": {
                        "user_id": 2,
                        "name": "ammudu",
                        "profile_pic":None
                    },
                    "commented_at":str(datetime.datetime.now()),
                    "comment_content":"yes ofcourse!!!",
                    "reactions": {
                        "count": 0,
                        "type": []
                    },
                }]
            },
        ],
        "comments_count": 1,
    }
    

@pytest.mark.django_db
def test_get_user_posts_user_id_invalid():
    #arrange
    
    #act
    with pytest.raises(InvalidUserException):
        get_user_posts(3)

    #assert
    
    
    
@pytest.mark.django_db
@freeze_time(str(datetime.datetime.now()))
def test_get_user_posts():
    #arrange
    user=User.objects.create(name="ammu")
    user2=User.objects.create(name="ammudu")
    post=Post.objects.create(posted_by_id=1,content="ammu is a very good girl")
    post2=Post.objects.create(posted_by_id=2,content="ammudu is a very good girl")
    comment=Comment.objects.create(commented_by_id=1,post_id=1,content="yes ofcourse!!!")
    reply_comment=Comment.objects.create(commented_by_id=2,post_id=1,content="yes ofcourse!!!",parent_comment_id=1)
    reaction=Reaction.objects.create(post_id=1,reaction="WOW",reacted_by_id=1)
    reaction2=Reaction.objects.create(post_id=2,reaction="SAD",reacted_by_id=2)
    reaction_to_comment=Reaction.objects.create(comment_id=1,reaction="WOW",reacted_by_id=1)
    
    #act
    details=get_user_posts(1)
    #assert
    assert details==[{
        "post_id": 1,
        "posted_by": {
            "name": "ammu",
            "user_id": 1,
            "profile_pic":None
        },
        "posted_at":str(datetime.datetime.now()),
        "post_content": "ammu is a very good girl",
        "reactions": {
            "count": 1,
            "type": ["WOW"]
        },
        "comments": [
            {
                "comment_id": 1,
                "commenter": {
                    "user_id": 1,
                    "name":"ammu",
                    "profile_pic":None
                },
                "commented_at":str(datetime.datetime.now()),
                "comment_content": "yes ofcourse!!!",
                "reactions": {
                    "count": 1,
                    "type": ["WOW"]
                },
                "replies_count": 1,
                "replies": [{
                    "comment_id": 2,
                    "commenter": {
                        "user_id": 2,
                        "name": "ammudu",
                        "profile_pic":None
                    },
                    "commented_at":str(datetime.datetime.now()),
                    "comment_content":"yes ofcourse!!!",
                    "reactions": {
                        "count": 0,
                        "type": []
                    },
                }]
            },
        ],
        "comments_count": 1,
    }]
    
    
    
@pytest.mark.django_db
def test_get_replies_for_comment_comment_id_invalid():
    #arrange
    
    #act
    with pytest.raises(InvalidCommentException):
        get_replies_for_comment(3)
        
    #assert    
        
@pytest.mark.django_db
@freeze_time(str(datetime.datetime.now()))
def test_get_replies_for_comment():
    #arrange
    User.objects.create(name="ammu")
    User.objects.create(name="ammudu")
    Post.objects.create(posted_by_id=1,content="ammu is a very good girl")
    Post.objects.create(posted_by_id=2,content="ammudu is a very good girl")
    Comment.objects.create(commented_by_id=1,post_id=1,content="yes ofcourse!!!")
    Comment.objects.create(commented_by_id=2,post_id=1,content="yes ofcourse!!!",parent_comment_id=1)
    
    #act
    details=get_replies_for_comment(1)
    
    #assert
    assert details== [{
                    "comment_id": 2,
                    "commenter": {
                        "user_id": 2,
                        "name": "ammudu",
                        "profile_pic":None
                    },
                    "commented_at":str(datetime.datetime.now()),
                    "comment_content":"yes ofcourse!!!"}]
                    
                       
                    
                    
                    