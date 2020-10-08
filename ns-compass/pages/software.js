/* eslint-disable react/no-unescaped-entities */
/* eslint-disable class-methods-use-this */
import Head from "next/head";
import React from "react";
import styles from "../styles/Home.module.css";
import NSButton from "../components/Button";
import Bgrnd from "../components/InitBg";
import NavBar from "../components/NavBar";
import NSMenu from "../components/Menu";
import { useRouter } from "next/router";
export default class AppHome extends React.Component {
  // WARN: must use window.eel to keep parse-able eel.expose{...}

  render() {
    return (
      <div className="container">
        <Head>
          <title>Compass | Software</title>
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <NavBar />
        <main className={styles.main}>page coming soon</main>
        <Bgrnd className="blurred" />
      </div>
    );
  }
}
