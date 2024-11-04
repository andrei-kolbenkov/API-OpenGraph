import requests
from bs4 import BeautifulSoup
from rest_framework import viewsets, status, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Link, Collection
from .serializers import LinkSerializer, CollectionSerializer, RegisterSerializer, UserSerializer, LoginSerializer, PasswordResetSerializer
# from knox.models import AuthToken
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend



class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title']
    ordering_fields = ['id', 'title', 'created_at', 'updated_at']

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        url = serializer.validated_data.get('url')
        if Link.objects.filter(user=self.request.user, url=url).exclude(pk=self.get_object().pk).exists():
            raise ValidationError("Ссылка с таким URL уже добавлена вами.")
        serializer.save()


    def perform_create(self, serializer):
        url = self.request.data.get('url')
        if Link.objects.filter(user=self.request.user, url=url).exists():
            raise ValidationError("Ссылка с таким URL уже добавлена вами.")
        # if self.request.data['collections']
        title, description, image_url, link_type = self.get_link_data(url)
        serializer.save(
            user=self.request.user,
            title=title,
            description=description,
            image_url=image_url,
            link_type=link_type
        )


    # Парсинг ссылки
    def get_link_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string if soup.title else ''

            # Получение описания из Open Graph или из мета-тега
            description = (soup.find("meta", property="og:description") or
                           soup.find("meta", attrs={"name": "description"}))
            description = description['content'] if description else ''

            # Получение изображения
            image_url = soup.find("meta", property="og:image")
            image_url = image_url['content'] if image_url else ''

            # Получение типа ссылки
            link_type = soup.find("meta", property="og:type")
            link_type = link_type['content'] if link_type else 'website'

            return title, description, image_url, link_type

        except Exception as e:
            print(f"Ошибка при извлечении данных из {url}: {e}")
            return '', '', '', 'website'  # Возвращаем значения по умолчанию


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['title']
    ordering_fields = ['id', 'title', 'created_at', 'updated_at']

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data
        })

class LoginAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer  # Указываем сериализатор для входа

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            return Response({
                "user": UserSerializer(user).data
            })
        else:
            return Response({"detail": "Неверные учетные данные."}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пароль успешно обновлен."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
