from rest_framework import status
from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from Movies.models import Movie
from Movies.serializers import MovieSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.

class MoviesPagination(LimitOffsetPagination):
	default_limit = 2
	max_limit = 3

class Movies(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id','name')
    search_fields = ('id','name')
    pagination_class = MoviesPagination

class MoviesCreateView(generics.CreateAPIView):
	serializer_class = MovieSerializer
	def create(self,requests,*args,**kwargs):
		try:
			name = requests.data.get('name')
			actor = requests.data.get('actor')
			rating = requests.data.get('rating')
			return super().create(requests,*args,**kwargs)
		except Exception as e:
			return Response({
				"Message":"Failed"
				})

class Movies_details(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    lookup_field = 'id'
    serializer_class = MovieSerializer

    def delete(self,requests,*args,**kwargs):
    	try:
    		id_ = requests.data.get('id',None)
    		response = super().delete(requests,*args,*kwargs)
    		if response.status_code == 204:
    			from django.core.cache import cache
    			cache.delete("{}".format(id_))
    	except Exception as e:
    		return Response({
    			"Message":"Failed"
    			})

    def update(self,requests,*args,**kwargs):
    	response = super().update(requests,*args,*kwargs)
    	if response.status_code == 200:
    		mdata = response.data
    		from django.core.cache import cache
    		cache.set("ID:{}".format(mdata.get('id',None)),{
    			"name":mdata["name"],
    			"actor":mdata["actor"],
    			"genre":mdata['genre'],
    			"rating":mdata["rating"]
    			})
    		return response


'''class Movies(APIView):
	def get(self,requests,format=None):
		return Response({
			"Message":"Get Works"
			})

	def post(self,requests,format=None):
		datam = requests.data
		Name = datam.get("name",None)
		Actor = datam.get("actor",None)
		data.append(Name)
		return Response({
			"Response":200,
			"Data":Name,
			"Message":"Item was added to Database"
			})

	def put(self,requests,format=None):
		datam = requests.data
		return Response({
			"Message":"Put Works"
			})'''

'''global data
data = ["Movie"]
class Movies(APIView):
	def get(self,requests):
		mdata = Movie.objects.all()
		serializer = MovieSerializer(mdata,many=True)
		return Response(serializer.data)

	def post(self,requests,format=None):
		try:
			serializer = MovieSerializer(data=requests.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data,status=status.HTTP_200_OK)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)'''