from rest_framework import serializers

from companies.models import Employee, Task, Client, Product, TaskStatus, NFe, ProdutoDetalheNFe
from accounts.models import User_Groups, User, Group, Group_Permissions

from django.contrib.auth.models import Permission


class EmployeesSerializer (serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email'
        )

    def get_name(self, obj):
        return obj.user.name

    def get_email(self, obj):
        return obj.user.email


class EmployeeSerializer (serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email',
            'groups'
        )

    def get_name(self, obj):
        return obj.user.name

    def get_email(self, obj):
        return obj.user.email
    
    def get_groups(self, obj):
        groupsDB = User_Groups.objects.filter(user_id=obj.user.id).all()
        groupsDATA = []

        for group in groupsDB:
            groupsDATA.append({
                "id": group.group.id,
                "name": group.group.name
            })

        return groupsDATA
    
class GroupsSerializer (serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions'
        )

    def get_permissions(self, obj):
        groups = Group_Permissions.objects.filter(group_id=obj.id).all()
        permissions = []

        for group in groups:
            permissions.append({
                "id": group.permission.id,
                "label": group.permission.name,
                "codename": group.permission.codename
            })

        return permissions
    
class PermissionsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'codename'
        )

class TasksSerializer (serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'due_date',
            'created_at',
            'status'
        )

    def get_status(self, obj):
        return obj.status.name
    
class TaskSerializer (serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'due_date',
            'created_at',
            'status',
            'employee'
        )

    def get_status(self, obj):
        return obj.status.name
    
    def get_employee(self, obj):
        return EmployeesSerializer(obj.employee).data
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status_id = validated_data.get('status_id', instance.status_id)
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.due_date = validated_data.get('due_date', instance.due_date)

        instance.save()

        return instance
    


class ClientsSerializer (serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'cnpj_cpf',
            'ie_rg',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'cep',
            'ibge'
        )
    
    def get_name(self, obj):
        return obj.name
    
class ClientSerializer (serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'cnpj_cpf',
            'ie_rg',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'cep',
            'ibge',
            'employee'
        )

    def get_name(self, obj):
        return obj.name
    
    def get_client(self, obj):
        return obj.client.name
    
    def get_employee(self, obj):
        return EmployeesSerializer(obj.employee).data
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.cnpj_cpf = validated_data.get('cnpj_cpf', instance.cnpj_cpf)
        instance.ie_rg = validated_data.get('ie_rg', instance.ie_rg)
        instance.logradouro = validated_data.get('logradouro', instance.logradouro)
        instance.numero = validated_data.get('numero', instance.numero)
        instance.complemento = validated_data.get('complemento', instance.complemento)
        instance.bairro = validated_data.get('bairro', instance.bairro)
        instance.cidade = validated_data.get('cidade', instance.cidade)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.cep = validated_data.get('cep', instance.cep)         
        instance.ibge = validated_data.get('ibge', instance.ibge)
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.id = validated_data.get('id', instance.id)
        

        instance.save()

        return instance
    


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'code',
            'description',
            'unit',
            'ncm',
            'cest',
            'gtin',
            'value'
        )

class ProductSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'code',
            'description',
            'unit',
            'ncm',
            'cest',
            'gtin',
            'value',
            'employee'
        )

    def get_employee(self, obj):
        if obj.employee:
            return EmployeesSerializer(obj.employee).data
        return None  # Retorna None se não houver employee associado

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.description = validated_data.get('description', instance.description)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.ncm = validated_data.get('ncm', instance.ncm)
        instance.cest = validated_data.get('cest', instance.cest)
        instance.gtin = validated_data.get('gtin', instance.gtin)
        instance.value = validated_data.get('value', instance.value)
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        
        instance.save()
        return instance

class ProdutoDetalheNFeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoDetalheNFe
        fields = '__all__'

class NFeSerializer(serializers.ModelSerializer):
    produtos = ProdutoDetalheNFeSerializer(many=True, read_only=True)

    class Meta:
        model = NFe
        fields = [
            'id',
            'chave',
            'xml',
            'status',
            'data_emissao',
            'data_autorizacao',
            'data_cancelamento',
            'destinatario_cnpj',
            'valor_total',
            'mensagem_retorno',
            'emitente',
            'produtos'  # Coloque o campo 'produtos' por último
        ]
        

class ProdutoDetalheSerializer(serializers.Serializer):
    produto_id = serializers.IntegerField()
    descricao = serializers.CharField(max_length=255)
    quantidade = serializers.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    ncm = serializers.CharField(max_length=20)
    cest = serializers.CharField(max_length=20, required=False, allow_blank=True)
    unidade = serializers.CharField(max_length=10)
    valor_total = serializers.DecimalField(max_digits=10, decimal_places=2)

class ClienteDetalheSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=255)
    cnpj_cpf = serializers.CharField(max_length=14)
    ie_rg = serializers.CharField(max_length=20, required=False, allow_blank=True)
    logradouro = serializers.CharField(max_length=255)
    numero = serializers.CharField(max_length=10)
    complemento = serializers.CharField(max_length=255, required=False, allow_blank=True)
    bairro = serializers.CharField(max_length=100)
    cidade = serializers.CharField(max_length=100)
    estado = serializers.CharField(max_length=2)
    cep = serializers.CharField(max_length=9)
    ibge = serializers.CharField(max_length=7, required=False, allow_blank=True)

class EmitirNFeSerializer(serializers.Serializer):
    cliente = ClienteDetalheSerializer()
    produtos = serializers.ListField(child=ProdutoDetalheSerializer())
    frete = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0.00)




