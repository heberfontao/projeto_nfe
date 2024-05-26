import { IoReturnDownBack } from 'react-icons/io5';
import { Link } from 'react-router-dom';

export const ClientList = () => {
  type Clients = {
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

  const getClientsMock: Clients[] = [
    {
      id: 8,
      name: 'Nome: ' + ' HEBER',
      cnpj_cpf: 'CPF/CNPJ: ' + ' 31052545223',
      ie_rg: 'IE / RG: ' + ' 393751035',
      logradouro: 'Logradouro: ' + ' Rua Teste 2',
      numero: 'Número: ' + ' 199',
      complemento: 'Complemento: ' + ' Apto 26',
      cidade: 'Cidade: ' + ' São Paulo',
      estado: 'Estado: ' + ' SP',
      ibge: 'IBGE: ' + ' 555555',
      bairro: 'Bairro: ' + ' Centro',
      cep: 'CEP: ' + ' 12345-777',
    },
    {
      id: 9,
      name: 'Nome: ' + ' MURILO',
      cnpj_cpf: 'CPF/CNPJ: ' + ' 15652512512',
      ie_rg: 'IE / RG: ' + ' 4355544423',
      logradouro: 'Logradouro: ' + ' Rua Teste 3',
      numero: 'Número: ' + ' 253',
      complemento: 'Complemento: ' + ' Apto 533',
      cidade: 'Cidade: ' + ' São Paulo',
      estado: 'Estado: ' + ' SP',
      ibge: 'IBGE: ' + ' 555555',
      bairro: 'Bairro: ' + ' Centro',
      cep: 'CEP: ' + ' 12345-666',
    },
    {
      id: 10,
      name: 'Nome: ' + ' Cliente Teste',
      cnpj_cpf: 'CPF/CNPJ: ' + ' 00000000000191',
      ie_rg: '',
      logradouro: 'Logradouro: ' + ' Rua Exemplo',
      numero: 'Número: ' + ' 123',
      complemento: 'Complemento: ' + ' Apto 45',
      bairro: 'Bairro: ' + ' Centro',
      cidade: 'Cidade: ' + ' São José do Rio Pardo',
      estado: 'Estado: ' + ' SP',
      cep: 'CEP: ' + ' 13720000',
      ibge: 'IBGE: ' + ' 3549706',
    },
  ];

  return (
    <div className='w-full m-auto overflow-x-hidden overflow-y-auto flex flex-col justify-center items-center p-8 2xl:w-1/2 xl:w-1/2 lg:w-2/3'>
      <p className='text-center text-sky-800 mb-6'>Clientes cadastrados</p>

      {getClientsMock.map((client) => (
        <div className='w-full bg-slate-100 p-2 my-4 font-bold' key={client.id}>
          {client.name} <br />
          {client.cnpj_cpf} <br />
          {client.ie_rg} <br />
          {client.logradouro} <br />
          {client.numero} <br />
          {client.complemento} <br />
          {client.cidade} <br />
          {client.estado} <br />
          {client.ibge} <br />
          {client.bairro} <br />
          {client.cep} <br />
        </div>
      ))}

      <div className='w-full mt-4'>
        <div className='w-full m-auto mb-4'>
          <Link
            to='/'
            className='font-bold text-sky-800 hover:text-slate-500 w-full flex items-center justify-center gap-2'
          >
            <IoReturnDownBack /> Fazer login
          </Link>
        </div>

        <div className='w-full m-auto text-center'>
          <Link
            to='/registro'
            className='text-xs font-light text-slate-400 hover:text-slate-500'
          >
            Dúvidas e informações? email@contato.com
          </Link>
        </div>
      </div>
    </div>
  );
};
