from app_dir.core.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User


class BlogPostsView(APIView):
    def get(self, req):
        try:
            posts = list(BlogPost.objects.filter(status=1).order_by('-braaps').values('id',
                                                                                      'title',
                                                                                      'slug',
                                                                                      'category',
                                                                                      'braaps',
                                                                                      'author__first_name',
                                                                                      'author__last_name',
                                                                                      'created_on'
                                                                                      ))

            return Response({"success": True,
                             "status": 200,
                             "posts": posts
                             })

        except Exception as e:
            return Response({"failed": True,
                             "status": 400,
                             "error": str(e)}
                            )


class BlogCategoriesView(APIView):
    def get(self, req):
        try:
            category = req.GET['category']
            categories = list(BlogPost.objects.filter(status=1, category=int(category)).order_by('-braaps').values(
                                                                                      'id',
                                                                                      'title',
                                                                                      'slug',
                                                                                      'category',
                                                                                      'braaps',
                                                                                      'author__first_name',
                                                                                      'author__last_name',
                                                                                      'created_on'
                                                                                      ))
            return Response({"success": True,
                             "status": 200,
                             "posts": categories
                             })

        except Exception as e:
            return Response({"failed": True,
                             "status": 400,
                             "error": str(e)}
                            )


class SinglePostView(APIView):
    def post(self, req):
        try:
            author = req.data['phoneNumber'].strip('+')
            user = User.objects.get(username=author)
            print(user.pk)
            title = req.data['title']
            slug = req.data['slug']
            created_on = req.data['createdOn']
            updated_on = req.data['updatedOn']
            content = req.data['content']
            status = req.data['status']
            braaps = req.data['upVotes']

            blog = BlogPost.objects.create(author=user,
                                           title=title,
                                           slug=slug,
                                           created_on=created_on,
                                           updated_on=updated_on,
                                           content=content,
                                           status=status,
                                           braaps=braaps
                                           )

            return Response({"success": True,
                             "status": 200,
                             "blog": blog.pk
                             })
        except Exception as e:
            return Response({"failed": True,
                             "status": 400,
                             "error": str(e)}
                            )

    def get(self, req):
        try:
            blog_id = req.GET['id']

            post = list(BlogPost.objects.filter(id=blog_id).values())

            return Response({"success": True,
                             "status": 200,
                             "posts": post
                             })

        except Exception as e:
            return Response({"failed": True,
                             "status": 400,
                             "error": str(e)}
                            )

    def put(self, req):
        try:
            braap = req.data['braap']
            id = req.data['id']
            blog = BlogPost.objects.filter(id=id)
            blog.update(braaps=braap)

            return Response({"success": True,
                             "status": 200,
                             })
        except Exception as e:
            return Response({"failed": True,
                             "status": 400,
                             "error": str(e)}
                            )
