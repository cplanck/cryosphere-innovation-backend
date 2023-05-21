# from allauth.socialaccount.models import SocialAccount
from rest_framework import serializers

from user_profiles.models import *
from user_profiles.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_avatar(self, obj):
        avatar = ''
        if obj.has_social_avatar:
            # social_account = SocialAccount.objects.get(user=obj.user)
            # social_avatar = social_account.extra_data.get('picture')
            social_avatar = ''  # THIS NEEDS TO BE FIXED AS WE MOVE TO ONE-TAP LOGIN!
            if social_avatar:
                avatar = social_avatar
        elif obj.avatar:
            avatar = obj.avatar.url
        else:
            avatar = 'https://ui-avatars.com/api/?name=' + \
                obj.user.first_name + '+' + obj.user.last_name
        return avatar
