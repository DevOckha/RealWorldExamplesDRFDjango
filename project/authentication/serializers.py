from django.contrib.auth import authenticate
from rest_framework import serializers
from profiles.serializers import ProfileSerializer

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serileştiriciler kayıt istekleri yapar ve yeni bir kullanıcı oluşturur."""

    password = serializers.CharField(max_length=255, min_length=8, write_only=True)

    # İstemci, bir kayıtla birlikte bir jeton gönderememelidir.

    token = serializers.CharField(max_length=255, read_only=True)

    # Yeni bir kullanıcı oluşturmak için daha önce yazdığımız `create_user` yöntemini kullanın.
    def create(self, validated_data):
        return User.object.create_user(**validated_data)
    
    
    class Meta:
        model = User
        # Bir isteğe dahil edilebilecek tüm alanları listeleyin # veya yanıt, yukarıda açıkça belirtilen alanlar dahil edilir.
        fields = ['email', 'username', 'password', 'token']



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=8, write_only=True)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email is required to log in')
        
        if password is None:
            raise serializers.ValidationError('A password is required to log in')
        

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found')
        

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')


        # 'validate' yöntemi, doğrulanmış verilerden oluşan bir sözlük döndürmelidir. # Bu, 'create' ve 'update' yöntemlerine iletilen verilerdir. # daha sonra göreceğiz.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }



class UserSerializer(serializers.ModelSerializer):
    """Kullanıcı nesnelerinin serileştirilmesini ve seri durumdan çıkarılmasını yönetir."""

    password = serializers.CharField(max_length=255, min_length=8, write_only=True)

    profile = ProfileSerializer(write_only=True)

    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.CharField(source='profile.image', read_only=True)

    class Meta:
        models = User
        fields = ('email', 'username', 'password', 'token', 'profile', 'bio', 'image')
        read_only_fields = ('token',)

    """Bir Kullanıcı üzerinde güncelleme gerçekleştirir."""
    def update(self, instance, validated_data):
        # Şifreler diğer alanların aksine `setattr` ile işlem görmemelidir. # Bunun nedeni, Django'nun hashlemeyi işleyen bir işlev sağlaması ve # güvenlik için önemli olan şifreleri tuzlamak.

        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        
        if password is not None:

            instance.set_password(password)


        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
        

        instance.profile.save()



        return instance




















