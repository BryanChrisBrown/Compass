/* eslint-disable class-methods-use-this */
/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
// eslint-disable-next-line no-unused-vars

export default class Loading extends React.Component {
  // WARN: must use window.eel to keep parse-able eel.expose{...}

  componentDidMount () {
    window.eel.set_host('ws://localhost:8080');
    window.eel.expose(this.sayHelloJS, 'say_hello_js');
    window.eel.expose(this.show_log, 'show_log');

    // Test calling sayHelloJS, then call the corresponding Python function
    this.sayHelloJS('Javascript World!');
    window.eel.say_hello_py('Javascript World!');
  }
  // Test anonymous function when minimized. See https://github.com/samuelhwilliams/Eel/issues/363

  show_log (msg) {
    console.log(msg);
  }

  // Expose the `sayHelloJS` function to Python as `say_hello_js`

  sayHelloJS (x) {
    console.log(`Hello from ${x}`);
  }

  render () {
    return (
      <div>
        <Head><title>Loading compass...</title></Head>
        <Link href="/home">
          <a>go to app page</a>
        </Link>
      </div>
    );
  }
}
