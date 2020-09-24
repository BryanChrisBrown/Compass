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

/* Todo, add suport for multiple menu's in a page. This will likely be done by checking if any of a menu's `active` props are satisfied or not, 
   if one isn't and there's an `activeTab` query in the URL, we know that there's another menu in use and the current menu needs to have its index
   highlighted
  */
function NSMenu(props) {
  const { children } = props;
  const router = useRouter();
  let isIndex = false;
  if (!router.query.activeTab) {
    isIndex = true;
  }
  const renderedItems = children.map((i, index) => {
    return (
      <li
        className={`ns-menu-item ${
          i.props.active == router.query.activeTab || (isIndex && index === 0)
            ? "ns-menu-item-active"
            : ""
        }`}
        key={index}
      >
        <Link href={{ query: { activeTab: `${i.props.active}` } }}>
          <a>{i}</a>
        </Link>
      </li>
    );
  });
  return <ul className="ns-menu">{renderedItems}</ul>;
}

NSMenu.defaultProps = {
  children: null,
  color: "normal",
  isActive: false,
  width: "auto",
};

NSMenu.propTypes = {
  children: PropTypes.array,
  color: PropTypes.string,
  isActive: PropTypes.bool,
  width: PropTypes.string,
};
export default NSMenu;
