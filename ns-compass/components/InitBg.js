import React from 'react';
import { animated } from 'react-spring';
import PropTypes from 'prop-types';

function Background(props) {
  const { runAnim } = props;
  console.log('cur props', props);

  return (
    <div className="nsbg-container">
      <animated.div className={`nsbg-circle ${runAnim === true ? 'bg-animated' : ''}`} />
    </div>
  );
}

Background.defaultProps = {
  runAnim: false,
};

Background.propTypes = {
  runAnim: PropTypes.bool,
};

export default Background;
