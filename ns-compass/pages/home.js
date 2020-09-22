/* eslint-disable react/no-unescaped-entities */
/* eslint-disable class-methods-use-this */
import Head from "next/head";
import React, { useRef, useState, Suspense } from "react";
import styles from "../styles/Home.module.css";
import NSButton from "../components/Button";
import Bgrnd from "../components/InitBg";
import NavBar from "../components/NavBar";
import Blob from "../components/Blob";
import { Canvas, useFrame } from "react-three-fiber";
import { config, useSpring } from "react-spring";
import * as THREE from "three";
//import { useSpring, a } from "react-spring/three";
function PlaceholderCube(props) {
  // This reference will give us direct access to the mesh
  const mesh = useRef();

  // Set up state for the hovered and active state
  const [hovered, setHover] = useState(false);
  const [active, setActive] = useState(false);

  // Rotate mesh every frame, this is outside of React without overhead
  useFrame(() => {
    mesh.current.rotation.x = mesh.current.rotation.y += 0.02;
  });
  const colorSp = useSpring({
    to: "lightpink",
    from: "red",
  });
  return (
    <mesh
      {...props}
      ref={mesh}
      onClick={(e) => setActive(!active)}
      onPointerOver={(e) => setHover(true)}
      onPointerOut={(e) => setHover(false)}
    >
      <boxBufferGeometry attach="geometry" args={[1, 1, 1]} />
      <meshStandardMaterial attach="material" color={colorSp} />
    </mesh>
  );
}

function ThreeCanvas(props) {
  return (
    <div className="ns-three-canvas">
      <Canvas>
        <ambientLight intensity={0.2} />
        <spotLight position={[14, 10, 10]} angle={0.15} penumbra={1.1} />
        <pointLight position={[15, 1, -10]} />
        <PlaceholderCube scale={[3, 3, 3]} position={[0, 0, 0]} />
      </Canvas>
    </div>
  );
}

export default class AppHome extends React.Component {
  // WARN: must use window.eel to keep parse-able eel.expose{...}

  componentDidMount() {
    //window.eel.set_host("ws://localhost:8080");
  }

  render() {
    return (
      <div className="container">
        <Head>
          <title>Compass | Home</title>
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <NavBar />
        <main>
          <div className="ns-container">
            <Blob>
              <div>
                <div className="ns-3d">
                  <ThreeCanvas />
                </div>
                <p>
                  <b>Project Northstar</b> <br />
                  This Launcher serves as a starting point for Northstar
                  hardware and software. It allows for easy customization of the
                  calibration scripts, setup for SteamVR and Monado. It also
                  provides a dashboard for hardware detection and debugging.
                </p>
              </div>
            </Blob>
          </div>
        </main>
        <Bgrnd className="blurred" />
      </div>
    );
  }
}
