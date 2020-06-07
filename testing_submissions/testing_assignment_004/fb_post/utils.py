from datetime import datetime
from .exceptions import *
from django.db.models import *

from .models import *
def create_post(user_id, post_content):
    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException
    if not post_content:
        raise InvalidPostContent

    post=Post.objects.create(content=post_content,posted_by_id=user_id)
    return post.id

def create_comment(user_id, post_id, comment_content):
    if not User.objects.filter(id=user_id).exists():
        raise InvalidUserException
    if not Post.objects.filter(id=post_id).exists():
        raise InvalidPostException
    if not comment_content:
        raise InvalidCommentContent
    comment=Comment.objects.create(content=comment_content,commented_by_id=user_id,post_id=post_id)
    return comment.id

def reply_to_comment(user_id, comment_id, reply_content):
    comment=Comment.objects.filter(id=comment_id)
    user=User.objects.filter(id=user_id)
    if not user:
        raise InvalidUserException
    if not comment:
        raise InvalidCommentException
    if not reply_content:
        raise InvalidReplyContent
    if comment[0].parent_comment_id:
        reply=Comment.objects.create(content=reply_content,commented_by_id=user_id,post_id=comment[0].post_id,parent_comment_id=comment[0].parent_comment_id)
    else:
        reply=Comment.objects.create(content=reply_content,commented_by_id=user_id,post_id=comment[0].post_id,parent_comment_id=comment_id)
    return reply.id

def react_to_post(user_id, post_id, reaction_type):
    user=User.objects.filter(id=user_id)
    post=Post.objects.filter(id=post_id)
    if not user:
        raise InvalidUserException
    if not post:
        raise InvalidPostException
    if reaction_type not in ["WOW","LIT","LOVE","HAHA","THUMBS-UP","THUMBS-DOWN","ANGRY","SAD"]:
        raise InvalidReactionTypeException
    react=Reaction.objects.filter(reacted_by_id=user_id,post_id=post_id)
    if not react:
        Reaction.objects.create(post_id=post_id,reaction=reaction_type,reacted_by_id=user_id)
    else:
        if react[0].reaction==reaction_type:
            react[0].delete()
        else :
            react[0].reaction=reaction_type
            react[0].save()



def react_to_comment(user_id, comment_id, reaction_type):
    user=User.objects.filter(id=user_id)
    comment=Comment.objects.filter(id=comment_id)
    if not user:
        raise InvalidUserException
    if not comment:
        raise InvalidCommentException
    if reaction_type not in ["WOW","LIT","LOVE","HAHA","THUMBS-UP","THUMBS-DOWN","ANGRY","SAD"]:
        raise InvalidReactionTypeException
    react=Reaction.objects.filter(reacted_by_id=user_id,comment_id=comment_id)
    if not react:
        Reaction.objects.create(comment_id=comment_id,reaction=reaction_type,reacted_by_id=user_id)
    else:
        if react[0].reaction==reaction_type:
            react[0].delete()
        else :
            react[0].reaction=reaction_type
            react[0].save()



def get_total_reaction_count():
    return Reaction.objects.aggregate(count=Count("reaction"))


def get_reaction_metrics(post_id):
    post=Post.objects.filter(id=post_id)
    if not post:
        raise InvalidPostException
    react= Reaction.objects.filter(post_id=post_id).values_list("reaction").annotate(Count("reaction"))
    return dict(react)

def delete_post(user_id, post_id):
    post=Post.objects.filter(id=post_id)
    if not post:
        raise InvalidPostException
    if post[0].posted_by_id==user_id:
        post[0].delete()

    user=User.objects.filter(id=user_id)
    if not user:
        raise InvalidUserException
    if post[0].posted_by_id!=user_id:
        raise UserCannotDeletePostException



def get_posts_with_more_positive_reactions():
    positive=Count("reaction",filter=Q(reaction__in=["THUMBS-UP","LIT","LOVE","HAHA","WOW"]))
    negitive=Count("reaction",filter=Q(reaction__in=["SAD","ANGRY","THUMBS-DOWN"]))
    return Reaction.objects.annotate(p=positive).annotate(n=negitive).filter(p__gt=F('n')).values_list("post_id",flat=True).distinct()




def get_posts_reacted_by_user(user_id):
    user=User.objects.filter(id=user_id)
    if not user:
        raise InvalidUserException
    return Reaction.objects.filter(reacted_by=user_id).values_list("post_id",flat=True)



def get_reactions_to_post(post_id):
    post=Post.objects.filter(id=post_id)
    if not post:
        raise InvalidPostException
    react=Reaction.objects.filter(post_id=post_id).select_related("reacted_by")
    return [
             {
                 "user_id":reaction_obj.reacted_by_id,
                 "name":reaction_obj.reacted_by.name,
                 "profile_pic":reaction_obj.reacted_by.profile_pic,
                 "reaction":reaction_obj.reaction

             }
            for reaction_obj in react
        ]

def get_dict(post):
    comment_list = []
    for comment in list(post.comments.all()):
        reply_list=[]
        for reply in list(post.comments.all()):
            if reply.parent_comment_id == comment.id:
                replies ={
                    "comment_id": reply.id,
                    "commenter": {
                    "user_id": reply.commented_by_id,
                    "name": reply.commented_by.name,
                    "profile_pic": reply.commented_by.profile_pic
                },
                "commented_at": str(reply.commented_at)[:-6],
                "comment_content": reply.content,
                "reactions": {
                    "count": reply.reaction.count(),
                    "type": list(dict.fromkeys([p.reaction for p in reply.reaction.all()]))
                    }
                }
                reply_list.append(replies)
        if not comment.parent_comment_id:
            comment = {
                "comment_id": comment.id,
                "commenter": {
                    "user_id": comment.commented_by_id,
                    "name": comment.commented_by.name,
                    "profile_pic": comment.commented_by.profile_pic
                },
                "commented_at": str(comment.commented_at)[:-6],
                "comment_content": comment.content,
                "reactions": {
                    "count": comment.reaction.count(),
                    "type": list(dict.fromkeys([p.reaction for p in comment.reaction.all()]))
                },
                "replies_count": len(reply_list),
                "replies": reply_list,
            }
            comment_list.append(comment)

    res = {
        "post_id": post.id,
        "posted_by": {
            "name": post.posted_by.name,
            "user_id": post.posted_by_id,
            "profile_pic": post.posted_by.profile_pic
        },
        "posted_at": str(post.posted_at)[:-6],
        "post_content": post.content,
        "reactions": {
            "count": post.reaction.count(),
            "type": list(dict.fromkeys([p.reaction for p in post.reaction.all()]))
        },
        "comments" : comment_list,
        "comments_count": len(comment_list),
    }
    return res

#task - 13
def get_post(post_id):
    try:
        post = list(Post.objects.select_related('posted_by').prefetch_related('comments', 'reaction', 'comments__reaction','comments__commented_by').filter(id = post_id))[0]
    except:
        #if not Post.objects.filter(pk = post_id).exists():
        raise InvalidPostException
    return get_dict(post)

#Task - 14
def get_user_posts(user_id):
    post = list(
            Post.objects.select_related(
                    'posted_by'
                ).prefetch_related(
                    'comments', 'reaction', 'comments__reaction','comments__commented_by'
                    ).filter(
                            posted_by_id = user_id
                        )
            )
    if not post:
        if not User.objects.filter(pk = user_id).exists():
            raise InvalidUserException
    res_list = []
    for p in post:
        res_list.append(get_dict(p))
    return res_list


def get_replies_for_comment(comment_id):
    comments=Comment.objects.filter(parent_comment_id=comment_id).select_related("commented_by")
    if not comments:
        raise InvalidCommentException

    return [
                {
                    "comment_id": comment_obj.id,
                    "commenter":
                    {
                        "user_id": comment_obj.commented_by.id,
                        "name":  comment_obj.commented_by.name,
                        "profile_pic": comment_obj.commented_by.profile_pic
                    },
                    "commented_at": str(comment_obj.commented_at)[:-6],
                    "comment_content": comment_obj.content
                }
                for comment_obj in comments
            ]




def usha():
    post=Post.objects.select_related("posted_by").prefectch_relatetd("comments","reaction","comments__commented_by","comments__reaction").filter(id=post_id)[0]
    {
        "post_id":post.id,
        "posted_by":
            {
                "name":post.posted_by.name,
                "user_id":post.posted_by.id,
                "profile_pic":post.posted_by.profile_pic
        },
        "posted_at":post.posted_at,
        "post_content":post.content,
        
        
        
    }
    return 




