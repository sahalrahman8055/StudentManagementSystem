from rest_framework import serializers
from admins.models import User , Role


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    
class TeacherListPostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)  

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'date_of_birth', 'address', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = self.generate_username(validated_data['first_name'], validated_data['last_name'])
        validated_data['username'] = username

        role, _ = Role.objects.get_or_create(name='teacher')
        validated_data['role'] = role
        return super().create(validated_data)
    
    def generate_username(self, first_name, last_name):
        return f"{first_name.lower()}{last_name.lower()}"

    