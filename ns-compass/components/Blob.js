import React from "react";
import PropTypes from "prop-types";
function Blob(props) {
  const { children } = props;
  return (
    <div className="ns-blob">
      <div className="ns-blob-child">{children}</div>
    </div>
  );
}

Blob.defaultProps = {
  children: null,
};

Blob.propTypes = {
  children: PropTypes.element,
};

export default Blob;
