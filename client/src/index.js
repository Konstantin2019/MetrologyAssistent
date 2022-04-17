import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css';
import LoadingIndicator from './indicator';

ReactDOM.render(
  <div>
    <LoadingIndicator />
    <App />
  </div>,
  document.getElementById('root')
);