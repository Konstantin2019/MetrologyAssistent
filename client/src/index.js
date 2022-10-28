import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css';
import LoadingIndicator from './indicator';
import { Provider } from 'react-redux'
import store from "./store/store";

ReactDOM.render(
  <div>
    <LoadingIndicator />
    <Provider store={ store }>
      <App />
    </Provider>
  </div>,
  document.getElementById('root')
);