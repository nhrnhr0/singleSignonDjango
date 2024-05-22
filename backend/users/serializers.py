
from .models import User

# override the api/token/ endpoint
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['org'] = user.organization.name if user.organization else 'no organization'
#         # ...

#         return token
    # def validate(self, attrs):
    #     data = super().validate(attrs)
        
    #     # Add custom claims
    #     data['username'] = self.user.username
        
    #     return data


# class MyRefreshTokenSerializer(TokenRefreshSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
        
#         # get the user id from the refresh token
#         user_id = RefreshToken(attrs['refresh']).payload['user_id']
#         user = User.objects.get(id=user_id)
        
#         # add organization name to the response
#         data['org'] = user.organization.name if user.organization else 'no organization'
        
#         return data