import { useNavigate } from 'react-router-dom';
import { api } from '../../infra/api';
import { toast } from 'react-toastify';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { ThreeDots } from 'react-loader-spinner';
import { getUserFromLocalStorage } from '../../infra/getToken';

export const InvoiceSummary = () => {
  const navigate = useNavigate();
  const [isInvoiceSaved, setIsInvoiceSaved] = useState(false);
  const [isLoader, setIsLoader] = useState(false);
  //const [users, setUsers] = useState<Users[] | null>(null);
  // const [products, setProducts] = useState<Products[] | null>(null);

  type ValuesToInvoiceProps = {
    cliente: {
      nome: string;
      cnpj_cpf: string;
      ie_rg: string;
      logradouro: string;
      numero: string;
      complemento: string;
      bairro: string;
      cidade: string;
      estado: string;
      cep: string;
      ibge: string;
    };
    produtos: Array<{
      produto_id: number;
      descricao: string;
      quantidade: number;
      valor_unitario: number;
      ncm: string;
      cest: string;
      ean: string;
      unidade: string;
      valor_total: number;
    }>;
    frete: number;
  };

  const valuesToInvoice: ValuesToInvoiceProps = useMemo(() => {
    return {
      cliente: {
        nome: 'Cliente Teste',
        cnpj_cpf: '00000000000191',
        ie_rg: '',
        logradouro: 'Rua Exemplo',
        numero: '123',
        complemento: 'Apto 45',
        bairro: 'Centro',
        cidade: 'São José do Rio Pardo',
        estado: 'SP',
        cep: '13720000',
        ibge: '3549706',
      },
      produtos: [
        {
          produto_id: 1,
          descricao: 'Fanta Uva 350ml',
          quantidade: 2,
          valor_unitario: 3.27,
          ncm: '22021000',
          cest: '0301100',
          ean: '7894900030013',
          unidade: 'UN',
          valor_total: 6.54,
        },
        {
          produto_id: 2,
          descricao: 'Coca Cola 2L',
          quantidade: 1,
          valor_unitario: 8.0,
          ncm: '22021000',
          cest: '0301100',
          ean: '7894900030013',
          unidade: 'UN',
          valor_total: 8.0,
        },
      ],
      frete: 0,
    };
  }, []);

  const handleToGenerateInvoice = useCallback(async () => {
    try {
      setIsLoader(true);
      await api.post('companies/nfe/emitir', valuesToInvoice);
      setIsInvoiceSaved(true);
      setIsLoader(false);
      toast.success('Nota gerada com sucesso!');
    } catch (error) {
      navigate('/');
      setIsLoader(false);
      toast.error('Erro ao enviar nota');
    }
  }, [navigate, valuesToInvoice]);

  const handleGenerateInvoice = useCallback(async () => {
    try {
      setIsLoader(true);
      await api.post('companies/nfe/enviar_pendentes');
      setIsLoader(false);
      toast.success('Nota emitida com sucesso!');
      navigate('/invoice/list');
    } catch (error) {
      navigate('/');
      setIsLoader(false);
      toast.error('Erro ao emitir a nota');
    }
  }, [navigate]);

  useEffect(() => {
    const getToken = getUserFromLocalStorage();
    if (!getToken) {
      return navigate('/');
    }
  }, [navigate]);

  return (
    <div className="w-full m-auto h-auto flex flex-col justify-center items-center p-8 2xl:w-1/2 xl:w-1/2 lg:w-2/3">
      <h2 className="text-center text-white font-bold bg-sky-800 p-3 w-full">
        Resumo das informações a nota
      </h2>
      <div className="w-full bg-white shadow-md p-6 mb-2 rounded">
        <h2 className="text-sky-800 font-bold mb-4">Dados do cliente</h2>
        <p>
          <strong>Nome:</strong> {valuesToInvoice.cliente.nome} <br />
          <strong>CNPJ:</strong> {valuesToInvoice.cliente.cnpj_cpf} <br />
        </p>
        <hr className="my-4" />
        <p>
          <strong>Endereço:</strong> {valuesToInvoice.cliente.logradouro},{' '}
          {valuesToInvoice.cliente.numero} <br />
          <strong>Complemento:</strong> {valuesToInvoice.cliente.complemento}{' '}
          <br />
          <strong>Bairro:</strong> {valuesToInvoice.cliente.bairro} <br />
          <strong>Cidade:</strong> {valuesToInvoice.cliente.cidade} <br />
          <strong>Estado:</strong> {valuesToInvoice.cliente.estado} <br />
          <strong>CEP:</strong> {valuesToInvoice.cliente.cep} <br />
        </p>

        <hr className="my-4" />

        <h2 className="text-sky-800 font-bold mb-4">Dados dos produtos</h2>

        <div className="w-full grid grid-cols-2 gap-4">
          {valuesToInvoice.produtos.map((product) => (
            <div className="w-full p-2 bg-slate-100" key={product.produto_id}>
              <p className="font-bold text-center">
                {product.descricao} <br />
                Qtd: {product.quantidade} <br />
                Valor unitário: R$ {product.valor_unitario} <br />
                Valor total R$: {product.valor_unitario * product.quantidade}
              </p>
            </div>
          ))}
          <div className="w-full col-span-2">
            <p className="m-auto w-full text-center font-bold text-lg">
              Valor total: R${' '}
              {valuesToInvoice.produtos[0].valor_total +
                valuesToInvoice.produtos[1].valor_total}
            </p>
          </div>
        </div>
      </div>

      {isLoader ? (
        <div className="w-full flex justify-center items-center">
          <ThreeDots
            visible={true}
            height="80"
            width="80"
            color="#069"
            radius="9"
            ariaLabel="three-dots-loading"
          />
        </div>
      ) : (
        <>
          <button
            type="button"
            onClick={handleToGenerateInvoice}
            className={`${
              isInvoiceSaved ? 'bg-gray-300 hover:bg-gray-300' : 'bg-sky-800'
            }  text-white px-2 py-3 rounded w-full`}
            disabled={isInvoiceSaved}
          >
            Salvar nota
          </button>

          {isInvoiceSaved ? (
            <button
              type="button"
              onClick={handleGenerateInvoice}
              className="bg-green-800 hover:bg-green-800 text-white px-2 py-3 rounded w-full my-4"
            >
              Emitir nota
            </button>
          ) : (
            ''
          )}
        </>
      )}
    </div>
  );
};
