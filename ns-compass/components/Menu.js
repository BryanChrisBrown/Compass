/* eslint-disable space-before-function-paren */
import React from "react";
import PropTypes from "prop-types";
import Link from "next/link";
import { useRouter } from "next/router";

/* 
  This component takes in elements/an array of elements (multiple elements) as it's children
  
  With each item, include its "active" prop, this allows it to be dynamically highlighted. Say you have a page with a menu of three items (help, learn more, and contact us).
  When you click on the "help" button, it'll show that content, and by setting the "active prop" to `help,` it will be highlighted as the current menu item
*/

function NSMenu(props) {
  const { children, menuID } = props;

  const router = useRouter();
  const tabID = `activeTab${menuID}`;
  let isIndex = false;
  if (!router.query[tabID]) {
    isIndex = true;
  }
  // this checker acts as a fallback if a menuID isn't supplied

  function checkExternalState() {
    const extStateChecker = children.filter(
      (ele) => ele.props.active == router.query[tabID]
    );
    if (!extStateChecker.length) return true;
  }
  if (!router.query[tabID]) {
    if (checkExternalState()) {
      isIndex = true;
    }
  }
  const renderedItems = children.map((i, index) => {
    return (
      <li
        className={`ns-menu-item ${
          i.props.active == router.query[tabID] || /*isIndex &&*/ index === 0
            ? "ns-menu-item-active"
            : ""
        }`}
        key={index}
      >
        <Link
          href={{
            query: { [tabID]: `${i.props.active}` },
          }}
        >
          <a className="no-underline">{i}</a>
        </Link>
      </li>
    );
  });
  return (
    <div className="ns-menu-container">
      <ul className="ns-menu">{renderedItems}</ul>
    </div>
  );
}

//this doesn't really matter but I don't want to remove it cause it'll prolly break everything

NSMenu.defaultProps = {
  children: null,
  color: "normal",
  isActive: false,
  width: "auto",
  menuID: "",
};

NSMenu.propTypes = {
  children: PropTypes.array,
  color: PropTypes.string,
  isActive: PropTypes.bool,
  width: PropTypes.string,
};
export default NSMenu;
