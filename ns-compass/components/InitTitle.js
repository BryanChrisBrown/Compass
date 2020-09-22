import React from "react";
// import PropTypes from 'prop-types';
import Link from "next/link";
import { useRouter } from "next/router";

function LoadingProgress() {
  const router = useRouter();
  return (
    <div
      className={"loadingProgress"}
      onAnimationEnd={() =>
        setTimeout(() => {
          router.push("/home");
        }, 1100)
      }
    ></div>
  );
}

class Title extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      doneLoading: false,
      loadingString: "Calibrating Flux Capacitors",
    };
  }

  componentDidMount() {
    this.setState({ doneLoading: false });
    // this func simulates loading by setting a
    // timeout before setting the `doneLoading` state as true (done)

    // in the future, we can set up an Eel function with a callback
    // that will load out devices and use async/await with said callback to
    // set our state and continue
    async function simLoading(thisParam) {
      const self = thisParam;
      await setTimeout(() => {
        self.setState({ doneLoading: true });
        self.props.loaderCallback(true);
      }, 4000);
    }
    simLoading(this);
  }

  render() {
    return (
      // eslint-disable-next-line no-unused-vars
      <div className="fullscreen">
        <div role="button" className="ns-title">
          <h1>Compass</h1>
          <div className="ns-line" />
          <div style={{ top: -40 }}>
            <p>Powered by Community</p>
          </div>
          <div>
            <div className="loadingBackground">
              <LoadingProgress />
            </div>
            {!this.state.doneLoading && (
              <p className="loader-msg">
                {this.state.loadingString}
                <span>.</span>
                <span>.</span>
                <span>.</span>
              </p>
            )}
          </div>
        </div>
      </div>
    );
  }
}

export default Title;
