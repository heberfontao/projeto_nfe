/* eslint-disable @typescript-eslint/no-explicit-any */
import { useNavigate, Link } from 'react-router-dom';
import { api } from '../../infra/api';
import { toast } from 'react-toastify';
import { useCallback, useEffect, useState } from 'react';
import { ThreeDots } from 'react-loader-spinner';
import { format } from 'date-fns';
import { getUserFromLocalStorage } from '../../infra/getToken';

export const InvoiceList = () => {
  const [isLoader, setIsLoader] = useState(false);
  const [invoices, setInvoices] = useState<any>(null);
  const navigate = useNavigate();

  const getInvoices = useCallback(async () => {
    try {
      setIsLoader(true);
      const response = await api.get('companies/nfe/consultar');
      setIsLoader(false);
      setInvoices(response.data);
    } catch (error) {
      setIsLoader(false);
      toast.error('erro ao listar notas');
    }
  }, []);

  useEffect(() => {
    getInvoices();
  }, [getInvoices]);

  useEffect(() => {
    const getToken = getUserFromLocalStorage();
    if (!getToken) {
      return navigate('/');
    }
  }, [navigate]);

  // const getPdfInvoice = useCallback(async (key: string) => {
  //   try {
  //     const response = await api.get(`companies/nfe/danfe/${key}`);
  //     console.log(response);
  //   } catch (error) {
  //     toast.error('Erro ao baixar PDF');
  //   }
  // }, []);

  return (
    <div className="w-full m-auto flex flex-col justify-center items-center p-8 2xl:w-1/2 xl:w-1/2 lg:w-2/3">
      <h2 className="text-center text-white font-bold bg-sky-800 p-3 w-full">
        Lista de notas emitidas
      </h2>
      <div className="w-full bg-white shadow-md p-6 mb-2 rounded">
        {isLoader ? (
          <div className="w-full m-auto">
            <ThreeDots
              visible={true}
              height="80"
              width="80"
              color="#069"
              radius="9"
              ariaLabel="three-dots-loading"
              wrapperStyle={{}}
              wrapperClass=""
            />
          </div>
        ) : (
          ''
        )}
        <div className="grid grid-cols-12 gap-4">
          {invoices &&
            invoices.map((invoice: any) => (
              <div className="col-span-12 bg-slate-100 p-2" key={invoice.id}>
                <p>Número da nota: {invoice.id}</p>
                <p>
                  Data: {format(new Date(invoice.data_emissao), 'dd/MM/yyyy')}
                </p>
                <p>
                  Chave da nota: <br />
                  {invoice.chave}
                </p>
                <div className="my-4">
                  <Link
                    to={`https://sistema-erp-ffk6w.ondigitalocean.app/api/v1/companies/nfe/danfe/${invoice.chave}`}
                    className="bg-sky-800 font-bold text-white rounded-xl px-4 py-2 my-4"
                  >
                    Baixar Danfe
                  </Link>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};
