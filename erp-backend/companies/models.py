from django.db import models


class Enterprise(models.Model):
    name = models.CharField(max_length=255, default='Empresa')
    cnpj = models.CharField(max_length=14, default='00000000000191')
    ie = models.CharField(max_length=12, default='000000000001')
    endereco = models.CharField(max_length=255, default='Rua Teste')
    municipio = models.CharField(max_length=255, default='São Paulo')
    uf = models.CharField(max_length=2, default='SP')
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)


class Employee(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)


class TaskStatus(models.Model):
    name = models.CharField(max_length=155)
    codename = models.CharField(max_length=100)

    class Meta:
        db_table = 'companies_task_status'


class Task(models.Model):
    title = models.TextField()
    description = models.TextField(null=True)
    due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Client(models.Model):
    name = models.TextField()
    cnpj_cpf = models.TextField(max_length=14)
    ie_rg = models.TextField(max_length=20, null=True, blank=True)
    logradouro = models.TextField()
    numero = models.TextField()
    complemento = models.TextField(null=True, blank=True)
    bairro = models.TextField()
    cidade = models.TextField()
    estado = models.TextField(max_length=2)
    cep = models.TextField(max_length=9)
    ibge = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    

class Product(models.Model):
    code = models.CharField(max_length=100)
    description = models.TextField()
    unit = models.CharField(max_length=10)  # Ex: 'un', 'kg', 'litro'
    ncm = models.CharField(max_length=20)  # Nomenclatura Comum do Mercosul
    cest = models.CharField(max_length=20, null=True, blank=True)  # Código Especificador da Substituição Tributária
    gtin = models.CharField(max_length=20, null=True, blank=True)  # Global Trade Item Number
    value = models.DecimalField(max_digits=10, decimal_places=2)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.description
    



class NFe(models.Model):
    STATUS_CHOICES = [
        ('AUTORIZADA', 'Autorizada'),
        ('CANCELADA', 'Cancelada'),
        ('REJEITADA', 'Rejeitada'),
        ('PENDENTE', 'Pendente'),
    ]

    chave = models.CharField(max_length=44, unique=True)
    #chave_validada = models.CharField(max_length=44, null=True, blank=True, unique=False)
    xml = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='PENDENTE')
    data_emissao = models.DateTimeField(auto_now_add=True)
    data_autorizacao = models.DateTimeField(null=True, blank=True)
    data_cancelamento = models.DateTimeField(null=True, blank=True)
    emitente = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='nfe_emitente')
    destinatario_cnpj = models.CharField(max_length=14)
    destinatario_nome = models.CharField(max_length=100)
    #destinatario_endereco = models.TextField()
    destinatario_logradouro = models.TextField()
    destinatario_numero = models.TextField()
    destinatario_complemento = models.TextField()
    destinatario_bairro = models.TextField()
    destinatario_cidade = models.TextField()
    destinatario_estado = models.TextField()
    destinatario_cep = models.TextField()
    destinatario_ibge = models.TextField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    mensagem_retorno = models.TextField(null=True, blank=True)
    emitente = models.ForeignKey('Enterprise', on_delete=models.CASCADE)
    frete = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'NF-e {self.chave} - {self.status}'



class ProdutoDetalheNFe(models.Model):
    nfe = models.ForeignKey(NFe, related_name='produtos', on_delete=models.CASCADE)
    produto_id = models.IntegerField()
    descricao = models.CharField(max_length=255)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    ncm = models.CharField(max_length=10)
    cest = models.CharField(max_length=10, blank=True, null=True)
    ean = models.CharField(max_length=13, blank=True, null=True)
    unidade = models.CharField(max_length=10)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)