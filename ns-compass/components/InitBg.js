import React from "react";
import { animated } from "react-spring";
import PropTypes from "prop-types";

function Background(props) {
  const { runAnim } = props;
  console.log("cur props", props);
  return (
    <div className="nsbg-container">
      <animated.div
        className={`nsbg-circle ${runAnim === true ? "bg-animated" : ""} ${
          props.className
        }`}
      />
    </div>
  );
}

Background.defaultProps = {
  runAnim: false,
  exStyles: "",
};

Background.propTypes = {
  runAnim: PropTypes.bool,
  exStyles: PropTypes.string,
};

export default Background;
