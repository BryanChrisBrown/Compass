/* eslint-disable class-methods-use-this */
/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useState } from "react";
import Head from "next/head";
import NSButton from "../components/Button";
import Bgrnd from "../components/InitBg";
import NavBar from "../components/NavBar";
import Blob from "../components/Blob";
import NSMenu from "../components/Menu";

export default function Hardware() {
  return (
    <div className="container">
      <Head>
        <title>Compass | Hardware</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <NavBar />
      <main>
        <div className="ns-container">
          <div
            style={{ height: "300px" }}
            className="row ns-flex justify-between"
          >
            <div className="ns-flex justify-between">
              <NSMenu menuID={"1"}>
                <p active="leapmotion">LeapMotion</p>
                <p active="connection">Connection</p>
                <p active="bandwidth">Bandwidth</p>
                <p active="tracking">Tracking</p>
              </NSMenu>
            </div>
            <div style={{ width: "32vw" }}>
              <Blob>
                <p>LeapMotion View</p>
              </Blob>
            </div>
            <div style={{ width: "32vw" }}>
              <Blob>
                <p>LeapMotion Output</p>
              </Blob>
            </div>
          </div>

          <div style={{ height: "40px" }} />

          <div
            style={{ height: "300px" }}
            className="row ns-flex justify-between"
          >
            <div className="ns-flex justify-between">
              <NSMenu menuID={"2"}>
                <p active="realsense">RealSense</p>
                <p active="connection">Connection</p>
                <p active="bandwidth">Bandwidth</p>
                <p active="tracking">Tracking</p>
              </NSMenu>
            </div>
            <div style={{ width: "32vw" }}>
              <Blob>
                <p>RealSense View</p>
              </Blob>
            </div>
            <div style={{ width: "32vw" }}>
              <Blob>
                <p>RealSense Output</p>
              </Blob>
            </div>
          </div>
        </div>
      </main>
      <Bgrnd className="blurred" />
    </div>
  );
}
