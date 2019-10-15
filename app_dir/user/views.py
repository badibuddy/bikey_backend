import nexmo
from random import randint

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response


class UserManagement(APIView):
    def post(self, req):
        try:
            phone = req.data['phoneNumber'].strip('+')
            email = req.data['email']
            first_name = req.data['firstName']
            last_name = req.data['lastName']
            password = req.data['password']

            user = User.objects.create_user(username=phone,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name
                                            )
            # Generate 6 Digit OTP

            one_time_password = randint(100000, 999999)

            client = nexmo.Client(key='TEST', secret='TEST')

            client.send_message({
                'from': 'Nexmo',
                'to': phone,
                'text': "Your OTP is: " + str(one_time_password) + ". It expires in 5 minutes.",
            })

            return Response({"success": True,
                             "status": 200,
                             "user_id": user.pk,
                             "OTP": one_time_password
                             })
        except Exception as e:
            return Response({"failed": True,
                             "status": 400,
                             "error": str(e)}
                            )

    def get(self, req):
        try:
            username = req.GET['phoneNumber'].strip('+')
            password = req.GET['password']

            user = User.objects.get(username__exact=username)
            valid = user.check_password(password)

            if not valid:
                return Response({"failed": True,
                                 "status": 400,
                                 "error": "Password validation error"})

            return Response({"success": True,
                             "status": 200,
                             "user_id": user.pk,
                             "user_first_name": user.first_name,
                             "user_last_name": user.last_name,
                             "user_status": user.is_superuser
                             })

        except Exception as e:
            return Response({"failed": True,
                             "status": 400,
                             "error": str(e)}
                            )

    def delete(self, req):
        try:
            phone = req.data['phoneNumber'].strip('+')
            user = User.objects.get(username=phone)
            user.delete()
            return Response({"success": True,
                             "status": 200,
                             "message": "The user is deleted"})

        except User.DoesNotExist:
            return Response({"success": True,
                             "status": 400,
                             "message": "User does not exist"})
        except Exception as e:
            return Response({"success": True,
                             "status": 400,
                             "message": str(e)})


