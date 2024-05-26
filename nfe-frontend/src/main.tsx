import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';

import { RouterRoot } from './routes/RouterRoot';
import './assets/css/global.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.Fragment>
    <ToastContainer />
    <RouterProvider router={RouterRoot} />
  </React.Fragment>,
);
