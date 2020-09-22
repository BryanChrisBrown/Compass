/* eslint-disable space-before-function-paren */
import React from "react";
import PropTypes from "prop-types";

function NSMenu(props) {
  const { children } = props;

  return (
    <div>
      <p>filler</p>
    </div>
  );
}

Button.defaultProps = {
  children: null,
  color: "normal",
  isActive: false,
  width: "auto",
};

Button.propTypes = {
  children: PropTypes.string,
  color: PropTypes.string,
  isActive: PropTypes.bool,
  width: PropTypes.string,
};
export default Button;
