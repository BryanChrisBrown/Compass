/* eslint-disable space-before-function-paren */
import React from "react";
import PropTypes from "prop-types";

function Button(props) {
  const { color, children, isActive, width } = props;

  return (
    <div>
      <button
        type="button"
        style={{ width: width }}
        className={`ns-button text-${color} ${isActive ? "btn-active" : ""}`}
      >
        {children}
      </button>
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
