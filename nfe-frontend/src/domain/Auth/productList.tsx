import { IoReturnDownBack } from 'react-icons/io5';
import { Link } from 'react-router-dom';

export const ProductList = () => {
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

  const getProductsMock: Products[] = [
    {
      id: 8,
      code: '1',
      description: 'Produto: ' + ' Fanta Uva 350ml',
      unit: 'UN',
      ncm: '35109999',
      cest: '1305170',
      gtin: '551651515615615611',
      value: '3.27',
    },
    {
      id: 10,
      code: '2',
      description: 'Produto: ' + ' Coca Cola 2L',
      unit: 'UN',
      ncm: '22021000',
      cest: '1305170',
      gtin: '551651515615615611',
      value: '8.00',
    },
    {
      id: 11,
      code: '3',
      description: 'Produto: ' + ' Fanta Laranja 1L',
      unit: 'UN',
      ncm: '49206173',
      cest: '5930416',
      gtin: '557103925833972501',
      value: '8.73',
    },
  ];

  return (
    <div className="w-full m-auto overflow-x-hidden overflow-y-auto flex flex-col justify-center items-center p-8 2xl:w-1/2 xl:w-1/2 lg:w-2/3">
      <p className="text-center text-sky-800 mb-6">Produtos cadastrados</p>

      {getProductsMock.map((product) => (
        <div
          className="w-full bg-slate-100 p-2 my-4 font-bold"
          key={product.id}
        >
          Id: {product.id} <br />
          Código: {product.code} <br />
          {product.description} <br />
          Unidade: {product.unit} <br />
          NCM: {product.ncm} <br />
          Cest: {product.cest} <br />
          Gtin: {product.gtin} <br />
          Valor unitário RS: {product.value} <br />
        </div>
      ))}

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
  );
};
