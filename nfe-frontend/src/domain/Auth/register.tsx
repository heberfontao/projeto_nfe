import { IoReturnDownBack, IoAddCircle } from 'react-icons/io5';
import { IoMdPersonAdd } from 'react-icons/io';
import { GiSodaCan } from 'react-icons/gi';
import { useForm, SubmitHandler } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
// import { api } from '../../infra/api';
import { toast } from 'react-toastify';

export const Register = () => {
  type RegisterFormProps = {
    email: string;
    password: string;
    name: string;
    cnpj: string;
    ie: string;
    phone: string;
    street: string;
    district: string;
    number: string;
    city: string;
    state: string;
    zipCode: string;
    complement?: string;
  };

  const navigate = useNavigate();
  const { register, handleSubmit } = useForm<RegisterFormProps>();

  const onSubmit: SubmitHandler<RegisterFormProps> = async (data) => {
    console.info(data);
    toast.success('Cadastro realizado com sucesso!');
    return navigate('/');
  };

  return (
    <div className="w-full m-auto overflow-x-hidden overflow-y-auto flex flex-col justify-center items-center p-8 2xl:w-1/2 xl:w-1/2 lg:w-2/3">
      <p className="text-center text-sky-800 mb-6">
        Realize o cadastro preenchendo todos os campos abaixo corretamente
      </p>
      <form onSubmit={handleSubmit(onSubmit)} className="w-full">
        <h2 className="text-center text-white font-bold bg-sky-800 p-3">
          Dados para login
        </h2>

        <div className="w-full bg-white shadow-md p-6 mb-6 rounded">
          <label
            htmlFor="email"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            E-mail:
          </label>
          <input
            type="email"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="e-mail"
            {...register('email')}
          />

          <label
            htmlFor="password"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Senha:
          </label>
          <input
            type="password"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Senha"
            {...register('password')}
          />
        </div>

        <h2 className="text-center text-white font-bold bg-sky-800 p-3">
          Dados da empresa
        </h2>

        <div className="w-full bg-white shadow-md p-6 mb-4 rounded">
          <label htmlFor="name" className="text-sky-800 font-bold text-sm mb-4">
            Razão social:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Razão social"
            {...register('name')}
          />

          <label htmlFor="cnpj" className="text-sky-800 font-bold text-sm mb-4">
            CNPJ:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="CNPJ"
            {...register('name')}
          />

          <label htmlFor="ie" className="text-sky-800 font-bold text-sm mb-4">
            Inscrição estadual:
          </label>
          <input
            type="text"
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Inscrição estadual"
            {...register('ie')}
          />

          <label
            htmlFor="street"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Endereço:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Rua / Av."
            {...register('street')}
          />
          <label
            htmlFor="number"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Número:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Número"
            {...register('number')}
          />

          <label
            htmlFor="number"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Complemento:
          </label>
          <input
            type="text"
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Complemento"
            {...register('complement')}
          />

          <label
            htmlFor="district"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Bairro:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Bairro"
            {...register('district')}
          />

          <label htmlFor="city" className="text-sky-800 font-bold text-sm mb-4">
            Cidade:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Cidade"
            {...register('city')}
          />

          <label htmlFor="city" className="text-sky-800 font-bold text-sm mb-4">
            Estado:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Estado"
            {...register('state')}
          />

          <label
            htmlFor="zipCode"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            CEP:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="CEP"
            {...register('zipCode')}
          />

          <label
            htmlFor="phone"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Telefone:
          </label>
          <input
            type="text"
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Telefone"
            {...register('phone')}
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
        <div className="w-full m-auto text-center mb-4">
          <Link
            to="/product"
            className="font-bold text-sky-800 hover:text-slate-500 w-full flex items-center justify-center gap-2"
          >
            <GiSodaCan /> Clique aqui e faça o cadastro dos produtos
          </Link>
        </div>

        <div className="w-full m-auto text-center mb-4">
          <Link
            to="/client"
            className="font-bold text-sky-800 hover:text-slate-500 w-full flex items-center justify-center gap-2"
          >
            <IoMdPersonAdd /> Clique aqui e faça o cadastro dos clientes
          </Link>
        </div>

        <div className="w-full mt-4">
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
    </div>
  );
};
