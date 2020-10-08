/* eslint-disable react/prop-types */
/* eslint-disable react/jsx-props-no-spreading */
/* eslint-disable react/react-in-jsx-scope */
import { useEffect } from "react";
import "../styles/globals.css";
import "../styles/compass-bootstrap.sass";

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    window.eel.set_host("ws://localhost:8080");
  });
  return (
    <div className="nsapp-entry">
      <Component {...pageProps} />
      <script type="text/javascript" src="http://localhost:8080/eel.js" />
    </div>
  );
}

export default MyApp;
