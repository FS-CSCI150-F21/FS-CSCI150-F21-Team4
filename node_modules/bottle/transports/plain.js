var tide = require('tide');

module.exports = function() {
  return function(logger, time, level, message) {
    var timestamp = tide.utc('YYYY-MM-DD hh:mm:ss.mmms UTC', time);
    console.log(timestamp + ' # ' + level + ': ' + message);
  };
};
