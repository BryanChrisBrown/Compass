/* eslint-disable space-before-function-paren */
import React from 'react';
import PropTypes from 'prop-types';
/**
 *
 * @param {string} color - Text color to be rendered
 */

function Button (props) {
  const { color, children } = props;

  return (
    <div>
      <button type="button" className={`ns-button text-${color}`}>{children}</button>
    </div>
  );
}

Button.defaultProps = {
  children: null,
  color: 'normal',
};

Button.propTypes = {
  children: PropTypes.string,
  color: PropTypes.string,
};
export default Button;
