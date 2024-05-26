import { createBrowserRouter } from 'react-router-dom';
import { Invoice } from '../domain/Invoice';
import { InvoiceSummary } from '../domain/Invoice/summary';
import { InvoiceList } from '../domain/Invoice/list';
import { Auth } from '../domain/Auth';
import { Register } from '../domain/Auth/register';
import { Product } from '../domain/Auth/product';
import { ProductList } from '../domain/Auth/productList';
import { ClientList } from '../domain/Auth/clientList';
import { Client } from '../domain/Auth/client';

export const RouterRoot = createBrowserRouter([
  {
    path: '/',
    element: <Auth />,
  },
  {
    path: '/register',
    element: <Register />,
  },
  {
    path: '/invoice',
    element: <Invoice />,
  },
  {
    path: '/product',
    element: <Product />,
  },
  {
    path: '/productList',
    element: <ProductList />,
  },
  {
    path: '/invoice/summary',
    element: <InvoiceSummary />,
  },
  {
    path: '/invoice/list',
    element: <InvoiceList />,
  },
  {
    path: '/client',
    element: <Client />,
  },
  {
    path: '/clientList',
    element: <ClientList />,
  },
]);
