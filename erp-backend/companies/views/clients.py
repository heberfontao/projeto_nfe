from companies.views.base import Base
from companies.utils.permissions import ClientPermission
from companies.serializers import ClientSerializer, ClientsSerializer
from companies.models import Client

from rest_framework.response import Response
from rest_framework.exceptions import APIException

import datetime


class Clients(Base):
    permission_classes = [ClientPermission]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        clients = Client.objects.filter(enterprise_id=enterprise_id).all()

        serializer = ClientsSerializer(clients, many=True)

        return Response({"clients": serializer.data})

    def post(self, request):
        employee_id = request.data.get('employee_id')
        name = request.data.get('name')
        cnpj_cpf = request.data.get('cnpj_cpf')
        ie_rg = request.data.get('ie_rg')
        logradouro = request.data.get('logradouro')
        numero = request.data.get('numero')
        complemento = request.data.get('complemento')
        bairro = request.data.get('bairro')
        cidade = request.data.get('cidade')
        estado = request.data.get('estado')
        cep = request.data.get('cep')
        ibge = request.data.get('ibge')

        employee = self.get_employee(employee_id, request.user.id)
       

        # Validators
        if not name or len(name) > 125:
            raise APIException("Envie um nome válido.")

        

        client = Client.objects.create(
            name=name,
            cnpj_cpf=cnpj_cpf,
            ie_rg=ie_rg,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cep=cep,
            ibge=ibge,         
            employee_id=employee_id,
            enterprise_id=employee.enterprise.id
        )

        serializer = ClientSerializer(client)

        return Response({"client": serializer.data})


class ClientDetail(Base):
    permission_classes = [ClientPermission]

    def get(self, request, client_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        client = self.get_client(client_id, enterprise_id)

        serializer = ClientSerializer(client)

        return Response({"client": serializer.data})

    def put(self, request, client_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        client = self.get_client(client_id, enterprise_id)

        name = request.data.get('name', client.name)
        employee_id = request.data.get('employee_id', client.employee.id)
        cnpj_cpf = request.data.get('cnpj_cpf', client.cnpj_cpf)
        ie_rg = request.data.get('ie_rg', client.ie_rg)
        logradouro = request.data.get('logradouro', client.logradouro)
        numero = request.data.get('numero', client.numero)
        complemento = request.data.get('complemento', client.complemento)
        cidade = request.data.get('cidade', client.cidade)
        estado = request.data.get('estado', client.estado)
        cep = request.data.get('cep', client.cep)
        ibge = request.data.get('ibge', client.ibge)
        
        
        

        # Validators
        self.get_client(client_id, enterprise_id)
        self.get_employee(employee_id, request.user.id)

        
        data = {
            "name": name,
            "cnpj_cpf": cnpj_cpf,
            "ie_rg": ie_rg,
            "logradouro": logradouro,
            "numero": numero,
            "complemento": complemento,
            "cidade": cidade,
            "estado": estado,
            "cep": cep,
            "ibge": ibge,
        }

        serializer = ClientSerializer(client, data=data, partial=True)

        if not serializer.is_valid():
            raise APIException("Não foi possível editar a tarefa")

        serializer.update(client, serializer.validated_data)

        return Response({"client": serializer.data})

    def delete(self, request, client_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        client = self.get_client(client_id, enterprise_id).delete()

        return Response({"success": True})
    