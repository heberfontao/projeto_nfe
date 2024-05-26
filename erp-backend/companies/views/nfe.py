from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from companies.serializers import NFeSerializer, EmitirNFeSerializer
from companies.models import NFe, ProdutoDetalheNFe, Product, Client, Enterprise

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.entidades import NotaFiscal as NFeEntity, Emitente, Cliente, Produto
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.utils.flags import CODIGO_BRASIL
from pynfe.entidades.fonte_dados import _fonte_dados
from lxml import etree
from pynfe.utils.flags import NAMESPACE_NFE
import urllib3

from OpenSSL import crypto
from datetime import datetime
from companies.views.base import Base
from companies.utils.permissions import TaskPermission
from rest_framework.exceptions import APIException, ValidationError
from django.utils import timezone
import hashlib
import requests
import os
from decimal import Decimal
import logging
import time
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from pynfe.utils import obter_codigo_por_municipio

# Desabilitar avisos de requisições não verificadas (não recomendado para produção)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from django.http import HttpResponse
from brazilfiscalreport.danfe import Danfe
import tempfile
import os

def gerar_danfe(xml_content):
    # Instantiate the DANFE object with the loaded XML content
    danfe = Danfe(xml=xml_content)

    # Cria um HttpResponse para o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="DANFE.pdf"'

    # Usa um arquivo temporário para salvar o PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        temp_pdf_path = tmp_file.name
        danfe.output(temp_pdf_path)

    # Lê o conteúdo do PDF gerado e escreve no HttpResponse
    with open(temp_pdf_path, 'rb') as pdf_file:
        response.write(pdf_file.read())

    # Remove o arquivo temporário
    os.remove(temp_pdf_path)

    return response


def validar_municipio(municipio, uf):
    try:
        return obter_codigo_por_municipio(municipio, uf)
    except ValueError:
        raise ValidationError({'municipio': f"Município inválido: {municipio} na UF: {uf}"})
    
def validar_xml(xml):
    try:
        # Atualize o caminho para o arquivo XSD
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas', 'nfe_v4.00.xsd')
        schema = etree.XMLSchema(etree.parse(schema_path))
        parser = etree.XMLParser(schema=schema)
        etree.fromstring(xml, parser)
    except etree.XMLSyntaxError as e:
        raise ValidationError({'xml': f"Erro na validação do XML contra o schema: {e}"})

certificado = "38543966000148.pfx"
senha = 'FC43489900'
uf = 'sp'
homologacao = True

class EmitirNFeView(Base):
    def post(self, request):
        emitente_id = self.get_enterprise_id(request.user.id)
        cliente_data = request.data.get('cliente')
        produtos_data = request.data.get('produtos')
        frete = request.data.get('frete', 0.00)

        # Validar se os campos obrigatórios estão presentes
        if not cliente_data:
            raise ValidationError({'cliente': 'Os dados do cliente são obrigatórios.'})
        if not produtos_data:
            raise ValidationError({'produtos': 'Os dados dos produtos são obrigatórios.'})

        destinatario_cnpj = cliente_data.get('cnpj_cpf')
        destinatario_nome = cliente_data.get('nome')
        destinatario_logradouro = cliente_data.get('logradouro')
        destinatario_numero = cliente_data.get('numero')
        destinatario_complemento = cliente_data.get('complemento')
        destinatario_bairro = cliente_data.get('bairro')
        destinatario_cidade = cliente_data.get('cidade')
        destinatario_estado = cliente_data.get('estado')
        destinatario_cep = cliente_data.get('cep')
        destinatario_ibge = cliente_data.get('ibge')

        if not destinatario_cnpj:
            raise ValidationError({'cliente': {'cnpj_cpf': 'Este campo é obrigatório.'}})
        if not destinatario_nome:
            raise ValidationError({'cliente': {'nome': 'Este campo é obrigatório.'}})

        valor_total = sum(produto['valor_total'] for produto in produtos_data) + frete

        # Gerar uma chave única usando hash
        chave = self.gerar_chave_unica(emitente_id, destinatario_cnpj, valor_total)

        nfe = NFe.objects.create(
            chave=chave,
            xml="",
            status="PENDENTE",
            data_emissao=timezone.now(),
            destinatario_cnpj=destinatario_cnpj,
            destinatario_nome=destinatario_nome,
            destinatario_logradouro=destinatario_logradouro,
            destinatario_numero=destinatario_numero,
            destinatario_complemento=destinatario_complemento,
            destinatario_bairro=destinatario_bairro,
            destinatario_cidade=destinatario_cidade,
            destinatario_estado=destinatario_estado,
            destinatario_cep=destinatario_cep,
            destinatario_ibge=destinatario_ibge,
            valor_total=valor_total,
            frete=frete,
            emitente_id=emitente_id
        )

        # Adicionar produtos à NF-e
        for produto_data in produtos_data:
            ProdutoDetalheNFe.objects.create(
                nfe=nfe,
                produto_id=produto_data['produto_id'],
                descricao=produto_data['descricao'],
                quantidade=produto_data['quantidade'],
                valor_unitario=produto_data['valor_unitario'],
                ncm=produto_data['ncm'],
                cest=produto_data.get('cest', ''),
                unidade=produto_data['unidade'],
                valor_total=produto_data['valor_total']
            )

        return Response({'message': 'NF-e emitida com sucesso', 'chave': chave}, status=status.HTTP_201_CREATED)

    def gerar_chave_unica(self, emitente_id, destinatario_cnpj, valor_total):
        hash_input = f"{emitente_id}{destinatario_cnpj}{valor_total}{timezone.now()}"
        chave = hashlib.sha256(hash_input.encode()).hexdigest()[:44]  # Tamanho da chave NF-e: 44 caracteres
        return chave

class ListarNFePendentesView(Base):
    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        # Filtrar NF-es com status "PENDENTE"
        nfes_pendentes = NFe.objects.filter(status='PENDENTE', emitente_id=enterprise_id)
        serializer = NFeSerializer(nfes_pendentes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConsultarNFeView(Base):
    def get(self, request, chave):
        enterprise_id = self.get_enterprise_id(request.user.id)

        try:
            nfe = NFe.objects.get(chave=chave, emitente_id=enterprise_id)
        except NFe.DoesNotExist:
            return Response({'error': 'NF-e não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = NFeSerializer(nfe)
        return Response(serializer.data, status=status.HTTP_200_OK)









class EnviarNFePendenteView(APIView):

    @staticmethod
    def remove_namespace(xml):
        ''' Remove namespaces from an XML string '''
        try:
            xslt_root = etree.XML('''<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
                                        <xsl:output method="xml" indent="yes"/>
                                        <xsl:template match="*">
                                            <xsl:element name="{local-name()}">
                                                <xsl:apply-templates select="@*|node()"/>
                                            </xsl:element>
                                        </xsl:template>
                                        <xsl:template match="@*|text()">
                                            <xsl:copy/>
                                        </xsl:template>
                                    </xsl:stylesheet>''')
            transform = etree.XSLT(xslt_root)
            tree = etree.fromstring(xml)
            new_tree = transform(tree)
            return etree.tostring(new_tree, encoding='unicode', pretty_print=True)
        except Exception as e:
            logging.error(f'Erro ao remover namespaces: {e}')
            return xml

    def post(self, request):
        enterprise = get_object_or_404(Enterprise, id=1)
        nfes_pendentes = NFe.objects.filter(status__in=['PENDENTE', 'REJEITADA'], emitente_id=enterprise.id)

        if not nfes_pendentes:
            return Response({'error': 'Nenhuma NF-e pendente ou rejeitada encontrada'}, status=status.HTTP_404_NOT_FOUND)

        for nfe in nfes_pendentes:
            emitente = Emitente(
                razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
                nome_fantasia='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
                cnpj=enterprise.cnpj,
                codigo_de_regime_tributario='1',
                inscricao_estadual=enterprise.ie,
                inscricao_municipal='12345',
                cnae_fiscal='4751201',
                endereco_logradouro=enterprise.endereco,
                endereco_numero='666',
                endereco_bairro='Centro',
                endereco_municipio=enterprise.municipio,
                endereco_uf=enterprise.uf,
                endereco_cep='13720000',
                endereco_pais='1058'
            )

            destinatario = Cliente(
                razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
                tipo_documento='CNPJ',
                email='email@email.com',
                numero_documento=nfe.destinatario_cnpj,
                indicador_ie=9,
                endereco_logradouro=nfe.destinatario_logradouro,
                endereco_numero=nfe.destinatario_numero,
                endereco_complemento=nfe.destinatario_complemento,
                endereco_bairro=nfe.destinatario_bairro,
                endereco_municipio=nfe.destinatario_cidade,
                endereco_uf=nfe.destinatario_estado,
                endereco_cep=nfe.destinatario_cep,
                endereco_pais='1058',
                endereco_telefone='11912341234',
            )

            nota_fiscal = NotaFiscal(
                emitente=emitente,
                cliente=destinatario,
                uf=enterprise.uf,
                natureza_operacao='VENDA',
                forma_pagamento=0,
                tipo_pagamento=1,
                modelo=55,
                serie='1',
                numero_nf=str(nfe.id),
                data_emissao=datetime.now(),
                data_saida_entrada=datetime.now(),
                tipo_documento=1,
                municipio=nfe.destinatario_ibge,
                tipo_impressao_danfe=1,
                forma_emissao='1',
                cliente_final=1,
                indicador_destino=1,
                indicador_presencial=1,
                finalidade_emissao='1',
                processo_emissao='0',
                transporte_modalidade_frete=1,
                informacoes_adicionais_interesse_fisco='Mensagem complementar'
            )

            valor_total_tributos = Decimal('0.00')

            for produto in ProdutoDetalheNFe.objects.filter(nfe=nfe):
                valor_tributos_aprox = Decimal('21.06')  # Substitua pelo valor real dos tributos se disponível
                valor_total_tributos += valor_tributos_aprox

                nota_fiscal.adicionar_produto_servico(
                    codigo=str(produto.produto_id),
                    descricao=produto.descricao,
                    ncm=produto.ncm,
                    cfop='5102',
                    unidade_comercial=produto.unidade,
                    ean='SEM GTIN' if not produto.ean else produto.ean,
                    ean_tributavel='SEM GTIN' if not produto.ean else produto.ean,
                    quantidade_comercial=Decimal(produto.quantidade),
                    valor_unitario_comercial=Decimal(produto.valor_unitario),
                    valor_total_bruto=Decimal(produto.valor_total),
                    unidade_tributavel=produto.unidade,
                    quantidade_tributavel=Decimal(produto.quantidade),
                    valor_unitario_tributavel=Decimal(produto.valor_unitario),
                    ind_total=1,
                    icms_modalidade='102',
                    icms_origem=0,
                    icms_csosn='400',
                    pis_modalidade='07',
                    cofins_modalidade='07',
                    valor_tributos_aprox=valor_tributos_aprox
                )

            # Ajuste do valor total dos tributos
            nota_fiscal.informacoes_adicionais_interesse_fisco = 'Mensagem complementar'
            nota_fiscal.totais_tributos_aproximado = valor_total_tributos

            # Serialização do XML
            serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
            nfe_serializada = serializador.exportar(nota_fiscal)

            # Assinatura do XML
            a1 = AssinaturaA1(certificado, senha)
            xml_assinado = a1.assinar(nfe_serializada)

            # Envio para SEFAZ
            con = ComunicacaoSefaz(enterprise.uf, certificado, senha, homologacao)
            envio = con.autorizacao(modelo='nfe', nota_fiscal=xml_assinado)

            # Adicionar logging para depuração
            logging.info(f'Tipo de envio[1]: {type(envio[1])}')
            logging.info(f'Conteúdo de envio[1]: {envio[1].text}')

            # Processamento da resposta da SEFAZ
            try:
                xml_response_str = envio[1].text
                xml_response_str = xml_response_str.encode('utf-8') if isinstance(xml_response_str, str) else xml_response_str
                xml_response = etree.fromstring(xml_response_str)
                cStat = xml_response.find('.//{http://www.portalfiscal.inf.br/nfe}cStat').text
                xMotivo = xml_response.find('.//{http://www.portalfiscal.inf.br/nfe}xMotivo').text

                logging.info(f'Resposta da SEFAZ - cStat: {cStat}, xMotivo: {xMotivo}')  # Adicionando log

                if cStat == '103':
                    nRec = xml_response.find('.//{http://www.portalfiscal.inf.br/nfe}nRec').text
                    nfe.mensagem_retorno = nRec

                    # Consultar o recibo até que o lote seja processado ou até um número máximo de tentativas
                    tentativas = 5
                    while tentativas > 0:
                        time.sleep(5)  # Aguardar 5 segundos antes de consultar o recibo
                        consulta = con.consulta_recibo(numero=nRec, modelo='nfe')

                        # Adicionar logging para depuração
                        logging.info(f'Tipo de consulta[1]: {type(consulta)}')
                        logging.info(f'Conteúdo de consulta[1]: {consulta.text}')

                        # Processamento da resposta da consulta de recibo
                        xml_consulta_str = consulta.text
                        xml_consulta_str = xml_consulta_str.encode('utf-8') if isinstance(xml_consulta_str, str) else xml_consulta_str
                        xml_response_consulta = etree.fromstring(xml_consulta_str)
                        cStat_consulta = xml_response_consulta.find('.//{http://www.portalfiscal.inf.br/nfe}cStat').text
                        xMotivo_consulta = xml_response_consulta.find('.//{http://www.portalfiscal.inf.br/nfe}xMotivo').text

                        logging.info(f'Resposta da consulta - cStat: {cStat_consulta}, xMotivo: {xMotivo_consulta}')  # Adicionando log

                        if cStat_consulta == '104':  # Lote processado
                            protNFe = xml_response_consulta.find('.//{http://www.portalfiscal.inf.br/nfe}protNFe')
                            if protNFe is not None:
                                infProt = protNFe.find('.//{http://www.portalfiscal.inf.br/nfe}infProt')
                                if infProt is not None:
                                    cStat_infProt = infProt.find('.//{http://www.portalfiscal.inf.br/nfe}cStat').text
                                    if cStat_infProt == '100':  # Autorizado o uso da NF-e
                                        nfe.status = 'AUTORIZADA'
                                        xml_infProt = self.remove_namespace(etree.tostring(infProt, encoding='unicode'))  # Remover namespaces antes de salvar
                                        nfe.mensagem_retorno = infProt.find('.//{http://www.portalfiscal.inf.br/nfe}xMotivo').text
                                        chave = infProt.find('.//{http://www.portalfiscal.inf.br/nfe}chNFe').text
                                        nfe.chave = chave  # Salvar a chave da nota
                                        nfe.data_autorizacao = timezone.now()  # Salvar a data de autorização

                                        # Construir o XML completo
                                        xml_nfe = etree.tostring(nfe_serializada, encoding='unicode')
                                        xml_protNFe = f'<protNFe xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">{xml_infProt}</protNFe>'
                                        xml_completo = f'<?xml version="1.0" encoding="UTF-8"?><nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">{xml_nfe}{xml_protNFe}</nfeProc>'
                                        nfe.xml = xml_completo
                                        break
                                    else:
                                        nfe.status = 'REJEITADA'
                                        nfe.mensagem_retorno = infProt.find('.//{http://www.portalfiscal.inf.br/nfe}xMotivo').text
                                        break
                        elif cStat_consulta == '105':  # Lote ainda em processamento
                            logging.info(f'Lote ainda em processamento. Tentativas restantes: {tentativas}')
                            tentativas -= 1
                        else:
                            nfe.status = 'REJEITADA'
                            nfe.mensagem_retorno = xMotivo_consulta
                            break
                    if tentativas == 0:
                        nfe.status = 'ERRO'
                        nfe.mensagem_retorno = 'Lote não processado após várias tentativas'
                elif cStat == '100':
                    # Quando a nota é autorizada diretamente na resposta de envio
                    nfe.status = 'AUTORIZADA'
                    infProt = xml_response.find('.//{http://www.portalfiscal.inf.br/nfe}infProt')
                    xml_infProt = self.remove_namespace(etree.tostring(infProt, encoding='unicode'))  # Remover namespaces antes de salvar
                    nfe.mensagem_retorno = infProt.find('.//{http://www.portalfiscal.inf.br/nfe}xMotivo').text
                    chave = infProt.find('.//{http://www.portalfiscal.inf.br/nfe}chNFe').text
                    nfe.chave = chave  # Salvar a chave da nota
                    nfe.data_autorizacao = timezone.now()  # Salvar a data de autorização

                    # Construir o XML completo
                    xml_nfe = etree.tostring(nfe_serializada, encoding='unicode')
                    xml_protNFe = f'<protNFe xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">{xml_infProt}</protNFe>'
                    xml_completo = f'<?xml version="1.0" encoding="UTF-8"?><nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">{xml_nfe}{xml_protNFe}</nfeProc>'
                    nfe.xml = xml_completo
                else:
                    nfe.status = 'REJEITADA'
                    nfe.mensagem_retorno = xMotivo
            except Exception as e:
                logging.error(f'Erro no processamento da resposta da SEFAZ: {str(e)}')
                nfe.status = 'ERRO'
                nfe.mensagem_retorno = str(e)

            # Adicionar logging para o processo de salvamento
            logging.info(f'Salvando NF-e: ID={nfe.id}, Status={nfe.status}, Mensagem={nfe.mensagem_retorno}, XML={nfe.xml}, Chave={nfe.chave}, Data Autorização={nfe.data_autorizacao}')

            nfe.save()

        return Response({'success': 'NF-e(s) processada(s) com sucesso'}, status=status.HTTP_200_OK)






class CancelarNFeView(Base):
    def post(self, request, chave):
        enterprise_id = self.get_enterprise_id(request.user.id)

        try:
            nfe = NFe.objects.get(chave=chave, emitente_id=enterprise_id)
        except NFe.DoesNotExist:
            return Response({'error': 'NF-e não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        if nfe.status == 'CANCELADA':
            return Response({'error': 'NF-e já está cancelada'}, status=status.HTTP_400_BAD_REQUEST)

        nfe.status = 'CANCELADA'
        nfe.data_cancelamento = timezone.now()
        nfe.save()

        return Response({'message': 'NF-e cancelada com sucesso'}, status=status.HTTP_200_OK)

class ListarTodasNFeView(Base):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        nfes = NFe.objects.filter(emitente_id=enterprise_id).all()

        nfe_list = []
        for nfe in nfes:
            produtos = ProdutoDetalheNFe.objects.filter(nfe=nfe).values()
            nfe_list.append({
                "id": nfe.id,
                "chave": nfe.chave,
                "xml": nfe.xml,
                "status": nfe.status,
                "data_emissao": nfe.data_emissao,
                "data_autorizacao": nfe.data_autorizacao,
                "data_cancelamento": nfe.data_cancelamento,
                "destinatario_cnpj": nfe.destinatario_cnpj,
                "destinatario_nome": nfe.destinatario_nome,
                "destinatario_logradouro": nfe.destinatario_logradouro,
                "destinatario_numero": nfe.destinatario_numero,
                "destinatario_complemento": nfe.destinatario_complemento,
                "destinatario_bairro": nfe.destinatario_bairro,
                "destinatario_cidade": nfe.destinatario_cidade,
                "destinatario_estado": nfe.destinatario_estado,
                "destinatario_cep": nfe.destinatario_cep,
                "destinatario_ibge": nfe.destinatario_ibge,
                "valor_total": nfe.valor_total,
                "mensagem_retorno": nfe.mensagem_retorno,
                "emitente": nfe.emitente_id,
                "frete": nfe.frete,
                "produtos": list(produtos)
            })

        return Response(nfe_list, status=status.HTTP_200_OK)

class ConsultarStatusNFeView(Base):
    def get(self, request, chave):
        enterprise_id = self.get_enterprise_id(request.user.id)

        try:
            nfe = NFe.objects.get(chave=chave, emitente_id=enterprise_id)
        except NFe.DoesNotExist:
            return Response({'error': 'NF-e não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        try:
            con = ComunicacaoSefaz(nfe.emitente.uf, certificado, senha, homologacao=True)
            envio = con.consulta_nota('nfe', chave)

            # Processar o XML de resposta
            ns = {'ns': NAMESPACE_NFE}
            prot = etree.fromstring(envio.content)
            status_retorno = prot.xpath('//ns:retConsSitNFe/ns:cStat', namespaces=ns)[0].text

            if status_retorno == '100':
                prot_nfe = prot.xpath('//ns:retConsSitNFe/ns:protNFe', namespaces=ns)[0]
                xml = etree.tostring(prot_nfe, encoding='unicode')
                return Response({
                    'status': 'Autorizada',
                    'xml': xml,
                    'mensagem_retorno': 'Autorização realizada com sucesso.'
                }, status=status.HTTP_200_OK)
            else:
                mensagem_retorno = prot.xpath('//ns:retConsSitNFe/ns:xMotivo', namespaces=ns)[0].text
                return Response({
                    'status': 'Rejeitada',
                    'mensagem_retorno': mensagem_retorno
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GerarDanfeView(APIView):
    def get(self, request, chave_acesso):
        nfe = get_object_or_404(NFe, chave=chave_acesso)
        if nfe.status != 'AUTORIZADA':
            return Response({'error': 'NF-e não está autorizada'}, status=400)

        # Carregar o conteúdo do XML da NF-e
        xml_content = nfe.xml

        # Gerar e retornar o DANFE em PDF
        response = gerar_danfe(xml_content)
        return response