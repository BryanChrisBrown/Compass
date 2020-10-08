/* eslint-disable react/no-unescaped-entities */
/* eslint-disable class-methods-use-this */
import Head from "next/head";
import React from "react";
import styles from "../styles/Home.module.css";
import NSButton from "../components/Button";
import Bgrnd from "../components/InitBg";
import NavBar from "../components/NavBar";
import NSMenu from "../components/Menu";
import Blob from "../components/Blob";
import { useRouter } from "next/router";
export default class AppHome extends React.Component {
  // WARN: must use window.eel to keep parse-able eel.expose{...}

  render() {
    return (
      <div className="container">
        <Head>
          <title>Compass | Learn</title>
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <NavBar />
        <main>
          <div className="ns-container">
            <div
              style={
                {
                  /*height: "300px", 
                "font-size": "0.9 em", */
                }
              }
              className="row ns-flex justify-between"
            >
              <div className="ns-flex justify-between">
                <NSMenu menuID={"1"}>
                  <p active="leapmotion">Hardware</p>
                  <p active="connection">2D Calibration</p>
                  <p active="bandwidth">3D Calibration</p>
                  <p active="tracking">Camera Calibration</p>
                </NSMenu>
              </div>
            </div>

            <div style={{ height: "40px" }} />

            <div
              style={
                {
                  /*height: "300px"*/
                }
              }
              className="row ns-flex justify-between"
            >
              <div className="ns-flex justify-between">
                <NSMenu menuID={"2"}>
                  <p active="realsense">Software</p>
                  <p active="connection">Optics</p>
                  <p active="bandwidth">Tracking</p>
                  <p active="tracking">Meshing</p>
                </NSMenu>
              </div>
            </div>
          </div>
        </main>
        <Bgrnd className="blurred" />
      </div>
    );
  }
}
