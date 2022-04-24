
from .models import Customer, Policy, Vehicle
from .serializers import CustomerSerializer, PolicySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'PUT'])
def customer(request, customer_id):
    if request.method == 'GET':
        res = Customer.objects.get(customer_id=customer_id)
        serializer = CustomerSerializer(res, many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        data = CustomerSerializer(data=request.data['cust'],context={'request':request})
        cust = Customer.objects.get(customer_id=customer_id)
        if data.is_valid(raise_exception=True):
            data.update(cust,data.validated_data)
            return Response(data.validated_data)
    return Response({'message': 'wrong method'},status=500)


@api_view(['GET', 'PUT'])
def policySearch(request):
    params = request.query_params
    if request.method =='GET':
        if params['search'] == 'policy':
            try:
                pol = Policy.objects.get(policy_id__exact=params['id'])
                serializer = PolicySerializer(pol, many=False, context={'request': request})
            except:
                return Response({'error':'No Policies Found'},status=400)
            return Response(serializer.data)
        elif params['search'] == 'customer':
            try:
                pols = Policy.objects.filter(customer_id=params['id'])
                serializer = PolicySerializer(pols, many=True)
            except:
                return Response({'error': 'No Policies Found'}, status=400)
            return Response(serializer.data)
        else:
            return Response({"message": "No results Found"}, status=400)


@api_view(['PUT'])
def policy(request, policy_id):
    if request.method == 'PUT':
        data = request.data
        try:
            vechicle_id = Vehicle.objects.get(vehicle_segment=data['segment'])
            vechicle_id.fuel = data['fuel']
            vechicle_id.save()
        except:
            v =Vehicle(vehicle_segment=data['segment'],fuel=data['fuel'])
            v.save()
        data = PolicySerializer(data=request.data['policy'], context={'request': request})
        policy = Policy.objects.get(policy_id=policy_id)
        if data.is_valid(raise_exception=True):
            data.update(policy,data.validated_data)
            return Response(data.validated_data,status=201)
    return Response({'message':'fail'}, status=400)


@api_view(['GET'])
def chart(request, region):
    chartData= [["Policies", "Month"]]
    for i in range(1,13):
        pols = Policy.objects.filter(customer_id__customer_region=region, date_of_purchase__month=i).count()
        chartData.append([i,pols])
    return Response(chartData)
