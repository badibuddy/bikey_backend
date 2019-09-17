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

            client = nexmo.Client(key='e76caf5c', secret='C6boNDHAaSawjnp6')

            client.send_message({
                'from': 'Nexmo',
                'to': phone,
                'text': one_time_password,
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
            password = req.GET['password']
            username = req.GET['phoneNumber'].strip('+')
            user = User.objects.get(username__exact=username)
            valid = user.check_password(password)

            if not valid:
                return Response({"failed": True,
                                 "status": 400,
                                 "error": "Password validation error"})

            return Response({"success": True,
                             "status": 200,
                             "user_id": user.pk})

        except Exception as e:
            return Response({"failed": True,
                             "status": 400,
                             "error": str(e)}
                            )





