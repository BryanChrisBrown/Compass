/* eslint-disable space-before-function-paren */
import React, { useState } from "react";
import PropTypes from "prop-types";
import NSButton from "./Button";
import Link from "next/link";
import { useRouter } from "next/router";

function NavBar(props) {
  //const { color, children } = props;
  const { route } = useRouter();
  let [tabActive, setActive] = useState(false);
  return (
    <div>
      <nav className="ns-nav full-width">
        <Link href="/home">
          <a>
            <NSButton
              isActive={route === "/home" ? true : false}
              width="150px"
              color="white"
            >
              Home
            </NSButton>
          </a>
        </Link>
        <Link href="/hardware">
          <a>
            <NSButton
              isActive={route === "/hardware" ? true : false}
              width="150px"
              color="white"
            >
              Hardware
            </NSButton>
          </a>
        </Link>
        <Link href="/software">
          <a>
            <NSButton
              isActive={route === "/software" ? true : false}
              width="150px"
              color="white"
            >
              Software
            </NSButton>
          </a>
        </Link>
        <Link href="/learn">
          <a>
            <NSButton
              isActive={route === "/learn" ? true : false}
              width="150px"
              color="white"
            >
              Learn
            </NSButton>
          </a>
        </Link>
      </nav>
    </div>
  );
}
/*
NavBar.defaultProps = {
  children: null,
  color: "normal",
};

NavBar.propTypes = {
  children: PropTypes.string,
  color: PropTypes.string,
};*/
export default NavBar;
