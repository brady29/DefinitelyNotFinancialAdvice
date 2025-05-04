import * as React from 'react';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Loading from './Loading.jsx'
import Alert from '@mui/material/Alert';
import Noti from './Noti.jsx'

const root = createRoot(document.getElementById('root'));

root.render(
  <StrictMode>
    <Loading />
  </StrictMode>,
);

$(document).ready(function () {
  let truths = undefined;

  $.ajax({
  	type: 'GET',
  	// url: 'http://127.0.0.1:8000/truth/latest\?n\=20',
  }).done(function(data) {
  	// Write result from server to website
  	truths = data;
    $.ajax({
      type: 'GET',
      url: 'http://127.0.0.1:8000/compare',
    }).done(function(data) {
      console.log(data);
    }).fail(function(jqXHR, textStatus) {
      root.render(
        <StrictMode>
          <Noti />
          <App truths={truths}/>
        </StrictMode>,
      )
    });
  }).fail(function(jqXHR, textStatus) {
    root.render(
      <StrictMode>
        <Alert severity="error">Server Rejects Request</Alert>
        <Loading />
      </StrictMode>,
    )
  });
})
