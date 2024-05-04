from rest_framework import serializers
from admins.models import User , Role


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    
class TeacherRegisterSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'date_of_birth', 'address', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role, _ = Role.objects.get_or_create(name='teacher')
        validated_data['role'] = role
        return super().create(validated_data)
    
    
    def get_username(self, obj):
        return f"{obj.first_name.lower()}"
    
