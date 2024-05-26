from companies.views.base import Base
from companies.utils.permissions import ProductPermission
from companies.serializers import ProductSerializer, ProductsSerializer
from companies.models import Product

from rest_framework.response import Response
from rest_framework.exceptions import APIException




class Products(Base):
    permission_classes = [ProductPermission]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        products = Product.objects.filter(enterprise_id=enterprise_id).all()

        serializer = ProductsSerializer(products, many=True)

        return Response({"products": serializer.data})

    def post(self, request):
        employee_id = request.data.get('employee_id')
        description = request.data.get('description')
        code = request.data.get('code')
        unit = request.data.get('unit')
        ncm = request.data.get('ncm')
        cest = request.data.get('cest')
        gtin = request.data.get('gtin')
        value = request.data.get('value')
        
        employee = self.get_employee(employee_id, request.user.id)
       

        # Validators
        if not code or len(code) > 100:
            raise APIException("Envie um código válido.")

        

        product = Product.objects.create(
            code=code,
            description=description,
            unit=unit,
            ncm=ncm,
            cest=cest,
            gtin=gtin,
            value=value,       
            employee_id=employee_id,
            enterprise_id=employee.enterprise.id
        )

        serializer = ProductSerializer(product)

        return Response({"product": serializer.data})


class ProductDetail(Base):
    permission_classes = [ProductPermission]

    def get(self, request, product_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        product = self.get_product(product_id, enterprise_id)

        serializer = ProductSerializer (product)

        return Response({"product": serializer.data})

    def put(self, request, product_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        product = self.get_product(product_id, enterprise_id)

        code = request.data.get('code', product.code)
        employee_id = request.data.get('employee_id', product.employee.id)
        description = request.data.get('description', product.description)
        unit = request.data.get('unit', product.unit)
        ncm = request.data.get('ncm', product.ncm)
        cest = request.data.get('cest', product.cest)
        gtin = request.data.get('gtin', product.gtin)
        value = request.data.get('value', product.value)
        
        
        
        

        # Validators
        self.get_product(product_id, enterprise_id)
        self.get_employee(employee_id, request.user.id)

        
        data = {
            "code": code,
            "description": description,
            "unit": unit,
            "ncm": ncm,
            "cest": cest,
            "gtin": gtin,
            "value": value,
        }

        serializer = ProductsSerializer(product, data=data, partial=True)

        if not serializer.is_valid():
            raise APIException("Não foi possível editar o produto")

        serializer.update(product, serializer.validated_data)

        return Response({"product": serializer.data})

    def delete(self, request, product_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        product = self.get_product(product_id, enterprise_id).delete()

        return Response({"success": True})
    