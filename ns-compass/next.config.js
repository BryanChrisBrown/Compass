const path = require('path');

module.exports = {
  /* config options here */
  // enabling sass support
  sassOptions: {
    includePaths: [path.join(__dirname, 'styles')],
  },
  devIndicators: {
    autoPrerender: false,
  },
};
