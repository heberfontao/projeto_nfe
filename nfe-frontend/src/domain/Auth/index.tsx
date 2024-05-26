import { useForm, SubmitHandler } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../../infra/api';
import { toast } from 'react-toastify';
import { useState } from 'react';
import { ThreeDots } from 'react-loader-spinner';

export const Auth = () => {
  type AuthFormProps = {
    email: string;
    password: string;
  };

  const navigate = useNavigate();
  const [isLoader, setIsLoader] = useState(false);
  const { register, handleSubmit } = useForm<AuthFormProps>();

  const onSubmit: SubmitHandler<AuthFormProps> = async (data) => {
    localStorage.clear();
    try {
      setIsLoader(true);
      const response = await api.post('/auth/signin', data);
      localStorage.setItem('erp', JSON.stringify(response.data));
      toast.success('Login realizado com sucesso!');
      setIsLoader(false);
      return navigate('/invoice');
    } catch (error: unknown) {
      setIsLoader(false);
      return toast.error('Loagin ou senha inválidos');
    }
  };

  return (
    <div className='w-full m-auto  flex flex-col justify-center items-center p-8 2xl:w-1/2 xl:w-1/2 lg:w-2/3'>
      <form onSubmit={handleSubmit(onSubmit)} className='w-full'>
        <h2 className='text-center text-sky-800 text-sm  font-light'>
          Realize o login no sistema
        </h2>

        <div className='w-full bg-white shadow-md p-6 my-4 rounded'>
          <input
            type='email'
            required
            className='w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded text-slate-800 mb-4'
            placeholder='e-mail'
            {...register('email')}
          />

          <input
            type='password'
            required
            className='w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded text-slate-800'
            placeholder='Senha'
            {...register('password')}
          />
        </div>

        {isLoader ? (
          <div className='w-full flex justify-center items-center'>
            <ThreeDots
              visible={true}
              height='80'
              width='80'
              color='#069'
              radius='9'
              ariaLabel='three-dots-loading'
            />
          </div>
        ) : (
          <button
            type='submit'
            className='bg-sky-800 hover:bg-sky-700 text-white px-2 py-3 rounded w-full'
          >
            Entrar
          </button>
        )}
      </form>

      <div className='w-full mt-4'>
        <div className='w-full m-auto text-center mb-4'>
          <Link
            to='/register'
            className='font-bold text-sky-800 hover:text-slate-500 w-full'
          >
            Clique aqui e faça seu cadastro
          </Link>
        </div>

        <div className='w-full m-auto text-center'>
          <p className='text-xs font-light text-slate-400 hover:text-slate-500'>
            Dúvidas e informações? email@contato.com
          </p>
        </div>
      </div>
    </div>
  );
};
