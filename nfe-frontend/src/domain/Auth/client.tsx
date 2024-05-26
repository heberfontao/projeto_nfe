import { IoReturnDownBack, IoAddCircle } from 'react-icons/io5';
import { FaClipboardList } from 'react-icons/fa';
import { useForm, SubmitHandler } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
// import { api } from '../../infra/api';
import { toast } from 'react-toastify';

export const Client = () => {
  type ClientFormProps = {
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

  const navigate = useNavigate();
  const { register, handleSubmit } = useForm<ClientFormProps>();

  const onSubmit: SubmitHandler<ClientFormProps> = async (data) => {
    console.info(data);
    toast.success('Cadastro realizado com sucesso!');
    return navigate('/');
  };

  return (
    <div className="w-full m-auto overflow-x-hidden overflow-y-auto flex flex-col justify-center items-center p-8 2xl:w-1/2 xl:w-1/2 lg:w-2/3">
      <p className="text-center text-sky-800 mb-6">
        Realize o cadastro do cliente
      </p>
      <form onSubmit={handleSubmit(onSubmit)} className="w-full">
        <h2 className="text-center text-white font-bold bg-sky-800 p-3">
          Dados do cliente
        </h2>

        <div className="w-full bg-white shadow-md p-6 mb-4 rounded">
          <label htmlFor="name" className="text-sky-800 font-bold text-sm mb-4">
            Nome / Razão social:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Nome / Razão social"
            {...register('name')}
          />

          <label
            htmlFor="cnpj_cpf"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            CPF / CNPJ:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="CPF / CNPJ"
            {...register('cnpj_cpf')}
          />

          <label
            htmlFor="ie_rg"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Inscrição estadual / RG:
          </label>
          <input
            type="text"
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Inscrição estadual / RG"
            {...register('ie_rg')}
          />

          <label
            htmlFor="logradouro"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Logradouro:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Logradouro"
            {...register('logradouro')}
          />

          <label
            htmlFor="numero"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Número:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Número"
            {...register('numero')}
          />

          <label
            htmlFor="complemento"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Complemento:
          </label>
          <input
            type="text"
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Complemento"
            {...register('complemento')}
          />

          <label
            htmlFor="cidade"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Cidade:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Cidade"
            {...register('cidade')}
          />

          <label
            htmlFor="estado"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Estado:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Estado"
            {...register('estado')}
          />

          <label htmlFor="ibge" className="text-sky-800 font-bold text-sm mb-4">
            IBGE:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="IBGE"
            {...register('ibge')}
          />

          <label
            htmlFor="bairro"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Bairro:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Bairro"
            {...register('bairro')}
          />

          <label htmlFor="cep" className="text-sky-800 font-bold text-sm mb-4">
            CEP:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="CEP"
            {...register('cep')}
          />
        </div>

        <button
          type="submit"
          className="bg-sky-800 hover:bg-sky-700 text-white px-2 py-3 rounded w-full flex justify-center items-center gap-2"
        >
          <IoAddCircle />
          Cadastrar
        </button>
      </form>

      <div className="w-full mt-4">
        <div className="w-full m-auto mb-4">
          <Link
            to="/clientList"
            className="font-bold text-sky-800 hover:text-slate-500 w-full flex items-center justify-center gap-2"
          >
            <FaClipboardList /> Clique aqui para listar os clientes cadastrados
          </Link>
        </div>
        <div className="w-full m-auto mb-4">
          <Link
            to="/"
            className="font-bold text-sky-800 hover:text-slate-500 w-full flex items-center justify-center gap-2"
          >
            <IoReturnDownBack /> Fazer login
          </Link>
        </div>

        <div className="w-full m-auto text-center">
          <Link
            to="/registro"
            className="text-xs font-light text-slate-400 hover:text-slate-500"
          >
            Dúvidas e informações? email@contato.com
          </Link>
        </div>
      </div>
    </div>
  );
};
