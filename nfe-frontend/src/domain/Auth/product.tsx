import { IoReturnDownBack, IoAddCircle } from 'react-icons/io5';
import { FaClipboardList } from 'react-icons/fa';
import { useForm, SubmitHandler } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
// import { api } from '../../infra/api';
import { toast } from 'react-toastify';

export const Product = () => {
  type ProductFormProps = {
    // id: string;
    code: string;
    description: string;
    unit: string;
    ncm: string;
    cest: string;
    gtin: string;
    price: string;
  };

  const navigate = useNavigate();
  const { register, handleSubmit } = useForm<ProductFormProps>();

  const onSubmit: SubmitHandler<ProductFormProps> = async (data) => {
    console.info(data);
    toast.success('Cadastro realizado com sucesso!');
    return navigate('/');
  };

  return (
    <div className="w-full m-auto overflow-x-hidden overflow-y-auto flex flex-col justify-center items-center p-8 2xl:w-1/2 xl:w-1/2 lg:w-2/3">
      <p className="text-center text-sky-800 mb-6">
        Realize o cadastro do produto
      </p>
      <form onSubmit={handleSubmit(onSubmit)} className="w-full">
        <h2 className="text-center text-white font-bold bg-sky-800 p-3">
          Dados do produto
        </h2>

        <div className="w-full bg-white shadow-md p-6 mb-4 rounded">
          {/* <label htmlFor="id" className="text-sky-800 font-bold text-sm mb-4">
            Id:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Id"
            {...register('id')}
          /> */}

          <label htmlFor="code" className="text-sky-800 font-bold text-sm mb-4">
            Código:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Código"
            {...register('code')}
          />

          <label
            htmlFor="description"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Descrição:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Descrição"
            {...register('description')}
          />

          <label htmlFor="unit" className="text-sky-800 font-bold text-sm mb-4">
            Unidade:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Unidade"
            {...register('unit')}
          />

          <label htmlFor="ncm" className="text-sky-800 font-bold text-sm mb-4">
            NCM do produto:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="NCM do produto"
            {...register('ncm')}
          />

          <label htmlFor="cest" className="text-sky-800 font-bold text-sm mb-4">
            Cest do produto:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Cest do produto"
            {...register('cest')}
          />

          <label htmlFor="gtin" className="text-sky-800 font-bold text-sm mb-4">
            Gtin do produto:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Gtin do produto"
            {...register('gtin')}
          />

          <label
            htmlFor="price"
            className="text-sky-800 font-bold text-sm mb-4"
          >
            Valor:
          </label>
          <input
            type="text"
            required
            className="w-full bg-white border border-slate-300 placeholder-slate-700 px-[0.6rem] py-[0.48rem] outline-none rounded mb-4 text-sky-800 placeholder:text-slate-400"
            placeholder="Valor"
            {...register('price')}
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
            to="/productList"
            className="font-bold text-sky-800 hover:text-slate-500 w-full flex items-center justify-center gap-2"
          >
            <FaClipboardList /> Clique aqui para listar os produtos cadastrados
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
