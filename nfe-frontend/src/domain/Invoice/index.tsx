// import { useCallback, useEffect, useState } from 'react';
import { useCallback, useEffect, useState } from 'react';
import { useForm, SubmitHandler, Controller } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';
import { getUserFromLocalStorage } from '../../infra/getToken';
import { api } from '../../infra/api';
import { toast } from 'react-toastify';

export const Invoice = () => {
  type InvoiceFormProps = {
    users: Users[] | null;
    products: Products[] | null;
  };

  type Users = {
    id: number;
    name: string;
    cnpj_cpf: string;
    ie_rg: string;
    logradouro: string;
    numero: string;
    complemento: string;
    cidade: string;
    estado: string;
    ibge: string;
    bairro: string;
    cep: string;
  };

  type Products = {
    id: number;
    code: string;
    description: string;
    unit: string;
    ncm: string;
    cest: string;
    gtin: string;
    value: string;
  };

  const navigate = useNavigate();
  const [users, setUsers] = useState<Users[] | null>(null);
  const [products, setProducts] = useState<Products[] | null>(null);
  const { control, handleSubmit, watch } = useForm<InvoiceFormProps>();

  const watchProducts = watch('products');
  const onSubmit: SubmitHandler<InvoiceFormProps> = (data) => {
    // console.info(data);
    navigate('/invoice/summary', { state: { valuesToInvoice: data } });
  };

  // const getProductsMock: Products[] = [
  //   {
  //     id: 8,
  //     code: '1',
  //     description: 'Fanta Uva',
  //     unit: 'UN',
  //     ncm: '35109999',
  //     cest: '1305170',
  //     gtin: '551651515615615611',
  //     value: '10.51',
  //   },
  //   {
  //     id: 10,
  //     code: '2',
  //     description: 'Fanta Maçã 2L',
  //     unit: 'UN',
  //     ncm: '97261539',
  //     cest: '78061377',
  //     gtin: '550829551036452974',
  //     value: '10,51',
  //   },
  //   {
  //     id: 11,
  //     code: '3',
  //     description: 'Fanta Laranja 1L',
  //     unit: 'UN',
  //     ncm: '49206173',
  //     cest: '5930416',
  //     gtin: '557103925833972501',
  //     value: '8,73',
  //   },
  // ];

  // const getClientsMock: Users[] = [
  //   {
  //     id: 8,
  //     name: 'HEBER',
  //     cnpj_cpf: '31052545223',
  //     ie_rg: '393751035',
  //     logradouro: 'Rua Teste 2',
  //     numero: '199',
  //     complemento: 'Apto 26',
  //     cidade: 'São Paulo',
  //     estado: 'SP',
  //     ibge: '555555',
  //     bairro: 'Centro',
  //     cep: '12345-777',
  //   },
  //   {
  //     id: 9,
  //     name: 'MURILO',
  //     cnpj_cpf: '15652512512',
  //     ie_rg: '4355544423',
  //     logradouro: 'Rua Teste 3',
  //     numero: '253',
  //     complemento: 'Apto 533',
  //     cidade: 'São Paulo',
  //     estado: 'SP',
  //     ibge: '555555',
  //     bairro: 'Centro',
  //     cep: '12345-666',
  //   },
  //   {
  //     id: 10,
  //     name: 'Cliente Teste',
  //     cnpj_cpf: '00000000000191',
  //     ie_rg: '',
  //     logradouro: 'Rua Exemplo',
  //     numero: '123',
  //     complemento: 'Apto 45',
  //     bairro: 'Centro',
  //     cidade: 'São José do Rio Pardo',
  //     estado: 'SP',
  //     cep: '13720000',
  //     ibge: '3549706',
  //   },
  // ];

  const getClients = useCallback(async () => {
    try {
      const response = await api.get('/companies/clients');
      setUsers(response.data.clients);
    } catch (error) {
      toast.error('Erro ao buscar clientes');
    }
  }, []);

  const getProducts = useCallback(async () => {
    try {
      const response = await api.get('/companies/products');
      setProducts(response.data.products);
    } catch (error) {
      toast.error('Erro ao listar produtos');
    }
  }, []);

  useEffect(() => {
    const getToken = getUserFromLocalStorage();
    if (!getToken) {
      return navigate('/');
    }
  }, [navigate]);

  useEffect(() => {
    getClients();
  }, [getClients]);

  useEffect(() => {
    getProducts();
  }, [getProducts]);

  return (
    <div className='w-full m-auto  flex flex-col justify-center items-center p-8 2xl:w-1/2 xl:w-1/2 lg:w-2/3'>
      <form onSubmit={handleSubmit(onSubmit)} className='w-full'>
        <h2 className='text-center text-sky-800 text-sm  font-light'>
          Selecione para qual cliente você vai gerar uma nota fiscal
        </h2>
        <div className='w-full bg-white shadow-md p-6 my-2 rounded'>
          <Controller
            name='users'
            control={control}
            render={({ field }) => (
              <Select
                {...field}
                // options={getClientsMock ?? []}
                options={users ?? []}
                getOptionValue={(option: Users) => `${option.id}`}
                getOptionLabel={(option: Users) => `${option.name}`}
                isSearchable
              />
            )}
          />
        </div>

        <hr className='my-4' />

        <h2 className='text-center text-sky-800 text-sm  font-light'>
          Selecione os produtos que deseja
        </h2>
        <div className='w-full bg-white shadow-md p-6 my-2 rounded'>
          <Controller
            name='products'
            control={control}
            render={({ field }) => (
              <Select
                {...field}
                // options={getProductsMock ?? []}
                options={products ?? []}
                getOptionValue={(option: Products) => `${option.id}`}
                getOptionLabel={(option: Products) => `${option.description}`}
                isSearchable
                isMulti
              />
            )}
          />
        </div>

        {watchProducts && watchProducts.length ? (
          <div className='w-full bg-white shadow-md p-6 my-2 rounded'>
            <div className='w-full flex flex-col'>
              {watchProducts.map((product: Products) => (
                <div
                  key={product.id}
                  className='w-full p-2 bg-slate-100 flex flex-col items-center justify-between mb-2'
                >
                  <div>{product.description}</div>
                  <div className='w-full grid grid-cols-4 gap-2'>
                    <input
                      type='text'
                      className='col-span-3 bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded text-slate-800 mb-4'
                      placeholder='Valor'
                    />
                    <input
                      type='text'
                      className='col-span-1 bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded text-slate-800 mb-4'
                      placeholder='Quantidade'
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          ''
        )}

        <button
          type='submit'
          // onClick={() => navigate('/invoice/summary')}
          className='bg-sky-800 hover:bg-sky-700 text-white px-2 py-3 rounded w-full'
        >
          Avançar
        </button>
      </form>
    </div>
  );
};
