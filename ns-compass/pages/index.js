/* eslint-disable class-methods-use-this */
/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useState } from 'react';
import Head from 'next/head';
import Title from '../components/InitTitle';
import Bgrnd from '../components/InitBg';

export default function Loading () {
  // eslint-disable-next-line prefer-const
  let [isDone, setDone] = useState(0);
  // this is a callback function that is sent to our
  // title component as a prop. When loading is complete,
  // it calls this function and our local state variable
  // is updated
  const loadingCallback = (callbackData) => {
    console.log('got data', callbackData);
    if (callbackData) setDone(isDone = true);
  };
  return (
    <div>
      <Head><title>Loading compass...</title></Head>
      <Title loaderCallback={loadingCallback} />
      <Bgrnd runAnim={isDone} />
    </div>
  );
}
